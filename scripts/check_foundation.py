"""No-download foundation check. Run after the approved package installation."""

from pathlib import Path
from tempfile import TemporaryDirectory
from gmrl.providers.sample import load_demo
from gmrl.storage.repository import Repository
from gmrl.data.validation import validate_market_data


def main() -> None:
    data = load_demo()
    validate_market_data(data)
    with TemporaryDirectory() as directory:
        repository = Repository(Path(directory))
        dataset_id = repository.save_dataset(data)
        assert repository.load_dataset(dataset_id) == data
    print(
        f"PASS: SYNTHETIC SAMPLE {len(data.instruments)} listings, {len(data.bars)} bars; dataset={dataset_id}"
    )


if __name__ == "__main__":
    main()
