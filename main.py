from pathlib import Path
import zipfile
import errno

from docxtpl import DocxTemplate
from tomlkit.items import Table
import tomlkit


def extract_template_variables(path: str | Path) -> set[str]:
    """Extracts all {{ jinja2 }} variables from a .docx file."""
    try:
        return DocxTemplate(path).get_undeclared_template_variables()
    except zipfile.BadZipFile:
        raise ValueError(f"Invalid file: {str(path)!r}")


def create_input_file(path: str | Path, template_path: str | Path) -> None:
    path = Path(path)
    template_path = Path(template_path)

    doc = tomlkit.document()
    variables = extract_template_variables(template_path)

    config_table = tomlkit.table(is_super_table=True)
    config_table.add("template_path", template_path.as_posix())
    doc.add("config", config_table)

    field_table = tomlkit.table(is_super_table=True)
    for var in variables:
        field_table.add(var, "")

    doc.add("field", field_table)

    with open(path, "w") as f:
        tomlkit.dump(doc, f)


def render_template(input_path: str | Path, output_path: str | Path) -> None:
    input_path = Path(input_path)
    with open(input_path, "r") as f:
        doc = tomlkit.load(f)

    config_table: Table | None = doc.get("config")
    if (
        not isinstance(config_table, Table)
        or "template_path" not in config_table
    ):
        raise ValueError(
            f"Invalid input file: {input_path.as_posix()!r} does not have a valid config table"
        )

    field_table: Table | None = doc.get("field")
    if not isinstance(field_table, Table):
        raise ValueError(
            f"Invalid input file: {input_path.as_posix()!r} does not have a field table"
        )

    template_path = Path(config_table["template_path"])
    if not template_path.exists():
        raise FileNotFoundError(
            errno.ENOENT, f"Template not found: {template_path.as_posix()!r}"
        )

    template = DocxTemplate(template_path)
    template.render(dict(field_table))
    template.save(output_path)


def main():
    input_file = Path("input.toml")
    output_file = Path("output.docx")

    if input_file.exists():
        render_template(input_file, output_file)
        print(
            f"Rendered {input_file.as_posix()!r} to {output_file.as_posix()!r}"
        )

    else:
        print(
            f"Generate {input_file.as_posix()!r} to test {render_template.__name__}() function"
        )


if __name__ == "__main__":
    main()
