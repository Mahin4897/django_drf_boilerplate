# Django Project Setup Guide

This repository contains a Django project.
Follow the steps below to set up the project locally using [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just).

## Prerequisites

- Python 3.9+
- Git (optional)

## Install uv

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check version:

```bash
uv --version
```

## Install Just

Install via uv tool:

```bash
uv tool install rust-just
```

Check version:

```bash
just --version
```

## Set Up the Project

### Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### Create Virtual Environment and Install Dependencies

```bash
uv sync
```

`uv sync` automatically creates a `.venv` and installs all dependencies from `pyproject.toml` / `uv.lock`.

## Justfile Commands

| Command | Description |
| --- | --- |
| `just dev` | Run the development server |
| `just dev0` | Run on all interfaces at port 8000 |
| `just migrate` | Apply migrations |
| `just makemigrations` | Make migrations |
| `just superuser` | Create a superuser |
| `just shell` | Open the Django shell |
| `just test` | Run tests |
| `just app <name>` | Create a new Django app |

## Justfile Reference

```just
dev:
    uv run python manage.py runserver

dev0:
    uv run python manage.py runserver 0.0.0.0:8000

migrate:
    uv run python manage.py migrate

makemigrations:
    uv run python manage.py makemigrations

superuser:
    uv run python manage.py createsuperuser

shell:
    uv run python manage.py shell

test:
    uv run python manage.py test

app name:
    uv run python manage.py startapp {{ name }}
```

## Open the App

<http://127.0.0.1:8000/>

## Add Dependencies

```bash
uv add <package-name>
```

## License

MIT License
