---
title: "Developer Documentation"
description: "Technical implementation details, API reference, and architecture guide for Info-Tech CLI"
date: 2024-09-23
draft: false
weight: 4
---

# Developer Documentation

This document provides technical implementation details for Info-Tech CLI, including architecture overview, API reference, and development guidelines.

## Architecture Overview

### System Architecture

Info-Tech CLI follows a modular command-line architecture built on the Click framework:

```
info_tech_cli/
├── __init__.py          # Package initialization and metadata
├── cli.py               # Main CLI interface and command routing
├── commands/            # Command implementations
│   ├── __init__.py
│   ├── create.py        # Module creation logic
│   ├── delete.py        # Module deletion logic
│   └── validate.py      # Module validation logic
├── templates/           # Built-in module templates
│   ├── module-basic/
│   ├── module-programming/
│   └── module-documentation/
├── utils/               # Shared utilities and helpers
│   ├── __init__.py
│   ├── github.py        # GitHub API integration
│   ├── validation.py    # Validation utilities
│   └── templates.py     # Template processing
└── config/              # Configuration management
    ├── __init__.py
    └── settings.py      # Default settings and validation
```

### Core Components

#### 1. CLI Interface (cli.py)

The main entry point that defines the command structure and handles global configuration:

```python
import click
from dotenv import load_dotenv
from .commands import create_module, delete_module, validate_module

@click.group()
@click.version_option(version="0.1.0", prog_name="info_tech_cli")
@click.pass_context
def cli(ctx):
    """InfoTech CLI - Educational platform command-line interface."""
    ctx.ensure_object(dict)
    load_dotenv()  # Load environment variables

@cli.command()
@click.argument('module_name')
@click.option('--template', '-t', default='module-basic')
@click.option('--category', '-c', default='programming')
@click.option('--difficulty', '-d', type=click.Choice(['beginner', 'intermediate', 'advanced']))
@click.option('--language', '-l', type=click.Choice(['ru', 'en']))
@click.option('--interactive', '-i', is_flag=True)
@click.pass_context
def create(ctx, module_name, template, category, difficulty, language, interactive):
    """Create a new learning module from template."""
    create_module(ctx, module_name, template, category, difficulty, language, interactive)
```

#### 2. Command Implementations (commands/)

Each command is implemented as a separate module for maintainability:

**Create Command (commands/create.py):**
```python
import os
import json
import shutil
from typing import Dict, Any, Optional
from ..utils.templates import TemplateProcessor
from ..utils.github import GitHubIntegration
from ..utils.validation import validate_module_name

def create_module(
    ctx: click.Context,
    module_name: str,
    template: str,
    category: str,
    difficulty: str,
    language: str,
    interactive: bool
) -> None:
    """Create a new learning module from template.

    Args:
        ctx: Click context object
        module_name: Name of the module to create
        template: Template to use for module creation
        category: Module category
        difficulty: Difficulty level
        language: Primary language
        interactive: Enable interactive mode
    """
    # Validate module name
    if not validate_module_name(module_name):
        click.echo(f"Error: Invalid module name '{module_name}'")
        return

    # Interactive mode handling
    if interactive:
        module_name, template, category, difficulty, language = interactive_setup()

    # Process template
    processor = TemplateProcessor(template)
    template_vars = {
        'module_name': module_name,
        'category': category,
        'difficulty': difficulty,
        'language': language,
        'author': os.getenv('DEFAULT_AUTHOR', 'Unknown'),
        'date': datetime.now().isoformat()[:10]
    }

    try:
        # Create module from template
        module_path = processor.create_module(module_name, template_vars)

        # GitHub integration
        if os.getenv('GITHUB_TOKEN'):
            github = GitHubIntegration()
            github.create_repository(module_name, module_path)

        click.echo(f"✅ Module '{module_name}' created successfully at {module_path}")

    except Exception as e:
        click.echo(f"❌ Error creating module: {str(e)}")
```

#### 3. Template System (utils/templates.py)

Handles template processing and variable substitution:

