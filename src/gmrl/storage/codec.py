"""Tagged JSON: no pickle and no lossy Decimal/offset conversion."""

from typing import Any
import dataclasses
import json
from datetime import date, datetime
from decimal import Decimal
from gmrl import domain


def encode(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            "@": type(value).__name__,
            "v": {f.name: encode(getattr(value, f.name)) for f in dataclasses.fields(value)},
        }
    if isinstance(value, Decimal):
        return {"@": "Decimal", "v": str(value)}
    if isinstance(value, datetime):
        return {"@": "datetime", "v": value.isoformat()}
    if isinstance(value, date):
        return {"@": "date", "v": value.isoformat()}
    if isinstance(value, tuple):
        return {"@": "tuple", "v": [encode(v) for v in value]}
    if isinstance(value, list):
        return [encode(v) for v in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


def decode(value: Any) -> Any:
    if isinstance(value, list):
        return [decode(v) for v in value]
    if not isinstance(value, dict):
        return value
    if "@" not in value:
        return {k: decode(v) for k, v in value.items()}
    if set(value) != {"@", "v"}:
        raise ValueError("Tagged payload requires exactly type and value fields")
    tag, item = (value["@"], value["v"])
    if tag == "Decimal":
        return Decimal(item)
    if tag == "datetime":
        return datetime.fromisoformat(item)
    if tag == "date":
        return date.fromisoformat(item)
    if tag == "tuple":
        return tuple((decode(v) for v in item))
    cls = getattr(domain, tag, None) if isinstance(tag, str) else None
    if not isinstance(cls, type) or not dataclasses.is_dataclass(cls):
        raise ValueError("Unknown record")
    expected = {field.name for field in dataclasses.fields(cls)}
    if not isinstance(item, dict) or set(item) != expected:
        raise ValueError("Persisted record must contain exactly its complete field set")
    return cls(**{k: decode(v) for k, v in item.items()})


def dumps(value: Any) -> str:
    return json.dumps(encode(value), sort_keys=True, separators=(",", ":"), allow_nan=False)


def loads(value: str) -> Any:
    return decode(json.loads(value))
