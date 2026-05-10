from docxtpl import DocxTemplate
from pathlib import Path
import zipfile
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


def main():
    template_file = Path("template.docx")
    input_file = Path("input.toml")
    if template_file.exists():
        create_input_file(input_file, template_file)
        print(
            f"Input file created at {input_file.as_posix()!r} from template {template_file.as_posix()!r}"
        )

    else:
        print(
            f"Place {template_file.as_posix()!r} to test {create_input_file.__name__}() function"
        )


if __name__ == "__main__":
    main()
