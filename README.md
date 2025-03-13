# capstone
Udacity final project

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r apps/backend/requirements.txt`
3. Install development dependencies: `pip install -r apps/backend/requirements-dev.txt`
4. Install pre-commit hooks: `pre-commit install`
5. Run the application: `cd apps/backend && flask run`

## Code Quality Tools

This project uses several code quality tools to ensure consistent code style and catch potential issues:

### Black

[Black](https://black.readthedocs.io/) is an uncompromising code formatter that ensures consistent code style.

To run Black manually:

```bash
black apps/backend
```

### isort

[isort](https://pycqa.github.io/isort/) sorts imports alphabetically and automatically separates them into sections.

To run isort manually:

```bash
isort apps/backend
```

### Flake8

[Flake8](https://flake8.pycqa.org/) is a code linter that checks for style and potential errors.

To run Flake8 manually:

```bash
flake8 apps/backend
```

### MyPy

[MyPy](https://mypy.readthedocs.io/) is a static type checker for Python.

To run MyPy manually:

```bash
mypy apps/backend
```

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run code quality checks before each commit.

To install pre-commit hooks:

```bash
pre-commit install
```

Now, the code quality checks will run automatically before each commit.

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow runs the code quality checks on each push and pull request.

## Database Seeding

To populate the database with sample data:

```bash
cd apps/backend
python seed_db.py
```

This will create sample actors, movies, and relationships between them.
