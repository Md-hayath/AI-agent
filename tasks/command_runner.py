"""Command execution helper."""

import asyncio
import os
import subprocess
from typing import Dict, Tuple


async def run_powershell(command: str, extra_env: Dict[str, str]) -> Tuple[int, str]:
    env = os.environ.copy()
    env.update(extra_env)

    process = await asyncio.create_subprocess_exec(
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    stdout, _ = await process.communicate()
    output = (stdout or b"").decode("utf-8", errors="replace").strip()
    return process.returncode, output
