from typing import Annotated
from pathlib import Path

import typer
import rich

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
) -> None:
    """Generate a TOML input file from a .docx template."""
    if template.suffix.lower() != ".docx":
        typer.secho(
            "Error: expected a .docx template file",
            err=True,
            fg=typer.colors.RED,
        )
        rich.print(
            f"Path: [link=file://{template.resolve()}]{template.as_posix()}[/link]"
        )
        raise typer.Exit(code=1)

    fields = extract_template_variables(template)
    rich.print(f"Found [green]{len(fields)}[/green] fields:")
    for field in fields:
        rich.print(f"    [dim]-[/dim] {field}")

    print()

    create_input_file(output, template)
    rich.print(
        f"[green]✓ Generated [link=file://{output.resolve()}]{output.as_posix()}[/link][/green]",
        end="\n\n",
    )

    typer.echo("Next:")
    typer.echo("    Edit input.toml and run:")
    typer.echo("    rendox render input.toml")


@app.command()
def render() -> None:
    """Render a .docx document using a input file."""
    raise NotImplementedError("Todo: render()")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