```python
import os
import json
import shutil
from typing import Dict, Any, List
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

class TemplateProcessor:
    """Handles template processing and module generation."""

    def __init__(self, template_name: str):
        self.template_name = template_name
        self.template_path = self._find_template_path(template_name)
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_path)),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def _find_template_path(self, template_name: str) -> Path:
        """Find template path in search locations."""
        search_paths = [
            Path.home() / '.info-tech-cli' / 'templates',
            Path(__file__).parent.parent / 'templates',
            Path('/usr/local/share/info-tech-cli/templates')
        ]

        for path in search_paths:
            template_path = path / template_name
            if template_path.exists():
                return template_path

        raise FileNotFoundError(f"Template '{template_name}' not found")

    def create_module(self, module_name: str, variables: Dict[str, Any]) -> Path:
        """Create module from template with variable substitution.

        Args:
            module_name: Name of the module to create
            variables: Template variables for substitution

        Returns:
            Path to created module directory
        """
        output_path = Path.cwd() / module_name

        if output_path.exists():
            raise FileExistsError(f"Directory '{module_name}' already exists")

        # Copy template structure
        shutil.copytree(self.template_path, output_path)

        # Process template files
        for file_path in output_path.rglob('*'):
            if file_path.is_file() and self._is_template_file(file_path):
                self._process_template_file(file_path, variables)

        return output_path

    def _is_template_file(self, file_path: Path) -> bool:
        """Check if file should be processed as template."""
        template_extensions = {'.md', '.json', '.yaml', '.yml', '.html', '.txt'}
        return file_path.suffix.lower() in template_extensions

    def _process_template_file(self, file_path: Path, variables: Dict[str, Any]) -> None:
        """Process individual template file with variable substitution."""
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')

            # Apply Jinja2 template processing
            template = Template(content)
            processed_content = template.render(**variables)

            # Write processed content back
            file_path.write_text(processed_content, encoding='utf-8')

        except Exception as e:
            print(f"Warning: Could not process template file {file_path}: {e}")
```

#### 4. GitHub Integration (utils/github.py)

Handles GitHub repository operations:

```python
import os
import requests
from typing import Optional, Dict, Any
from pathlib import Path

class GitHubIntegration:
    """Handles GitHub API integration for repository management."""

    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.org = os.getenv('GITHUB_ORG')
        self.api_base = 'https://api.github.com'

        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")

    def create_repository(self, repo_name: str, local_path: Path) -> Dict[str, Any]:
        """Create GitHub repository and push initial content.

        Args:
            repo_name: Name of the repository to create
            local_path: Path to local module directory

        Returns:
            Repository information from GitHub API
        """
        # Create repository
        repo_data = {
            'name': repo_name,
            'description': f'Educational module: {repo_name}',
            'private': False,
            'auto_init': False
        }

        if self.org:
            url = f"{self.api_base}/orgs/{self.org}/repos"
        else:
            url = f"{self.api_base}/user/repos"

        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.post(url, json=repo_data, headers=headers)
        response.raise_for_status()

        repo_info = response.json()

        # Initialize git repository and push
        self._init_and_push_repo(local_path, repo_info['clone_url'])

        return repo_info

    def _init_and_push_repo(self, local_path: Path, remote_url: str) -> None:
        """Initialize git repository and push to remote."""
        import subprocess

        os.chdir(local_path)

        # Git operations
        commands = [
            ['git', 'init'],
            ['git', 'add', '.'],
            ['git', 'commit', '-m', 'Initial module structure'],
            ['git', 'branch', '-M', 'main'],
            ['git', 'remote', 'add', 'origin', remote_url],
            ['git', 'push', '-u', 'origin', 'main']
        ]

        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{result.stderr}")
```

#### 5. Validation System (utils/validation.py)

Comprehensive module validation:

