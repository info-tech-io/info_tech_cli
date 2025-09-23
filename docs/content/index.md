---
title: "Info-Tech CLI"
description: "Command-line interface for InfoTech.io educational platform - create, manage and deploy learning modules"
date: 2024-09-23
draft: false
weight: 1
---

# Info-Tech CLI

A powerful command-line interface for the InfoTech.io educational platform that streamlines the creation, management, and deployment of learning modules with integrated Quiz Engine support.

## Overview

Info-Tech CLI is designed to accelerate educational content development by providing developers and educators with sophisticated tooling for building interactive learning experiences.

### Key Features

- **Module Creation** - Generate new learning modules from pre-built templates
- **Template System** - Choose from educational, programming, and specialized templates
- **Quiz Integration** - Built-in support for Quiz Engine interactive assessments
- **GitHub Integration** - Automatic repository creation and management
- **Category Management** - Organize modules by subject, difficulty, and language
- **Interactive Mode** - Guided setup with prompts and validation
- **Batch Operations** - Efficiently manage multiple modules

### Architecture

Info-Tech CLI follows a modular command structure built on Click framework:

```
info_tech_cli/
├── cli.py              # Main CLI interface
├── commands/           # Command implementations
│   ├── create.py      # Module creation
│   ├── delete.py      # Module deletion
│   └── validate.py    # Module validation
├── templates/         # Module templates
└── utils/             # Shared utilities
```

## Use Cases

### Educational Content Creators
- **Course Development** - Rapidly prototype new programming courses
- **Content Organization** - Structure lessons with consistent templates
- **Assessment Integration** - Add quizzes and interactive elements
- **Multi-language Support** - Create content in multiple languages

### Development Teams
- **Training Materials** - Generate internal training modules
- **Documentation** - Create interactive documentation with examples
- **Onboarding** - Build structured onboarding experiences
- **Skills Assessment** - Develop technical skill evaluations

### Educational Institutions
- **Curriculum Management** - Standardize course creation processes
- **Content Distribution** - Deploy modules across multiple platforms
- **Progress Tracking** - Integrate with learning management systems
- **Collaborative Development** - Team-based content creation

## Quick Start

### Installation

```bash
# Install from PyPI (when available)
pip install info-tech-cli

# Or install from source
git clone https://github.com/info-tech-io/info-tech-cli.git
cd info-tech-cli
pip install -e .
```

### Basic Usage

```bash
# Create a new Python basics module
info_tech_cli create python-basics

# Create with specific options
info_tech_cli create linux-admin \
  --category devops \
  --difficulty intermediate \
  --language en

# Interactive creation with prompts
info_tech_cli create --interactive

# Validate existing module
info_tech_cli validate ./my-module

# View help
info_tech_cli --help
```

## Command Reference

### Core Commands

**`create`** - Create new learning modules
```bash
info_tech_cli create MODULE_NAME [OPTIONS]
```

**`delete`** - Remove existing modules
```bash
info_tech_cli delete MODULE_NAME [OPTIONS]
```

**`validate`** - Validate module structure
```bash
info_tech_cli validate [PATH]
```

**`version`** - Show version information
```bash
info_tech_cli version
```

### Available Options

- `--template, -t` - Module template (default: module-basic)
- `--category, -c` - Content category (default: programming)
- `--difficulty, -d` - Difficulty level (beginner/intermediate/advanced)
- `--language, -l` - Primary language (ru/en)
- `--interactive, -i` - Interactive mode with prompts
- `--force, -f` - Force operation without confirmation
- `--remove-repo` - Also remove GitHub repository

## Technology Stack

**Core Framework:**
- **Click** - Command-line interface framework
- **Python 3.8+** - Modern Python with type hints
- **dotenv** - Environment configuration management

**Integration:**
- **GitHub API** - Repository management and automation
- **Hugo Templates** - Static site generation for modules
- **Quiz Engine** - Interactive assessment integration
- **JSON Schema** - Configuration validation

**Development:**
- **pytest** - Comprehensive testing framework
- **Black** - Code formatting and style consistency
- **Type hints** - Static type checking support

## Template System

### Available Templates

**`module-basic`** - Standard educational module template
- Basic content structure
- Quiz integration placeholders
- Standard navigation
- Minimal styling

**`module-programming`** - Programming course template
- Code syntax highlighting
- Interactive code examples
- Exercise framework
- Project-based structure

**`module-documentation`** - Technical documentation template
- API reference structure
- Code examples
- Getting started guide
- Advanced topics organization

### Template Structure

```
module-template/
├── content/              # Main content files
│   ├── index.md         # Module overview
│   ├── lessons/         # Individual lessons
│   └── exercises/       # Practice exercises
├── static/              # Static assets
├── quizzes/             # Quiz definitions
├── config/              # Module configuration
└── scripts/             # Build and deploy scripts
```

---

*Ready to create your first module? Check out our [Getting Started Guide]({{< ref "getting-started" >}}) for detailed setup instructions.*