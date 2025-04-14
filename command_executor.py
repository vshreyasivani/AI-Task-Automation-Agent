import subprocess
import click
import os
from typing import List, Tuple

class CommandExecutor:
    @staticmethod
    def execute_commands(commands: List[str]) -> Tuple[bool, str]:
        """Execute a list of shell commands with working directory tracking."""
        current_dir = "."  # Start from current directory

        for cmd in commands:
            click.echo(f"Executing: {cmd}")

            # Split chained commands (e.g., cd dir && touch file)
            parts = [part.strip() for part in cmd.split("&&")]

            for part in parts:
                if part.startswith("cd "):
                    new_dir = part.split("cd ", 1)[1].strip()
                    current_dir = os.path.normpath(os.path.join(current_dir, new_dir))
                    click.echo(f"Changed working directory to: {current_dir}")
                    continue

                try:
                    result = subprocess.run(
                        part,
                        shell=True,
                        check=True,
                        text=True,
                        capture_output=True,
                        cwd=current_dir
                    )
                    click.echo(result.stdout)
                except subprocess.CalledProcessError as e:
                    click.echo(f"Error executing command: {e.stderr}")
                    return False, e.stderr

        return True, "All commands executed successfully"
