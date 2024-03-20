import os
import subprocess


def run_command(command):
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()


git_version = run_command("git rev-list --count HEAD")
git_diff = run_command("git diff --name-only HEAD")
is_dirty = '1' if git_diff else '0'
commit_hash = run_command("git rev-parse HEAD")[:6]

version_info = f"""
'1.0.{git_version}.{is_dirty}' - {commit_hash};
"""

file_path = "version_info.txt"

with open(file_path, "w") as file:
    file.write(version_info.strip())
