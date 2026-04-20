"""Data models for setup tasks."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SetupTask:
    name: str
    task_type: str
    description: str
    commands: List[str] = field(default_factory=list)
    source: str = ""
    destination: str = ""
    url: str = ""
    notes: str = ""
    env: Dict[str, str] = field(default_factory=dict)


@dataclass
class TaskResult:
    name: str
    task_type: str
    success: bool
    message: str
