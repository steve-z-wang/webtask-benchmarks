"""Mind2Web evaluation package."""

from .mind2web_types import (
    Operation,
    Candidate,
    Action,
    Task,
    Mind2WebDataset,
)

from .mind2web_loader import (
    load_json_file,
    load_multiple_files,
    load_train_split,
    load_test_split,
)

__all__ = [
    # Types
    "Operation",
    "Candidate",
    "Action",
    "Task",
    "Mind2WebDataset",
    # Loaders
    "load_json_file",
    "load_multiple_files",
    "load_train_split",
    "load_test_split",
]
