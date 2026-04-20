"""Manifest parser."""

import json
from pathlib import Path
from typing import List

from tasks.models import SetupTask


def load_manifest(path: Path) -> List[SetupTask]:
    content = json.loads(path.read_text(encoding="utf-8"))
    raw_tasks = content.get("tasks", [])
    tasks: List[SetupTask] = []

    for item in raw_tasks:
        tasks.append(
            SetupTask(
                name=item.get("name", ""),
                task_type=item.get("task_type", ""),
                description=item.get("description", ""),
                commands=item.get("commands", []),
                source=item.get("source", ""),
                destination=item.get("destination", ""),
                url=item.get("url", ""),
                notes=item.get("notes", ""),
                env=item.get("env", {}),
            )
        )

    return tasks
