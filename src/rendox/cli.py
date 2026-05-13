from typing import Annotated
from pathlib import Path

from rich.console import Console
import typer

from core import create_input_file, extract_template_variables


app = typer.Typer(
    name="Rendox",
    help="""
Render Jinja2-templated .docx files.

Workflow:

1. Generate an input file
   rendox gen template.docx

2. Fill in values in input.toml

3. Render document
   rendox render input.toml
""",
    rich_markup_mode="rich",
)
console = Console()
err_console = Console(stderr=True)


def format_path(path: Path) -> str:
    return f"[link=file://{path.resolve()}]{path.as_posix()}[/link]"


def print_err(msg: str) -> None:
    err_console.print(f"[red][bold]Error: [/bold]{msg}[/red]")


@app.command()
def gen(
    template: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to a .docx template",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Path for the generated TOML file",
        ),
    ] = Path("input.toml"),
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force overwrite output file if exists without prompting",
        ),
    ] = False,
) -> None:
    """Generate a TOML input file from a .docx template."""
    if template.suffix.lower() != ".docx":
        print_err("expected a .docx template file")
        console.print(f"Path: {format_path(template)}")
        raise typer.Exit(1)

    if output.exists():
        if not output.is_file():
            print_err("output path exists and path is not a file")
            console.print(f"Path: {format_path(output)}")
            raise typer.Exit(1)

        if not force:
            typer.confirm(
                f"File {output.as_posix()!r} exists. Overwrite?",
                abort=True,
            )

    fields = extract_template_variables(template)
    console.print(f"Found [green]{len(fields)}[/green] fields:")
    for field in fields:
        console.print(f"    [dim]-[/dim] {field}")

    console.print()

    create_input_file(output, template)
    console.print(
        f"[green]✓ Generated {format_path(output)}[/green]",
        end="\n\n",
    )

    console.print("Next:")
    console.print("    Edit input.toml and run:")
    console.print("    rendox render input.toml")


@app.command()
def render() -> None:
    """Render a .docx document using a input file."""
    raise NotImplementedError("Todo: render()")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
