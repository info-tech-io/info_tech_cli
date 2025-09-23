---
title: "Getting Started"
description: "Complete setup guide for Info-Tech CLI - from installation to creating your first module"
date: 2024-09-23
draft: false
weight: 2
---

# Getting Started with Info-Tech CLI

This guide will walk you through installing Info-Tech CLI and creating your first learning module in just a few minutes.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed with pip
- **Git** for version control
- **GitHub account** (optional, for repository integration)
- **Text editor** or IDE for content creation

### Verify Prerequisites

```bash
# Check Python version
python3 --version

# Check pip installation
pip --version

# Check Git installation
git --version
```

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install info-tech-cli
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/info-tech-io/info-tech-cli.git
cd info-tech-cli

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Verify Installation

```bash
# Check if CLI is available
info_tech_cli --version

# View available commands
info_tech_cli --help
```

## Configuration

### Environment Setup

Create a `.env` file in your working directory for configuration:

```bash
# .env file
GITHUB_TOKEN=your_github_token_here
DEFAULT_AUTHOR=Your Name
DEFAULT_EMAIL=your.email@example.com
DEFAULT_ORGANIZATION=your-github-org
```

**Getting GitHub Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` permissions
3. Copy token to your `.env` file

### Global Configuration

```bash
# Set default template
export INFO_TECH_DEFAULT_TEMPLATE=module-programming

# Set default category
export INFO_TECH_DEFAULT_CATEGORY=programming

# Set default language
export INFO_TECH_DEFAULT_LANGUAGE=en
```

## Creating Your First Module

### Basic Module Creation

```bash
# Create a simple module
info_tech_cli create my-first-module

# This creates:
# ./my-first-module/
# ├── content/
# │   ├── index.md
# │   └── lessons/
# ├── quizzes/
# ├── static/
# └── module.json
```

### Interactive Creation

For guided setup, use interactive mode:

```bash
info_tech_cli create --interactive
```

You'll be prompted for:
- Module name (kebab-case)
- Template selection
- Category and difficulty
- Language preference
- GitHub integration options

### Advanced Creation

Create a programming course with specific options:

```bash
info_tech_cli create python-fundamentals \
  --template module-programming \
  --category programming \
  --difficulty beginner \
  --language en
```

## Understanding Module Structure

### Generated Files

When you create a module, Info-Tech CLI generates this structure:

```
python-fundamentals/
├── content/                 # Main content directory
│   ├── index.md            # Module overview and introduction
│   ├── lessons/            # Individual lesson files
│   │   ├── 01-basics.md
│   │   ├── 02-variables.md
│   │   └── 03-functions.md
│   └── exercises/          # Hands-on practice exercises
│       ├── exercise-1.md
│       └── exercise-2.md
├── quizzes/                # Quiz Engine quiz definitions
│   ├── basics-quiz.json
│   └── functions-quiz.json
├── static/                 # Images, videos, and assets
│   ├── images/
│   └── videos/
├── config/                 # Module configuration
│   └── build.json
├── scripts/                # Build and deployment scripts
│   ├── build.sh
│   └── deploy.sh
├── module.json             # Module metadata
└── README.md               # Development documentation
```

### Key Files Explained

**`module.json`** - Module metadata and configuration:
```json
{
  "name": "python-fundamentals",
  "version": "1.0.0",
  "category": "programming",
  "difficulty": "beginner",
  "language": "en",
  "author": "Your Name",
  "description": "Learn Python programming fundamentals",
  "topics": ["variables", "functions", "control-flow"],
  "estimated_time": "4 hours",
  "prerequisites": [],
  "quiz_integration": true
}
```

**`content/index.md`** - Module homepage:
```markdown
---
title: "Python Fundamentals"
description: "Learn Python programming from scratch"
weight: 1
---

# Python Fundamentals

Welcome to Python Fundamentals! This module will teach you...

## Learning Objectives

By the end of this module, you will:
- Understand Python syntax and basic concepts
- Write simple Python programs
- Use variables and functions effectively
```

## Working with Content

### Adding Lessons

Create new lesson files in the `content/lessons/` directory:

```bash
# content/lessons/04-lists.md
---
title: "Working with Lists"
description: "Learn Python list operations"
weight: 4
---

# Working with Lists

Python lists are versatile data structures...

## Creating Lists

