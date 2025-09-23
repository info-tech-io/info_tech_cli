---
title: "Contributing"
description: "Contributing guidelines for Info-Tech CLI - development setup, coding standards, and contribution process"
date: 2024-09-23
draft: false
weight: 5
---

# Contributing to Info-Tech CLI

We welcome contributions to the Info-Tech CLI project! This guide will help you get started with development and understand our contribution process.

## Getting Started

### Development Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/info-tech-io/info-tech-cli.git
   cd info-tech-cli
   ```

2. **Set up Python environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   pip install -r requirements-dev.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   export GITHUB_TOKEN=your_github_token_here
   ```

4. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

5. **Verify installation:**
   ```bash
   info_tech_cli --version
   info_tech_cli --help
   ```

### Development Dependencies

The `requirements-dev.txt` includes:
```
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.991
pre-commit>=2.20.0
click-testing>=0.4.0
responses>=0.22.0
```

## Project Structure

### Code Organization

```
info-tech-cli/
├── info_tech_cli/          # Main package
│   ├── __init__.py         # Package metadata
│   ├── cli.py              # Main CLI interface
│   ├── commands/           # Command implementations
│   │   ├── __init__.py
│   │   ├── create.py       # Create command
│   │   ├── delete.py       # Delete command
│   │   └── validate.py     # Validate command
│   ├── utils/              # Shared utilities
│   │   ├── __init__.py
│   │   ├── github.py       # GitHub integration
│   │   ├── templates.py    # Template processing
│   │   └── validation.py   # Validation logic
│   ├── templates/          # Built-in templates
│   │   ├── module-basic/
│   │   ├── module-programming/
│   │   └── module-documentation/
│   └── config/             # Configuration management
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_cli.py         # CLI interface tests
│   ├── test_commands/      # Command-specific tests
│   ├── test_utils/         # Utility tests
│   └── fixtures/           # Test fixtures
├── docs/                   # Documentation
├── .github/                # GitHub workflows
├── setup.py                # Package setup
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md
```

### Design Principles

1. **Modularity** - Separate concerns into focused modules
2. **Testability** - Write testable code with dependency injection
3. **Usability** - Provide clear error messages and helpful defaults
4. **Extensibility** - Design for plugins and custom templates
5. **Performance** - Optimize for common use cases

## Development Workflow

### Code Standards

**Python Style:**
- Follow PEP 8 guidelines
- Use Black for automatic formatting
- Maximum line length: 88 characters
- Use type hints for all public APIs

**Example:**
```python
from typing import Optional, Dict, Any, List
import click
from pathlib import Path

def create_module(
    module_name: str,
    template: str = "module-basic",
    variables: Optional[Dict[str, Any]] = None
) -> Path:
    """Create a new learning module from template.

    Args:
        module_name: Name of the module to create (kebab-case)
        template: Template name to use for creation
        variables: Template variables for substitution

    Returns:
        Path to the created module directory

    Raises:
        ValueError: If module_name is invalid
        FileExistsError: If module already exists
        TemplateNotFoundError: If template doesn't exist
    """
    if not _validate_module_name(module_name):
        raise ValueError(f"Invalid module name: {module_name}")

    output_path = Path.cwd() / module_name
    if output_path.exists():
        raise FileExistsError(f"Module '{module_name}' already exists")

    # Implementation details...
    return output_path

def _validate_module_name(name: str) -> bool:
    """Validate module name follows kebab-case convention."""
    import re
    return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))
```

### Pre-commit Hooks

Set up pre-commit hooks for code quality:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-click]

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: [--profile=black]
```

Install hooks:
```bash
pre-commit install
```

## Testing

### Test Structure

**Unit Tests:**
```python
# tests/test_commands/test_create.py
import pytest
from unittest.mock import Mock, patch
from click.testing import CliRunner
from info_tech_cli.cli import cli
from info_tech_cli.commands.create import create_module

