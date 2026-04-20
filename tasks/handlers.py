"""Task handlers for different setup task types."""

import shutil
from pathlib import Path

from tasks.command_runner import run_powershell
from tasks.models import SetupTask, TaskResult
from utils.logger import setup_logger

logger = setup_logger("task-handler")


class TaskHandler:
    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run

    async def execute(self, task: SetupTask) -> TaskResult:
        try:
            if task.task_type == "click_install":
                return await self._run_click_install(task)
            if task.task_type == "cli_install":
                return await self._run_cli_install(task)
            if task.task_type == "cli_setup":
                return await self._run_cli_setup(task)
            if task.task_type == "copy_files":
                return await self._run_copy_files(task)
            if task.task_type == "system_config":
                return await self._run_system_config(task)

            return TaskResult(task.name, task.task_type, False, "Unknown task type.")
        except Exception as exc:  # pylint: disable=broad-except
            return TaskResult(task.name, task.task_type, False, f"Exception: {exc}")

    async def _run_click_install(self, task: SetupTask) -> TaskResult:
        print(f"\n[CLICK INSTALL] {task.name}")
        print(f"- {task.description}")
        if task.url:
            print(f"- Open installer page: {task.url}")
        if task.notes:
            print(f"- Notes: {task.notes}")

        if self.dry_run:
            return TaskResult(task.name, task.task_type, True, "Dry-run completed.")

        for cmd in task.commands:
            code, output = await run_powershell(cmd, task.env)
            if code != 0:
                return TaskResult(task.name, task.task_type, False, output)
        return TaskResult(task.name, task.task_type, True, "Click install task done.")

    async def _run_cli_install(self, task: SetupTask) -> TaskResult:
        print(f"\n[CLI INSTALL] {task.name}")
        print(f"- {task.description}")
        return await self._run_commands(task)

    async def _run_cli_setup(self, task: SetupTask) -> TaskResult:
        print(f"\n[CLI SETUP] {task.name}")
        print(f"- {task.description}")
        return await self._run_commands(task)

    async def _run_system_config(self, task: SetupTask) -> TaskResult:
        print(f"\n[SYSTEM CONFIG] {task.name}")
        print(f"- {task.description}")
        return await self._run_commands(task)

    async def _run_copy_files(self, task: SetupTask) -> TaskResult:
        print(f"\n[COPY FILES] {task.name}")
        print(f"- {task.description}")

        src = Path(task.source)
        dst = Path(task.destination)
        if self.dry_run:
            return TaskResult(
                task.name,
                task.task_type,
                True,
                f"Dry-run copy: {src} -> {dst}",
            )

        if not src.exists():
            return TaskResult(task.name, task.task_type, False, f"Source missing: {src}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return TaskResult(task.name, task.task_type, True, f"Copied {src} -> {dst}")

    async def _run_commands(self, task: SetupTask) -> TaskResult:
        if self.dry_run:
            for cmd in task.commands:
                print(f"  [dry-run] {cmd}")
            return TaskResult(task.name, task.task_type, True, "Dry-run completed.")

        for cmd in task.commands:
            logger.info("Executing command: %s", cmd)
            code, output = await run_powershell(cmd, task.env)
            if output:
                print(f"  {output}")
            if code != 0:
                return TaskResult(task.name, task.task_type, False, f"Failed command: {cmd}")

        return TaskResult(task.name, task.task_type, True, "Completed.")