```python
import json
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path

class ModuleValidator:
    """Validates module structure and content."""

    def __init__(self, module_path: Path):
        self.module_path = Path(module_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Perform comprehensive module validation.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors.clear()
        self.warnings.clear()

        # Core validation checks
        self._validate_structure()
        self._validate_metadata()
        self._validate_content()
        self._validate_quizzes()
        self._validate_assets()

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_structure(self) -> None:
        """Validate module directory structure."""
        required_files = [
            'module.json',
            'content/index.md'
        ]

        for file_path in required_files:
            full_path = self.module_path / file_path
            if not full_path.exists():
                self.errors.append(f"Required file missing: {file_path}")

        # Check for recommended directories
        recommended_dirs = ['content', 'static', 'quizzes']
        for dir_name in recommended_dirs:
            dir_path = self.module_path / dir_name
            if not dir_path.exists():
                self.warnings.append(f"Recommended directory missing: {dir_name}")

    def _validate_metadata(self) -> None:
        """Validate module.json metadata."""
        metadata_path = self.module_path / 'module.json'

        if not metadata_path.exists():
            return  # Already reported in structure validation

        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Required fields
            required_fields = ['name', 'version', 'category', 'difficulty']
            for field in required_fields:
                if field not in metadata:
                    self.errors.append(f"Required metadata field missing: {field}")

            # Validate field values
            if 'difficulty' in metadata:
                valid_difficulties = ['beginner', 'intermediate', 'advanced']
                if metadata['difficulty'] not in valid_difficulties:
                    self.errors.append(f"Invalid difficulty: {metadata['difficulty']}")

            # Validate name format (kebab-case)
            if 'name' in metadata:
                if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', metadata['name']):
                    self.errors.append("Module name must be in kebab-case format")

        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in module.json: {e}")

    def _validate_content(self) -> None:
        """Validate markdown content files."""
        content_dir = self.module_path / 'content'

        if not content_dir.exists():
            return

        # Check markdown files for basic structure
        for md_file in content_dir.rglob('*.md'):
            self._validate_markdown_file(md_file)

    def _validate_markdown_file(self, file_path: Path) -> None:
        """Validate individual markdown file."""
        try:
            content = file_path.read_text(encoding='utf-8')

            # Check for frontmatter
            if not content.startswith('---'):
                self.warnings.append(f"Missing frontmatter: {file_path.relative_to(self.module_path)}")

            # Check for broken links (basic check)
            import_pattern = r'\{\{<\s*ref\s+"([^"]+)"\s*>\}\}'
            matches = re.findall(import_pattern, content)

            for ref in matches:
                # Check if referenced file exists
                ref_path = self.module_path / 'content' / f"{ref}.md"
                if not ref_path.exists():
                    self.errors.append(f"Broken reference in {file_path.name}: {ref}")

        except Exception as e:
            self.warnings.append(f"Could not validate {file_path.name}: {e}")

    def _validate_quizzes(self) -> None:
        """Validate quiz JSON files."""
        quiz_dir = self.module_path / 'quizzes'

        if not quiz_dir.exists():
            return

        for quiz_file in quiz_dir.glob('*.json'):
            self._validate_quiz_file(quiz_file)

    def _validate_quiz_file(self, file_path: Path) -> None:
        """Validate individual quiz file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)

            # Required fields in quiz
            required_fields = ['title', 'questions']
            for field in required_fields:
                if field not in quiz_data:
                    self.errors.append(f"Quiz missing required field '{field}': {file_path.name}")

            # Validate questions
            if 'questions' in quiz_data:
                for i, question in enumerate(quiz_data['questions']):
                    self._validate_question(question, file_path.name, i)

        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in quiz {file_path.name}: {e}")

    def _validate_question(self, question: Dict[str, Any], quiz_name: str, index: int) -> None:
        """Validate individual quiz question."""
        required_fields = ['type', 'question']

        for field in required_fields:
            if field not in question:
                self.errors.append(f"Question {index} in {quiz_name} missing field: {field}")

        # Type-specific validation
        question_type = question.get('type')

        if question_type == 'multiple_choice':
            if 'options' not in question:
                self.errors.append(f"Multiple choice question {index} in {quiz_name} missing options")
            if 'correct' not in question:
                self.errors.append(f"Multiple choice question {index} in {quiz_name} missing correct answer")

        elif question_type == 'true_false':
            if 'correct' not in question:
                self.errors.append(f"True/false question {index} in {quiz_name} missing correct answer")

    def _validate_assets(self) -> None:
        """Validate static assets."""
        static_dir = self.module_path / 'static'

        if not static_dir.exists():
            return

        # Check for large files
        max_file_size = 10 * 1024 * 1024  # 10MB

        for asset_file in static_dir.rglob('*'):
            if asset_file.is_file():
                file_size = asset_file.stat().st_size
                if file_size > max_file_size:
                    self.warnings.append(f"Large asset file: {asset_file.name} ({file_size // 1024 // 1024}MB)")

def validate_module_name(name: str) -> bool:
    """Validate module name format (kebab-case)."""
    return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))
```

## API Reference

### CLI Commands

#### create

```python
@cli.command()
@click.argument('module_name')
@click.option('--template', '-t', default='module-basic')
@click.option('--category', '-c', default='programming')
@click.option('--difficulty', '-d', type=click.Choice(['beginner', 'intermediate', 'advanced']))
@click.option('--language', '-l', type=click.Choice(['ru', 'en']))
@click.option('--interactive', '-i', is_flag=True)
@click.pass_context
def create(ctx, module_name, template, category, difficulty, language, interactive):
```

#### delete

```python
@cli.command()
@click.argument('module_name')
@click.option('--force', '-f', is_flag=True)
@click.option('--remove-repo', is_flag=True)
@click.pass_context
def delete(ctx, module_name, force, remove_repo):
```

#### validate

```python
@cli.command()
@click.argument('path', default='.')
@click.option('--verbose', '-v', is_flag=True)
def validate(path, verbose):
```

### Utility Classes

#### TemplateProcessor

```python
class TemplateProcessor:
    def __init__(self, template_name: str)
    def create_module(self, module_name: str, variables: Dict[str, Any]) -> Path
    def list_templates(self) -> List[str]
    def get_template_info(self, template_name: str) -> Dict[str, Any]
```

#### ModuleValidator

```python
class ModuleValidator:
    def __init__(self, module_path: Path)
    def validate(self) -> Tuple[bool, List[str], List[str]]
    def validate_structure(self) -> bool
    def validate_metadata(self) -> bool
    def validate_content(self) -> bool
```

#### GitHubIntegration

