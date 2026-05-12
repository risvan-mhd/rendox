import typer


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
def gen() -> None:
    """Generate a TOML input file from a .docx template."""
    raise NotImplementedError("Todo: gen()")


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
