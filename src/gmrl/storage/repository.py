from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from typing import Any, Literal
from hashlib import sha256
from uuid import uuid4
import sqlite3
from gmrl.domain import (
    ProviderStatus,
    PaperState,
    CanonicalOrder,
    Fill,
    CorporateAction,
    JournalEntry,
    MarketData,
)
from typing import Iterator
from gmrl.errors import AccountingError, DataUnavailableError
from gmrl.storage.codec import dumps, loads
from gmrl.data.validation import validate_market_data


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> Literal[False]:
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


class PaperTransaction:
    """Persistence only. Callers supply validated accounting reductions."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def _get(self, kind: str, key: str) -> Any:
        row = self.connection.execute(
            "SELECT payload FROM paper WHERE kind=? AND id=?", (kind, key)
        ).fetchone()
        return loads(row[0]) if row else None

    def _put(self, kind: str, key: str, value: Any, parent: str | None = None) -> None:
        try:
            self.connection.execute(
                "INSERT INTO paper(kind,id,payload,parent_kind,parent_id,unique_fill_id) VALUES (?,?,?,?,?,?)",
                (
                    kind,
                    key,
                    dumps(value),
                    "order" if parent else None,
                    parent,
                    value.fill_id if kind == "fill" else None,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise AccountingError("Duplicate persisted identity") from exc

    def load_account(self) -> PaperState | None:
        return self._get("account", "one")

    def save_account(self, state: PaperState, *, expected_version: int | None) -> None:
        from gmrl.data.validation import aware

        aware(state.simulation_time)
        if (
            state.account.cash_eur < 0
            or not state.account.cash_eur.is_finite()
            or (not state.initial_cash_eur.is_finite())
            or (state.initial_cash_eur <= 0)
        ):
            raise AccountingError("Invalid paper cash/capital")
        prior = self.load_account()
        if (prior.version if prior else None) != expected_version:
            raise AccountingError("Paper state version conflict")
        if prior and (
            state.initial_cash_eur != prior.initial_cash_eur
            or state.simulation_time < prior.simulation_time
            or state.version != prior.version + 1
        ):
            raise AccountingError("Capital, time or version conflict")
        if not prior and state.version != 0:
            raise AccountingError("Initial version must be zero")
        self.connection.execute(
            "INSERT INTO paper(kind,id,payload) VALUES ('account','one',?) ON CONFLICT(kind,id) DO UPDATE SET payload=excluded.payload",
            (dumps(state),),
        )

    def lookup_order(self, client_order_id: str) -> CanonicalOrder | None:
        return self._get("order", client_order_id)

    def lookup_fill(self, client_order_id: str) -> Fill | None:
        return self._get("fill", client_order_id)

    def lookup_action(self, action_id: str) -> CorporateAction | None:
        return self._get("action", action_id)

    def lookup_journal(self, entry_id: str) -> JournalEntry | None:
        return self._get("journal", entry_id)

    def append_order(self, order: CanonicalOrder) -> None:
        self._put("order", order.order.client_order_id, order)

    def append_fill(self, client_order_id: str, fill: Fill) -> None:
        if self.lookup_order(client_order_id) is None:
            raise AccountingError("Fill requires persisted canonical order")
        self._put("fill", client_order_id, fill, client_order_id)

    def append_action(self, action: CorporateAction) -> None:
        self._put("action", action.action_id, action)

    def append_journal(self, entry: JournalEntry) -> None:
        if entry.order_id and self.lookup_order(entry.order_id) is None:
            raise AccountingError("Unknown journal order")
        self._put("journal", entry.entry_id, entry, entry.order_id)

    def _records(self, kind: str) -> tuple[Any, ...]:
        rows = self.connection.execute(
            "SELECT payload FROM paper WHERE kind=? ORDER BY id", (kind,)
        )
        return tuple(loads(row[0]) for row in rows)

    def orders(self) -> tuple[CanonicalOrder, ...]:
        """Canonical orders in ascending client order ID order."""
        return self._records("order")

    def fills(self) -> tuple[Fill, ...]:
        """Fills in ascending associated client order ID order."""
        return self._records("fill")

    def actions(self) -> tuple[CorporateAction, ...]:
        """Applied action records in ascending action ID order."""
        return self._records("action")

    def journal(self) -> tuple[JournalEntry, ...]:
        return tuple(
            (
                loads(r[0])
                for r in self.connection.execute(
                    "SELECT payload FROM paper WHERE kind='journal' ORDER BY id"
                )
            )
        )


class Repository:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "datasets").mkdir(exist_ok=True)
        with self.connect() as c:
            c.executescript(
                "CREATE TABLE IF NOT EXISTS paper(kind TEXT,id TEXT,payload TEXT NOT NULL,unique_fill_id TEXT UNIQUE,parent_kind TEXT,parent_id TEXT,PRIMARY KEY(kind,id),FOREIGN KEY(parent_kind,parent_id) REFERENCES paper(kind,id)); CREATE TABLE IF NOT EXISTS datasets(id TEXT PRIMARY KEY,payload TEXT NOT NULL); CREATE TABLE IF NOT EXISTS experiments(id TEXT PRIMARY KEY,payload TEXT NOT NULL); CREATE TABLE IF NOT EXISTS cache(key TEXT PRIMARY KEY,payload TEXT NOT NULL); CREATE TABLE IF NOT EXISTS usage(provider TEXT,at TEXT,outcome TEXT,debit INTEGER);"
            )

    def connect(self) -> ClosingConnection:
        c = sqlite3.connect(self.root / "metadata.sqlite3", timeout=10, factory=ClosingConnection)
        c.execute("PRAGMA foreign_keys=ON")
        return c

    def save_dataset(self, data: MarketData) -> str:
        validate_market_data(data)
        payload = dumps(data)
        dataset_id = sha256(payload.encode()).hexdigest()
        import pyarrow as pa
        import pyarrow.parquet as pq

        rows = [
            {"record_type": kind, "record": dumps(record)}
            for kind in ("instruments", "sessions", "bars", "actions", "fx", "provenance")
            for record in getattr(data, kind)
        ]
        target = self.root / "datasets" / (dataset_id + ".parquet")
        if not target.exists():
            temporary = target.with_name(dataset_id + "." + uuid4().hex + ".tmp")
            try:
                pq.write_table(pa.Table.from_pylist(rows), temporary)
                temporary.replace(target)
            finally:
                temporary.unlink(missing_ok=True)
        with self.connect() as c:
            c.execute("INSERT OR IGNORE INTO datasets VALUES (?,?)", (dataset_id, payload))
        return dataset_id

    def load_dataset(self, dataset_id: str) -> MarketData:
        if len(dataset_id) != 64 or any((c not in "0123456789abcdef" for c in dataset_id)):
            raise DataUnavailableError("Invalid dataset identity")
        import pyarrow.parquet as pq
        from gmrl.domain import MarketData

        try:
            rows = pq.read_table(self.root / "datasets" / (dataset_id + ".parquet")).to_pylist()
        except (OSError, ValueError) as exc:
            raise DataUnavailableError("Dataset unavailable") from exc
        groups: dict[str, list[Any]] = {
            k: [] for k in ("instruments", "sessions", "bars", "actions", "fx", "provenance")
        }
        for row in rows:
            groups[row["record_type"]].append(loads(row["record"]))
        data = MarketData(**{k: tuple(v) for k, v in groups.items()})
        if sha256(dumps(data).encode()).hexdigest() != dataset_id:
            raise DataUnavailableError("Dataset hash mismatch")
        validate_market_data(data)
        return data

    def save_experiment(self, manifest: dict[str, object]) -> str:
        payload = dumps(manifest)
        key = sha256(payload.encode()).hexdigest()
        with self.connect() as c:
            c.execute("INSERT OR IGNORE INTO experiments VALUES (?,?)", (key, payload))
        return key

    def list_experiments(self) -> tuple[dict[str, object], ...]:
        """Unmodified saved manifests in ascending content-derived ID order."""
        with self.connect() as connection:
            rows = connection.execute("SELECT payload FROM experiments ORDER BY id")
            return tuple(loads(row[0]) for row in rows)

    def load_experiment(self, experiment_id: str) -> dict[str, object]:
        """Load the exact saved manifest; absence is an actionable data error."""
        with self.connect() as connection:
            row = connection.execute(
                "SELECT payload FROM experiments WHERE id=?", (experiment_id,)
            ).fetchone()
        if row is None:
            raise DataUnavailableError("Saved experiment not found")
        return loads(row[0])

    def experiments(self) -> tuple[tuple[str, dict[str, object]], ...]:
        with self.connect() as c:
            return tuple(
                (
                    (r[0], loads(r[1]))
                    for r in c.execute("SELECT id,payload FROM experiments ORDER BY rowid DESC")
                )
            )

    def record_usage(self, provider: str, at: datetime, outcome: str, debit: int = 1) -> None:
        with self.connect() as c:
            c.execute(
                "INSERT INTO usage VALUES (?,?,?,?)", (provider, at.isoformat(), outcome, debit)
            )

    def provider_status(self) -> tuple[ProviderStatus, ...]:
        with self.connect() as c:
            return tuple(
                (
                    ProviderStatus(r[0], True, "Persisted usage; quota unknown", r[1], None)
                    for r in c.execute("SELECT provider,SUM(debit) FROM usage GROUP BY provider")
                )
            )

    def usage_stats(self) -> tuple[tuple[str, str, int, int], ...]:
        with self.connect() as c:
            return tuple(
                c.execute(
                    "SELECT provider,outcome,COUNT(*),SUM(debit) FROM usage GROUP BY provider,outcome"
                )
            )

    def cache_get(self, key: str) -> Any:
        with self.connect() as c:
            row = c.execute("SELECT payload FROM cache WHERE key=?", (key,)).fetchone()
        return loads(row[0]) if row else None

    def cache_put(self, key: str, value: Any) -> None:
        with self.connect() as c:
            c.execute("INSERT OR REPLACE INTO cache VALUES (?,?)", (key, dumps(value)))

    @contextmanager
    def paper_transaction(self) -> Iterator[PaperTransaction]:
        c = self.connect()
        try:
            c.execute("BEGIN IMMEDIATE")
            yield PaperTransaction(c)
            c.commit()
        except BaseException:
            c.rollback()
            raise
        finally:
            c.close()