```python
class GitHubIntegration:
    def __init__(self)
    def create_repository(self, repo_name: str, local_path: Path) -> Dict[str, Any]
    def delete_repository(self, repo_name: str) -> bool
    def list_repositories(self) -> List[Dict[str, Any]]
```

## Configuration System

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `GITHUB_TOKEN` | string | None | GitHub API token |
| `GITHUB_ORG` | string | None | GitHub organization |
| `INFO_TECH_DEFAULT_TEMPLATE` | string | `module-basic` | Default template |
| `INFO_TECH_DEFAULT_CATEGORY` | string | `programming` | Default category |
| `INFO_TECH_DEFAULT_DIFFICULTY` | string | `beginner` | Default difficulty |
| `INFO_TECH_DEFAULT_LANGUAGE` | string | `ru` | Default language |
| `INFO_TECH_DEFAULT_AUTHOR` | string | `Unknown` | Default author name |
| `INFO_TECH_TEMPLATE_PATH` | string | None | Custom template search path |
| `INFO_TECH_OUTPUT_DIR` | string | `.` | Default output directory |
| `INFO_TECH_DEBUG` | boolean | `false` | Enable debug mode |

### Configuration File

Global configuration at `~/.info-tech-cli/config.json`:

```json
{
  "defaults": {
    "template": "module-programming",
    "category": "programming",
    "difficulty": "intermediate",
    "language": "en",
    "author": "Your Name"
  },
  "github": {
    "organization": "your-org",
    "auto_create_repo": true,
    "default_branch": "main"
  },
  "templates": {
    "search_paths": [
      "~/.info-tech-cli/templates",
      "/usr/local/share/info-tech-cli/templates"
    ]
  },
  "validation": {
    "strict_mode": true,
    "check_links": true,
    "validate_quizzes": true
  }
}
```

## Extension Points

### Custom Commands

Add custom commands by extending the CLI:

```python
# custom_commands.py
import click
from info_tech_cli.cli import cli

@cli.command()
@click.argument('module_name')
def deploy(module_name):
    """Deploy module to production."""
    # Custom deployment logic
    pass
```

### Custom Templates

Create custom templates in `~/.info-tech-cli/templates/`:

```
custom-template/
├── module.json.j2
├── content/
│   ├── index.md.j2
│   └── lessons/
│       └── lesson-template.md.j2
├── quizzes/
│   └── quiz-template.json.j2
└── static/
    └── css/
        └── custom.css
```

### Plugin System

Future plugin architecture:

```python
# Plugin interface
class InfoTechPlugin:
    def register_commands(self, cli_group):
        """Register plugin commands."""
        pass

    def register_templates(self, template_registry):
        """Register plugin templates."""
        pass

    def register_validators(self, validator_registry):
        """Register custom validators."""
        pass
```

## Testing Framework

### Unit Tests

```python
# tests/test_create.py
import pytest
from click.testing import CliRunner
from info_tech_cli.cli import cli

def test_create_basic_module():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['create', 'test-module'])
        assert result.exit_code == 0
        assert 'Module \'test-module\' created successfully' in result.output

def test_create_with_options():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'create', 'advanced-module',
            '--template', 'module-programming',
            '--difficulty', 'advanced'
        ])
        assert result.exit_code == 0
```

### Integration Tests

```python
# tests/test_integration.py
import tempfile
from pathlib import Path
from info_tech_cli.utils.templates import TemplateProcessor

def test_full_module_creation_workflow():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create module
        processor = TemplateProcessor('module-basic')
        module_path = processor.create_module('test-module', {
            'module_name': 'test-module',
            'category': 'programming',
            'difficulty': 'beginner'
        })

        # Validate created module
        validator = ModuleValidator(module_path)
        is_valid, errors, warnings = validator.validate()

        assert is_valid
        assert len(errors) == 0
```

## Performance Considerations

### Template Processing

- Use Jinja2 template caching for repeated operations
- Lazy load templates to reduce memory usage
- Batch file operations when processing large templates

### GitHub API

- Implement rate limiting to avoid API limits
- Use authentication to increase rate limits
- Cache repository information when possible

### File Operations

- Use efficient file copying for large assets
- Implement progress indicators for long operations
- Handle interruptions gracefully

## Security Considerations

### Input Validation

- Validate all user inputs, especially file paths
- Sanitize template variables to prevent injection
- Use safe YAML/JSON parsing

### GitHub Integration

- Store tokens securely (environment variables, not files)
- Use minimum required permissions for GitHub tokens
- Validate repository names and organization access

### Template Security

- Sandboxed template execution
- Validate template files before processing
- Prevent path traversal in template operations

---

*For contributing to the codebase, see our [Contributing Guide]({{< ref "contributing" >}}) or check out the [GitHub repository](https://github.com/info-tech-io/info-tech-cli).*