class TestCreateCommand:
    """Test suite for create command."""

    def test_create_basic_module(self, tmp_path):
        """Test basic module creation."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cli, ['create', 'test-module'])

            assert result.exit_code == 0
            assert 'Module \'test-module\' created successfully' in result.output
            assert Path('test-module').exists()
            assert Path('test-module/module.json').exists()

    def test_create_with_template(self, tmp_path):
        """Test module creation with specific template."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'create', 'python-course',
                '--template', 'module-programming',
                '--category', 'programming',
                '--difficulty', 'intermediate'
            ])

            assert result.exit_code == 0

            # Verify module structure
            module_path = Path('python-course')
            assert module_path.exists()
            assert (module_path / 'content' / 'index.md').exists()
            assert (module_path / 'quizzes').exists()

    def test_create_existing_module_fails(self, tmp_path):
        """Test that creating existing module fails."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Create module first time
            result1 = runner.invoke(cli, ['create', 'existing-module'])
            assert result1.exit_code == 0

            # Try to create again
            result2 = runner.invoke(cli, ['create', 'existing-module'])
            assert result2.exit_code != 0
            assert 'already exists' in result2.output

    @patch('info_tech_cli.utils.github.GitHubIntegration')
    def test_create_with_github_integration(self, mock_github, tmp_path):
        """Test module creation with GitHub integration."""
        mock_github_instance = Mock()
        mock_github.return_value = mock_github_instance

        runner = CliRunner()

        with runner.isolated_filesystem():
            with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}):
                result = runner.invoke(cli, ['create', 'github-module'])

                assert result.exit_code == 0
                mock_github_instance.create_repository.assert_called_once()

    def test_invalid_module_name(self):
        """Test validation of invalid module names."""
        runner = CliRunner()

        invalid_names = [
            'Invalid_Name',    # Underscores not allowed
            'invalid.name',    # Dots not allowed
            'InvalidName',     # CamelCase not allowed
            'invalid name',    # Spaces not allowed
            '123invalid',      # Cannot start with number
            ''                 # Empty name
        ]

        for invalid_name in invalid_names:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, ['create', invalid_name])
                assert result.exit_code != 0
                assert 'Invalid module name' in result.output
```

**Integration Tests:**
```python
# tests/test_integration.py
import tempfile
import json
from pathlib import Path
from info_tech_cli.utils.templates import TemplateProcessor
from info_tech_cli.utils.validation import ModuleValidator

class TestFullWorkflow:
    """Integration tests for complete workflows."""

    def test_create_validate_workflow(self):
        """Test complete create and validate workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create module using template processor
            processor = TemplateProcessor('module-basic')
            variables = {
                'module_name': 'integration-test',
                'category': 'programming',
                'difficulty': 'beginner',
                'language': 'en',
                'author': 'Test Author',
                'date': '2024-09-23'
            }

            module_path = processor.create_module('integration-test', variables)

            # Validate created module
            validator = ModuleValidator(module_path)
            is_valid, errors, warnings = validator.validate()

            assert is_valid, f"Validation failed: {errors}"
            assert len(errors) == 0

            # Verify content
            assert (module_path / 'module.json').exists()
            assert (module_path / 'content' / 'index.md').exists()

            # Check metadata
            with open(module_path / 'module.json') as f:
                metadata = json.load(f)

            assert metadata['name'] == 'integration-test'
            assert metadata['category'] == 'programming'
            assert metadata['difficulty'] == 'beginner'

    def test_template_processing(self):
        """Test template variable processing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test all built-in templates
            templates = ['module-basic', 'module-programming', 'module-documentation']

            for template_name in templates:
                processor = TemplateProcessor(template_name)
                variables = {
                    'module_name': f'test-{template_name}',
                    'category': 'programming',
                    'difficulty': 'intermediate',
                    'language': 'en'
                }

                module_path = processor.create_module(f'test-{template_name}', variables)

                # Basic validation
                assert module_path.exists()
                assert (module_path / 'module.json').exists()
```

**Mock Tests:**
```python
# tests/test_utils/test_github.py
import pytest
import responses
from info_tech_cli.utils.github import GitHubIntegration

class TestGitHubIntegration:
    """Test GitHub API integration."""

    @responses.activate
    def test_create_repository_success(self):
        """Test successful repository creation."""
        # Mock GitHub API response
        responses.add(
            responses.POST,
            'https://api.github.com/user/repos',
            json={
                'name': 'test-repo',
                'clone_url': 'https://github.com/user/test-repo.git',
                'html_url': 'https://github.com/user/test-repo'
            },
            status=201
        )

        github = GitHubIntegration()

        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}):
            with tempfile.TemporaryDirectory() as temp_dir:
                repo_info = github.create_repository('test-repo', Path(temp_dir))

                assert repo_info['name'] == 'test-repo'
                assert 'clone_url' in repo_info

    @responses.activate
    def test_create_repository_failure(self):
        """Test repository creation failure."""
        responses.add(
            responses.POST,
            'https://api.github.com/user/repos',
            json={'message': 'Repository already exists'},
            status=422
        )

        github = GitHubIntegration()

        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}):
            with pytest.raises(requests.HTTPError):
                github.create_repository('existing-repo', Path('/tmp'))
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=info_tech_cli --cov-report=html

# Run specific test file
python -m pytest tests/test_commands/test_create.py

# Run with verbose output
python -m pytest -v

# Run only unit tests
python -m pytest tests/test_commands/ tests/test_utils/

# Run only integration tests
python -m pytest tests/test_integration.py
```

## Feature Development

### Adding New Commands

1. **Create command module:**
   ```python
   # info_tech_cli/commands/new_command.py
   import click
   from typing import Any

   def new_command(ctx: click.Context, **kwargs: Any) -> None:
       """Implementation of new command."""
       # Command logic here
       click.echo("New command executed!")
   ```

2. **Register command in CLI:**
   ```python
   # info_tech_cli/cli.py
   from .commands.new_command import new_command

   @cli.command()
   @click.option('--option', help='Command option')
   @click.pass_context
   def new(ctx, option):
       """New command description."""
       new_command(ctx, option=option)
   ```

3. **Add tests:**
   ```python
   # tests/test_commands/test_new_command.py
   from click.testing import CliRunner
   from info_tech_cli.cli import cli

   def test_new_command():
       runner = CliRunner()
       result = runner.invoke(cli, ['new'])
       assert result.exit_code == 0
   ```

### Adding New Templates

1. **Create template structure:**
   ```
   info_tech_cli/templates/new-template/
   ├── module.json.j2
   ├── content/
   │   ├── index.md.j2
   │   └── lessons/
   └── static/
   ```

2. **Template files with variables:**
   ```json
   // module.json.j2
   {
     "name": "{{ module_name }}",
     "category": "{{ category }}",
     "template": "new-template",
     "custom_field": "value"
   }
   ```

3. **Register template:**
   ```python
   # Template automatically discovered by file structure
   # No additional registration required
   ```

### Adding Validation Rules

1. **Extend validator:**
   ```python
   # info_tech_cli/utils/validation.py
   class ModuleValidator:
       def _validate_custom_rule(self) -> None:
           """Add custom validation rule."""
           # Custom validation logic
           if not self._check_custom_condition():
               self.errors.append("Custom validation failed")
   ```

2. **Add to validation pipeline:**
   ```python
   def validate(self) -> Tuple[bool, List[str], List[str]]:
       # Existing validations...
       self._validate_custom_rule()
       # ...
   ```

## Bug Fixes

### Bug Report Process

When reporting bugs, include:

1. **Environment information:**
   ```bash
   # Include output of these commands
   info_tech_cli --version
   python --version
   pip list | grep info-tech-cli
   ```

2. **Steps to reproduce:**
   ```
   1. Run command: info_tech_cli create test-module
   2. Navigate to: cd test-module
   3. Execute: info_tech_cli validate
   4. Observe error: ValidationError: ...
   ```

3. **Expected vs actual behavior**

4. **Relevant logs and error messages**

### Bug Fix Process

1. **Create failing test that demonstrates the bug**
2. **Fix the bug with minimal changes**
3. **Verify the test now passes**
4. **Run full test suite to check for regressions**
5. **Update documentation if necessary**

### Common Bug Categories

**Template Processing:**
- Variable substitution failures
- Template file discovery issues
- Jinja2 syntax errors

**GitHub Integration:**
- API authentication failures
- Rate limiting issues
- Repository creation conflicts

**Validation:**
- False positive/negative validations
- Performance issues with large modules
- Cross-platform file path issues

## Documentation

### Documentation Standards

- Use clear, concise language
- Include practical examples
- Test all code examples
- Maintain consistency with existing docs
- Update both inline and external documentation

### Documentation Types

**Inline Documentation:**
```python
def create_module(module_name: str, template: str) -> Path:
    """Create a new learning module from template.

    This function creates a new educational module by processing
    the specified template with the given parameters.

    Args:
        module_name: Name for the new module (must be kebab-case)
        template: Template name to use for module creation

    Returns:
        Path to the created module directory

    Raises:
        ValueError: If module_name is not valid kebab-case
        FileExistsError: If module directory already exists
        TemplateNotFoundError: If specified template doesn't exist

    Example:
        >>> path = create_module("python-basics", "module-programming")
        >>> print(path)
        /current/directory/python-basics
    """
```

**README Updates:**
- Update feature lists
- Add new examples
- Update installation instructions
- Keep changelog current

## Release Process

### Version Management

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to CLI interface
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

1. **Pre-release:**
   - [ ] All tests pass
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated
   - [ ] Version numbers bumped in `__init__.py` and `setup.py`

2. **Release:**
   - [ ] Create release branch: `git checkout -b release/v1.2.0`
   - [ ] Final testing on release branch
   - [ ] Tag release: `git tag v1.2.0`
   - [ ] Build package: `python setup.py sdist bdist_wheel`
   - [ ] Upload to PyPI: `twine upload dist/*`

3. **Post-release:**
   - [ ] Merge release branch to main
   - [ ] Create GitHub release with notes
   - [ ] Update documentation site
   - [ ] Announce on relevant channels

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what is best for the community

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussions
- **Pull Requests**: Code contributions and reviews

### Getting Help

- Check existing issues and documentation first
- Provide detailed information when asking questions
- Be patient and respectful when seeking help
- Offer help to others when possible

## Advanced Contributions

### Plugin Development

Future plugin system design:

```python
# Plugin interface example
class InfoTechPlugin:
    def __init__(self):
        self.name = "my-plugin"
        self.version = "1.0.0"

    def register_commands(self, cli_group):
        """Register plugin commands with CLI."""
        @cli_group.command()
        def my_command():
            click.echo("Plugin command executed!")

    def register_templates(self, template_registry):
        """Register plugin templates."""
        template_registry.add_template("my-template", "/path/to/template")

    def register_validators(self, validator_registry):
        """Register custom validators."""
        validator_registry.add_validator("my-validation", my_validator_func)
```

### Performance Optimization

Areas for optimization:
- Template processing speed
- File I/O operations
- GitHub API efficiency
- Memory usage with large modules

### Security Contributions

Security-focused contributions:
- Input validation improvements
- Secure template processing
- GitHub token handling
- File system security

---

*Ready to contribute? Start by checking our [open issues](https://github.com/info-tech-io/info-tech-cli/issues) or proposing a new feature in [discussions](https://github.com/info-tech-io/info-tech-cli/discussions).*