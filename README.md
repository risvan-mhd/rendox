# Rendox

> ⚠️ Work in progress — not ready for use.

A CLI tool for rendering Jinja2-templated `.docx` files. Give it a template, get an input file. Fill in your values, get your document.

> 🧪 **Experimental branch:** `experimental/preprocessor`
> This branch makes rendox *use* an external preprocessor.
> The preprocessor itself is NOT in this repo.

## Experimental: Use external preprocessor

Requires the preprocessor to be installed separately.

## Installation

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone -b experimental/preprocessor https://github.com/risvan-mhd/rendox
cd rendox
uv tool install .
```

# TODO: add preprocessor installation instructions here



## How it works

```
template.docx  ──►  rendox gen  ──►  input.rendox.toml  ──►  (fill in values)  ──►  rendox render  ──►  (preprocessor)  ──►  output.docx
```

1. **`rendox gen <template>`** — takes a path to any `.docx` template and generates an `input.rendox.toml` stub with the template path and all variables found in the template
2. **Edit `input.rendox.toml`** — fill in your values
3. **`rendox render <input>`** — runs the external preprocessor to generate an updated input, then renders `output.docx`

> **Note:** The preprocessor only runs on `.rendox.toml` files. Passing a standard `.toml` file skips the preprocessor and renders directly.



## Usage

```bash
# Step 1: generate an input file from a template
rendox gen ~/templates/contract.docx
# → writes input.rendox.toml in the current directory

rendox gen ~/templates/contract.docx --output ~/inputs/contract.rendox.toml
# → write to a specific path

# Step 2: fill in your values in input.rendox.toml

# Step 3: render the final document
rendox render input.rendox.toml
# → reads template path and values from input.rendox.toml, writes output.docx

rendox render ~/inputs/contract.rendox.toml --output filled-contract.docx
# → custom input and output paths

rendox render ~/inputs/contract.toml --output filled-contract.docx
# → skips preprocessor for standard .toml files and renders directly
```

## Template syntax

Rendox templates are standard `.docx` files using [Jinja2](https://jinja.palletsprojects.com/) variable syntax.

```
Dear {{ name }},

Your invoice total is {{ total }} due on {{ due_date | date }}.
```

## Generated input file

Running `rendox gen` on the above template produces:

```toml
[config]
template_path = "/home/user/templates/contract.docx"

[field]
name = ""
total = ""
due_date = ""
```

The `[config]` section is set automatically — you only need to fill in the values under `[field]`.

## Why Rendox?

Built out of personal need for a simple way to fill in `.docx` templates without writing code every time. If it's useful to you too, great.

## Contributing

Contributions welcome. Please open an issue before starting work on a large change.

## License

MIT
