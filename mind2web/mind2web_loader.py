"""
Mind2Web dataset loader.

Loads Mind2Web JSON files and converts to type-safe dataclasses.
"""

import json
from pathlib import Path
from typing import List, Union, Optional
from .mind2web_types import (
    Mind2WebDataset,
    Task,
    Action,
    Operation,
    Candidate
)


def load_candidate(candidate_dict: dict) -> Candidate:
    """
    Load Candidate from dictionary.

    Args:
        candidate_dict: Raw candidate dictionary from JSON

    Returns:
        Candidate dataclass instance
    """
    return Candidate(
        backend_node_id=str(candidate_dict['backend_node_id']),
        tag=candidate_dict['tag'],
        attributes=candidate_dict.get('attributes', ''),
        is_original_target=candidate_dict.get('is_original_target', False),
        is_top_level_target=candidate_dict.get('is_top_level_target', False)
    )


def load_operation(operation_dict: dict) -> Operation:
    """
    Load Operation from dictionary.

    Args:
        operation_dict: Raw operation dictionary from JSON

    Returns:
        Operation dataclass instance
    """
    return Operation(
        op=operation_dict['op'],
        value=operation_dict.get('value', ''),
        original_op=operation_dict.get('original_op', operation_dict['op'])
    )


def load_action(action_dict: dict) -> Action:
    """
    Load Action from dictionary.

    Args:
        action_dict: Raw action dictionary from JSON

    Returns:
        Action dataclass instance
    """
    # Load operation
    operation = load_operation(action_dict['operation'])

    # Load candidates
    pos_candidates = [
        load_candidate(c) for c in action_dict.get('pos_candidates', [])
    ]
    neg_candidates = [
        load_candidate(c) for c in action_dict.get('neg_candidates', [])
    ]

    return Action(
        action_uid=action_dict['action_uid'],
        raw_html=action_dict['raw_html'],
        cleaned_html=action_dict['cleaned_html'],
        operation=operation,
        pos_candidates=pos_candidates,
        neg_candidates=neg_candidates
    )


def load_task(task_dict: dict) -> Task:
    """
    Load Task from dictionary.

    Args:
        task_dict: Raw task dictionary from JSON

    Returns:
        Task dataclass instance
    """
    # Load actions
    actions = [load_action(a) for a in task_dict['actions']]

    return Task(
        annotation_id=task_dict['annotation_id'],
        website=task_dict['website'],
        domain=task_dict['domain'],
        subdomain=task_dict['subdomain'],
        confirmed_task=task_dict['confirmed_task'],
        action_reprs=task_dict.get('action_reprs', []),
        actions=actions
    )


def load_json_file(file_path: Union[str, Path]) -> Mind2WebDataset:
    """
    Load Mind2Web dataset from JSON file.

    Args:
        file_path: Path to JSON file (train_*.json, test_*.json, etc.)

    Returns:
        Mind2WebDataset with all tasks loaded

    Example:
        >>> dataset = load_json_file("../../Mind2Web-data/data/train/train_0.json")
        >>> print(dataset)
        Mind2WebDataset(split=train_0, 112 tasks, 891 actions)
    """
    file_path = Path(file_path)

    # Load JSON
    with open(file_path) as f:
        raw_data = json.load(f)

    # Parse tasks
    tasks = [load_task(task_dict) for task_dict in raw_data]

    # Infer split name from filename
    split_name = file_path.stem  # e.g., "train_0", "test_task_1"

    return Mind2WebDataset(tasks=tasks, split=split_name)


def load_multiple_files(file_paths: List[Union[str, Path]], split_name: Optional[str] = None) -> Mind2WebDataset:
    """
    Load and combine multiple Mind2Web JSON files.

    Args:
        file_paths: List of paths to JSON files
        split_name: Optional name for combined dataset (defaults to "combined")

    Returns:
        Mind2WebDataset with all tasks from all files

    Example:
        >>> files = ["train_0.json", "train_1.json"]
        >>> dataset = load_multiple_files(files, split_name="train")
        >>> print(dataset)
        Mind2WebDataset(split=train, 224 tasks, 1782 actions)
    """
    all_tasks = []

    for file_path in file_paths:
        dataset = load_json_file(file_path)
        all_tasks.extend(dataset.tasks)

    if split_name is None:
        split_name = "combined"

    return Mind2WebDataset(tasks=all_tasks, split=split_name)


def load_train_split(data_dir: Union[str, Path], max_files: Optional[int] = None) -> Mind2WebDataset:
    """
    Load all training files from Mind2Web data directory.

    Args:
        data_dir: Path to Mind2Web data directory (contains train/ subdirectory)
        max_files: Maximum number of files to load (None = all files)

    Returns:
        Mind2WebDataset with all training tasks

    Example:
        >>> dataset = load_train_split("../../Mind2Web-data/data")
        >>> print(dataset)
        Mind2WebDataset(split=train, 1009 tasks, 8141 actions)
    """
    data_dir = Path(data_dir)
    train_dir = data_dir / "train"

    if not train_dir.exists():
        raise FileNotFoundError(f"Train directory not found: {train_dir}")

    # Find all train_*.json files
    train_files = sorted(train_dir.glob("train_*.json"))

    if not train_files:
        raise FileNotFoundError(f"No train_*.json files found in {train_dir}")

    # Limit files if requested
    if max_files is not None:
        train_files = train_files[:max_files]

    return load_multiple_files(train_files, split_name="train")


def load_test_split(
    data_dir: Union[str, Path],
    split_type: str = "task",
    max_files: Optional[int] = None
) -> Mind2WebDataset:
    """
    Load test split from Mind2Web data directory.

    Args:
        data_dir: Path to Mind2Web data directory
        split_type: Test split type ("task", "website", or "domain")
        max_files: Maximum number of files to load (None = all files)

    Returns:
        Mind2WebDataset with test tasks

    Example:
        >>> dataset = load_test_split("../../Mind2Web-data/data", split_type="website")
        >>> print(dataset)
        Mind2WebDataset(split=test_website, 177 tasks, ...)
    """
    data_dir = Path(data_dir)
    test_dir = data_dir / f"test_{split_type}"

    if not test_dir.exists():
        raise FileNotFoundError(f"Test directory not found: {test_dir}")

    # Find all test files
    test_files = sorted(test_dir.glob(f"test_{split_type}_*.json"))

    if not test_files:
        raise FileNotFoundError(f"No test_{split_type}_*.json files found in {test_dir}")

    # Limit files if requested
    if max_files is not None:
        test_files = test_files[:max_files]

    return load_multiple_files(test_files, split_name=f"test_{split_type}")