```python
# Create a list
fruits = ['apple', 'banana', 'orange']
numbers = [1, 2, 3, 4, 5]
```

## Exercises

Try these exercises to practice list operations...
```

### Adding Quizzes

Create quiz files in the `quizzes/` directory:

```json
{
  "title": "Python Lists Quiz",
  "description": "Test your knowledge of Python lists",
  "questions": [
    {
      "type": "multiple_choice",
      "question": "How do you create an empty list in Python?",
      "options": ["[]", "{}", "()", "None"],
      "correct": 0,
      "explanation": "Square brackets [] create an empty list in Python."
    }
  ]
}
```

### Adding Assets

Place images, videos, and other assets in the `static/` directory:

```
static/
├── images/
│   ├── python-logo.png
│   └── diagram-variables.svg
├── videos/
│   └── intro-python.mp4
└── downloads/
    └── exercise-files.zip
```

Reference assets in your content:

```markdown
![Python Logo](../static/images/python-logo.png)

Watch this introduction video:
{{< video src="../static/videos/intro-python.mp4" >}}
```

## Validation and Testing

### Module Validation

Validate your module structure:

```bash
# Validate current directory
info_tech_cli validate

# Validate specific module
info_tech_cli validate ./python-fundamentals

# Validation checks:
# ✓ Module structure is correct
# ✓ Required files are present
# ✓ Metadata is valid
# ✓ Content links are working
# ✓ Quiz format is correct
```

### Content Testing

Test your content during development:

```bash
# Build the module locally (if Hugo integration available)
cd python-fundamentals
hugo server -D

# View at http://localhost:1313
```

## Next Steps

### Publishing Your Module

Once your module is ready:

1. **Validate the module:**
   ```bash
   info_tech_cli validate ./python-fundamentals
   ```

2. **Create GitHub repository (if configured):**
   ```bash
   # This happens automatically if GITHUB_TOKEN is set
   # Or manually push to GitHub
   ```

3. **Deploy to InfoTech.io platform:**
   ```bash
   # Using platform-specific deployment
   # (Integration details depend on target platform)
   ```

### Advanced Features

Explore advanced CLI features:

- **Batch Operations** - Manage multiple modules
- **Template Customization** - Create your own templates
- **Integration Hooks** - Connect with external systems
- **Automated Deployment** - Set up CI/CD pipelines

## Common Workflows

### Course Development Workflow

```bash
# 1. Create module
info_tech_cli create advanced-python --difficulty advanced

# 2. Add content iteratively
cd advanced-python
# Edit content files...

# 3. Validate frequently
info_tech_cli validate

# 4. Test locally
hugo server -D

# 5. Commit and deploy
git add .
git commit -m "Add advanced Python module"
git push
```

### Template-Based Development

```bash
# Create multiple related modules
info_tech_cli create python-basics --template module-programming
info_tech_cli create python-web --template module-programming
info_tech_cli create python-data --template module-programming

# Maintain consistency across modules
for module in python-*; do
  info_tech_cli validate $module
done
```

## Troubleshooting

### Common Issues

**"Command not found: info_tech_cli"**
```bash
# Ensure CLI is installed
pip install info-tech-cli

# Check if pip bin directory is in PATH
python -m pip show info-tech-cli
```

**"GitHub token not configured"**
```bash
# Set token in .env file
echo "GITHUB_TOKEN=your_token_here" >> .env

# Or set environment variable
export GITHUB_TOKEN=your_token_here
```

**"Module validation failed"**
```bash
# Check specific validation errors
info_tech_cli validate ./module-name --verbose

# Common fixes:
# - Ensure module.json is valid JSON
# - Check required files are present
# - Verify content markdown syntax
```

**"Template not found"**
```bash
# List available templates
info_tech_cli create --help

# Use default template
info_tech_cli create module-name --template module-basic
```

### Getting Help

- **Built-in help:** `info_tech_cli --help` or `info_tech_cli COMMAND --help`
- **Documentation:** Visit our [User Guide]({{< ref "user-guide" >}})
- **Examples:** Check out [example modules](https://github.com/info-tech-io/module-examples)
- **Issues:** Report bugs on [GitHub Issues](https://github.com/info-tech-io/info-tech-cli/issues)

---

*Ready to dive deeper? Check out our [User Guide]({{< ref "user-guide" >}}) for advanced usage patterns and best practices.*