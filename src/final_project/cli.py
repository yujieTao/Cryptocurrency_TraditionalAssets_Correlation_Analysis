"""Console script for final_project."""
import final_project

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for final_project."""
    console.print("Replace this message by putting your code into "
               "final_project.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")


if __name__ == "__main__":
    app()
