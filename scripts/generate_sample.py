"""Generate optional local artifact without contacting any service."""

from pathlib import Path
from gmrl.providers.sample import load_demo
from gmrl.storage.repository import Repository

if __name__ == "__main__":
    print(Repository(Path(".runtime")).save_dataset(load_demo()))
