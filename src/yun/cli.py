import sys
from pathlib import Path
from typing import Annotated

from cyclopts import App, Parameter

from yun.pprint import PrettyPrinter

app = App()
pprint = PrettyPrinter()


@app.command
def init(root_dir: Annotated[Path, Parameter(name="root", help="The project root directory.")] = Path.cwd()):  # noqa: B008
    """Initialize .env and settings.yaml, and the input directory."""
    input_dir = root_dir / "input"
    init_files = [".env", "settings.yaml"]

    conflicts = []
    if input_dir.exists():
        conflicts.append(f"Directory already exists: {input_dir}")
    for init_file in init_files:
        if (root_dir / init_file).exists():
            conflicts.append(f"File already exists: {root_dir / init_file}")

    if conflicts:
        pprint.error(
            "Initialization failed",
            conflicts,
        )
        sys.exit(1)

    input_dir.mkdir(parents=True)
    for init_file in init_files:
        (root_dir / init_file).touch(exist_ok=False)

    pprint.success("Created successfully")


@app.command
def index():
    pass


@app.command
def query():
    pass


@app.command
def serve():
    pass


@app.default
def main():
    pass


if __name__ == "__main__":
    app()
