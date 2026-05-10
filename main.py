from docxtpl import DocxTemplate
from pathlib import Path
import zipfile


def extract_template_variables(path: str | Path) -> set[str]:
    """Extracts all {{ jinja2 }} variables from a .docx file."""
    try:
        return DocxTemplate(path).get_undeclared_template_variables()
    except zipfile.BadZipFile:
        raise ValueError(f"Invalid file: {str(path)!r}")


def main():
    test_file = Path("template.docx")
    if test_file.exists():
        variables = extract_template_variables(test_file)
        print(f"Template variables: {variables}")

    else:
        print(
            f"Place {test_file.as_posix()!r} to test {extract_template_variables.__name__}() function"
        )


if __name__ == "__main__":
    main()
