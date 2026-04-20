"""CLI output helpers."""

from typing import List

from tasks.models import TaskResult


def print_banner() -> None:
    print("=" * 62)
    print("AI SETUP AGENT - Software install and configuration workflow")
    print("=" * 62)


def print_summary(results: List[TaskResult]) -> None:
    print("\n" + "=" * 62)
    print("RUN SUMMARY")
    print("=" * 62)
    ok_count = 0

    for result in results:
        icon = "OK" if result.success else "FAIL"
        print(f"[{icon}] {result.name} ({result.task_type})")
        print(f"      {result.message}")
        if result.success:
            ok_count += 1

    print("-" * 62)
    print(f"Completed: {ok_count}/{len(results)} successful")
    print("=" * 62)
