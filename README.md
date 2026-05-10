# Rendox

> ⚠️ Work in progress — not ready for use.

A CLI tool for rendering Jinja2-templated `.docx` files. Give it a template, get an input file. Fill in your values, get your document.

## How it works

```
template.docx  ──►  rendox gen  ──►  input.toml  ──►  (fill in values)  ──►  rendox render  ──►  output.docx
```

1. **`rendox gen <template>`** — takes a path to any `.docx` template and generates an `input.toml` stub with the template path and all variables found in the template
2. **Edit `input.toml`** — fill in your values
3. **`rendox render <input>`** — reads the template path and values from the input file and renders the final document

## Installation

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/risvan-mhd/rendox
cd rendox
uv tool install .
```

## Usage

```bash
# Step 1: generate an input file from a template
rendox gen ~/templates/contract.docx
# → writes input.toml in the current directory

rendox gen ~/templates/contract.docx --output ~/inputs/contract.toml
# → write to a specific path

# Step 2: fill in your values in input.toml

# Step 3: render the final document
rendox render input.toml
# → reads template path and values from input.toml, writes output.docx

rendox render ~/inputs/contract.toml --output filled-contract.docx
# → custom input and output paths
```

## Template syntax

Rendox templates are standard `.docx` files using [Jinja2](https://jinja.palletsprojects.com/) variable syntax.

```
Dear {{ name }},

Your invoice total is {{ total }} due on {{ due_date | date }}.
```

Rendox adds a `date` filter for formatting date values. Defaults to `%d-%m-%Y`, accepts any `strftime` format string:

```
{{ due_date | date }}
{{ due_date | date("%B %d, %Y") }}
```

## Generated input file

Running `rendox gen` on the above template produces:

```toml
template = "/home/user/templates/contract.docx"

name = ""
total = ""
due_date = ""
```

The `template` field is set automatically — you only need to fill in the rest.

## Why Rendox?

Built out of personal need for a simple way to fill in `.docx` templates without writing code every time. If it's useful to you too, great.

## Contributing

Contributions welcome. Please open an issue before starting work on a large change.

## License

MIT
