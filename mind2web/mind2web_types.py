"""
Mind2Web dataset dataclasses.

Type-safe representations of Mind2Web data structures with helper methods.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
import json


@dataclass
class Operation:
    """
    Action operation to perform on an element.

    Attributes:
        op: Operation type (CLICK, TYPE, SELECT)
        value: Optional value (for TYPE/SELECT operations)
        original_op: Original operation from annotation (may include HOVER, ENTER)
    """
    op: Literal["CLICK", "TYPE", "SELECT"]
    value: str
    original_op: str

    @property
    def is_click(self) -> bool:
        """Check if this is a CLICK operation."""
        return self.op == "CLICK"

    @property
    def is_type(self) -> bool:
        """Check if this is a TYPE operation."""
        return self.op == "TYPE"

    @property
    def is_select(self) -> bool:
        """Check if this is a SELECT operation."""
        return self.op == "SELECT"

    @property
    def has_value(self) -> bool:
        """Check if operation has a value."""
        return bool(self.value and self.value.strip())

    def __str__(self) -> str:
        if self.has_value:
            return f"{self.op}: {self.value}"
        return self.op


@dataclass
class Candidate:
    """
    Element candidate (positive = ground truth, negative = distractor).

    Attributes:
        backend_node_id: Unique element ID from CDP
        tag: HTML tag name
        attributes: Element attributes as JSON string
        is_original_target: Whether this was the annotator's original target
        is_top_level_target: Whether this is a top-level target (see Mind2Web paper)
    """
    backend_node_id: str
    tag: str
    attributes: str  # JSON string
    is_original_target: bool
    is_top_level_target: bool

    @property
    def attributes_dict(self) -> Dict[str, str]:
        """Parse attributes JSON string to dictionary."""
        if not self.attributes:
            return {}
        try:
            return json.loads(self.attributes)
        except json.JSONDecodeError:
            return {}

    @property
    def is_clickable(self) -> bool:
        """Check if element is marked as clickable."""
        attrs = self.attributes_dict
        return attrs.get('is_clickable') == 'true'

    @property
    def bounding_box(self) -> Optional[tuple]:
        """Get bounding box as (x, y, width, height) or None."""
        attrs = self.attributes_dict
        bbox_str = attrs.get('bounding_box_rect', '')
        if not bbox_str:
            return None
        try:
            parts = bbox_str.split(',')
            if len(parts) >= 4:
                return tuple(float(p) for p in parts[:4])
        except ValueError:
            pass
        return None

    def __str__(self) -> str:
        return f"<{self.tag} backend_node_id={self.backend_node_id}>"


@dataclass
class Action:
    """
    Single action step in a task.

    Attributes:
        action_uid: Unique action ID
        raw_html: Complete HTML before action
        cleaned_html: Cleaned/filtered HTML before action
        operation: Operation to perform
        pos_candidates: Positive (ground truth) element candidates
        neg_candidates: Negative (distractor) element candidates
    """
    action_uid: str
    raw_html: str
    cleaned_html: str
    operation: Operation
    pos_candidates: List[Candidate]
    neg_candidates: List[Candidate]

    @property
    def has_ground_truth(self) -> bool:
        """Check if action has at least one positive candidate."""
        return len(self.pos_candidates) > 0

    @property
    def ground_truth_ids(self) -> List[str]:
        """Get all ground truth backend_node_ids."""
        return [c.backend_node_id for c in self.pos_candidates]

    @property
    def primary_ground_truth(self) -> Optional[Candidate]:
        """Get the primary ground truth (original target if available)."""
        # Prefer original target
        for candidate in self.pos_candidates:
            if candidate.is_original_target:
                return candidate
        # Fallback to first positive candidate
        return self.pos_candidates[0] if self.pos_candidates else None

    @property
    def num_candidates(self) -> int:
        """Total number of candidates (pos + neg)."""
        return len(self.pos_candidates) + len(self.neg_candidates)

    @property
    def all_candidate_ids(self) -> List[str]:
        """Get all candidate backend_node_ids (pos + neg)."""
        return (
            [c.backend_node_id for c in self.pos_candidates] +
            [c.backend_node_id for c in self.neg_candidates]
        )

    def __str__(self) -> str:
        gt = f" (gt={self.primary_ground_truth.backend_node_id})" if self.primary_ground_truth else " (no gt)"
        return f"Action({self.operation}{gt}, {self.num_candidates} candidates)"


@dataclass
class Task:
    """
    Complete task with multiple action steps.

    Attributes:
        annotation_id: Unique task ID
        website: Website name
        domain: Website domain category
        subdomain: Website subdomain category
        confirmed_task: Natural language task description
        action_reprs: Human-readable action sequence
        actions: List of action steps
    """
    annotation_id: str
    website: str
    domain: str
    subdomain: str
    confirmed_task: str
    action_reprs: List[str]
    actions: List[Action]

    @property
    def num_actions(self) -> int:
        """Number of action steps in task."""
        return len(self.actions)

    @property
    def num_actions_with_ground_truth(self) -> int:
        """Number of actions that have ground truth."""
        return sum(1 for action in self.actions if action.has_ground_truth)

    @property
    def operation_types(self) -> List[str]:
        """Get list of operation types for all actions."""
        return [action.operation.op for action in self.actions]

    @property
    def operation_counts(self) -> Dict[str, int]:
        """Count operations by type."""
        counts = {"CLICK": 0, "TYPE": 0, "SELECT": 0}
        for action in self.actions:
            counts[action.operation.op] = counts.get(action.operation.op, 0) + 1
        return counts

    def get_action(self, action_uid: str) -> Optional[Action]:
        """Get action by UID."""
        for action in self.actions:
            if action.action_uid == action_uid:
                return action
        return None

    def get_action_at_index(self, index: int) -> Optional[Action]:
        """Get action by index (0-based)."""
        if 0 <= index < len(self.actions):
            return self.actions[index]
        return None

    def get_previous_actions(self, action_index: int, max_k: int = 5) -> List[str]:
        """
        Get previous action representations for context.

        Args:
            action_index: Current action index (0-based)
            max_k: Maximum number of previous actions to return

        Returns:
            List of previous action representations (most recent last)
        """
        if action_index <= 0:
            return []
        start = max(0, action_index - max_k)
        return self.action_reprs[start:action_index]

    def __str__(self) -> str:
        return f"Task(id={self.annotation_id[:8]}..., task=\"{self.confirmed_task[:50]}...\", {self.num_actions} actions)"


@dataclass
class Mind2WebDataset:
    """
    Collection of Mind2Web tasks.

    Attributes:
        tasks: List of tasks
        split: Dataset split name (e.g., "train", "test_task", "test_website", "test_domain")
    """
    tasks: List[Task]
    split: str = "unknown"

    @property
    def num_tasks(self) -> int:
        """Number of tasks in dataset."""
        return len(self.tasks)

    @property
    def num_actions(self) -> int:
        """Total number of actions across all tasks."""
        return sum(task.num_actions for task in self.tasks)

    @property
    def num_actions_with_ground_truth(self) -> int:
        """Total number of actions with ground truth."""
        return sum(task.num_actions_with_ground_truth for task in self.tasks)

    @property
    def operation_counts(self) -> Dict[str, int]:
        """Count operations across all tasks."""
        total_counts = {"CLICK": 0, "TYPE": 0, "SELECT": 0}
        for task in self.tasks:
            task_counts = task.operation_counts
            for op, count in task_counts.items():
                total_counts[op] = total_counts.get(op, 0) + count
        return total_counts

    @property
    def websites(self) -> List[str]:
        """Get unique website names."""
        return list(set(task.website for task in self.tasks))

    @property
    def domains(self) -> List[str]:
        """Get unique domain categories."""
        return list(set(task.domain for task in self.tasks))

    def get_task(self, annotation_id: str) -> Optional[Task]:
        """Get task by annotation ID."""
        for task in self.tasks:
            if task.annotation_id == annotation_id:
                return task
        return None

    def filter_by_website(self, website: str) -> 'Mind2WebDataset':
        """Create new dataset with tasks from specific website."""
        filtered_tasks = [t for t in self.tasks if t.website == website]
        return Mind2WebDataset(tasks=filtered_tasks, split=f"{self.split}__{website}")

    def filter_by_domain(self, domain: str) -> 'Mind2WebDataset':
        """Create new dataset with tasks from specific domain."""
        filtered_tasks = [t for t in self.tasks if t.domain == domain]
        return Mind2WebDataset(tasks=filtered_tasks, split=f"{self.split}__{domain}")

    def sample(self, n: int, seed: Optional[int] = None) -> 'Mind2WebDataset':
        """Sample n tasks randomly."""
        import random
        if seed is not None:
            random.seed(seed)
        sampled = random.sample(self.tasks, min(n, len(self.tasks)))
        return Mind2WebDataset(tasks=sampled, split=f"{self.split}__sample{n}")

    def __str__(self) -> str:
        return (
            f"Mind2WebDataset(split={self.split}, "
            f"{self.num_tasks} tasks, "
            f"{self.num_actions} actions, "
            f"ops={self.operation_counts})"
        )

    def __repr__(self) -> str:
        return str(self)
