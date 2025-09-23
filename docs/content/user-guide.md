---
title: "User Guide"
description: "Comprehensive guide to Info-Tech CLI - advanced features, best practices, and workflow optimization"
date: 2024-09-23
draft: false
weight: 3
---

# User Guide

This comprehensive guide covers advanced usage of Info-Tech CLI, best practices for educational content development, and workflow optimization techniques.

## Command Reference

### Create Command

The `create` command is the primary tool for generating new learning modules.

#### Basic Syntax

```bash
info_tech_cli create MODULE_NAME [OPTIONS]
```

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--template` | `-t` | choice | `module-basic` | Template to use |
| `--category` | `-c` | string | `programming` | Module category |
| `--difficulty` | `-d` | choice | `beginner` | Difficulty level |
| `--language` | `-l` | choice | `ru` | Primary language |
| `--interactive` | `-i` | flag | `false` | Interactive mode |

#### Examples

```bash
# Basic module creation
info_tech_cli create python-intro

# Advanced Python course
info_tech_cli create advanced-python \
  --template module-programming \
  --category programming \
  --difficulty advanced \
  --language en

# DevOps course with interactive setup
info_tech_cli create docker-fundamentals \
  --category devops \
  --interactive

# Quick prototyping
info_tech_cli create test-module --template module-basic
```

### Delete Command

Remove modules and optionally their GitHub repositories.

```bash
# Delete local module
info_tech_cli delete old-module

# Force deletion without confirmation
info_tech_cli delete test-module --force

# Delete module and GitHub repository
info_tech_cli delete outdated-course --force --remove-repo
```

### Validate Command

Validate module structure and content integrity.

```bash
# Validate current directory
info_tech_cli validate

# Validate specific module
info_tech_cli validate ./python-course

# Verbose validation with detailed output
info_tech_cli validate ./module --verbose
```

## Template System

### Available Templates

#### `module-basic`
General-purpose educational module template.

**Features:**
- Simple content structure
- Basic navigation
- Quiz placeholders
- Minimal styling
- Universal compatibility

**Best for:**
- Quick prototypes
- Simple content
- Non-technical subjects
- Getting started

#### `module-programming`
Specialized template for programming courses.

**Features:**
- Syntax highlighting
- Code examples
- Interactive exercises
- Project structure
- Technical documentation

**Best for:**
- Programming languages
- Software development
- Technical tutorials
- Hands-on coding

#### `module-documentation`
Technical documentation template.

**Features:**
- API reference structure
- Code documentation
- Getting started guides
- Advanced topics
- Search functionality

**Best for:**
- Software documentation
- API references
- Technical guides
- Developer resources

### Template Customization

#### Creating Custom Templates

```bash
# Templates are stored in the CLI package
# To create custom templates:

# 1. Create template directory
mkdir -p ~/.info-tech-cli/templates/my-template

# 2. Add template files
cat > ~/.info-tech-cli/templates/my-template/module.json << EOF
{
  "name": "{{module_name}}",
  "template": "my-template",
  "category": "{{category}}",
  "custom_field": "custom_value"
}
EOF

# 3. Use custom template
info_tech_cli create new-module --template my-template
```

#### Template Variables

Templates support variable substitution:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{module_name}}` | Module name | `python-basics` |
| `{{title}}` | Human-readable title | `Python Basics` |
| `{{category}}` | Module category | `programming` |
| `{{difficulty}}` | Difficulty level | `beginner` |
| `{{language}}` | Primary language | `en` |
| `{{author}}` | Author name | `John Doe` |
| `{{date}}` | Creation date | `2024-09-23` |

## Advanced Configuration

### Environment Variables

Configure CLI behavior with environment variables:

```bash
# Default settings
export INFO_TECH_DEFAULT_TEMPLATE=module-programming
export INFO_TECH_DEFAULT_CATEGORY=programming
export INFO_TECH_DEFAULT_DIFFICULTY=intermediate
export INFO_TECH_DEFAULT_LANGUAGE=en
export INFO_TECH_DEFAULT_AUTHOR="Your Name"

# GitHub integration
export GITHUB_TOKEN=your_token_here
export GITHUB_ORG=your-organization

# Template paths
export INFO_TECH_TEMPLATE_PATH=/path/to/custom/templates

# Output settings
export INFO_TECH_OUTPUT_DIR=/path/to/modules
```

### Configuration File

Create a global configuration file at `~/.info-tech-cli/config.json`:

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

## Content Development

### Module Structure Best Practices

#### Organizing Content

```
my-module/
├── content/
│   ├── index.md              # Module overview (required)
│   ├── prerequisites.md      # Prerequisites and setup
│   ├── lessons/              # Ordered lessons
│   │   ├── 01-introduction.md
│   │   ├── 02-basics.md
│   │   └── 03-advanced.md
│   ├── exercises/            # Hands-on practice
│   │   ├── exercise-1.md
│   │   └── exercise-2.md
│   └── reference/            # Reference materials
│       ├── glossary.md
│       └── resources.md
├── quizzes/                  # Quiz definitions
├── static/                   # Assets
└── module.json               # Metadata
```

#### Content Guidelines

**Lesson Structure:**
```markdown
---
title: "Lesson Title"
description: "Brief lesson description"
weight: 1
duration: "30 minutes"
objectives:
  - "Learning objective 1"
  - "Learning objective 2"
---

# Lesson Title

## Introduction
Brief overview of what will be covered...

## Core Content
Main lesson content with examples...

## Practice
Hands-on exercises...

## Summary
Key takeaways...

## Next Steps
Link to next lesson or additional resources...
```

**Exercise Format:**
```markdown
---
title: "Exercise: Build a Calculator"
type: "hands-on"
difficulty: "intermediate"
estimated_time: "45 minutes"
---

# Exercise: Build a Calculator

## Objective
Build a simple calculator application...

## Requirements
- Python 3.8+
- Basic math operations
- User input handling

## Instructions
1. Create a new Python file...
2. Implement basic operations...
3. Add input validation...

## Solution
<details>
<summary>Click to view solution</summary>

```python
def calculator():
    # Solution code here...
```

</details>

## Extension Challenges
- Add scientific functions
- Create a GUI interface
- Add calculation history
```

### Quiz Integration

#### Quiz File Format

Create quiz files in JSON format:

```json
{
  "title": "Python Basics Quiz",
  "description": "Test your understanding of Python fundamentals",
  "metadata": {
    "category": "programming",
    "difficulty": "beginner",
    "estimated_time": "10 minutes"
  },
  "questions": [
    {
      "id": "q1",
      "type": "multiple_choice",
      "question": "What is the correct way to create a list in Python?",
      "options": [
        "list = []",
        "list = {}",
        "list = ()",
        "list = <>"
      ],
      "correct": 0,
      "explanation": "Square brackets [] are used to create lists in Python.",
      "points": 1
    },
    {
      "id": "q2",
      "type": "code_completion",
      "question": "Complete the function to calculate the square of a number:",
      "code_template": "def square(x):\n    return ___",
      "correct_answer": "x * x",
      "test_cases": [
        {"input": "2", "expected": "4"},
        {"input": "5", "expected": "25"}
      ],
      "points": 2
    }
  ],
  "passing_score": 70
}
```

#### Quiz Types

**Multiple Choice:**
```json
{
  "type": "multiple_choice",
  "question": "Question text",
  "options": ["Option A", "Option B", "Option C"],
  "correct": 0,
  "explanation": "Why this is correct"
}
```

**True/False:**
```json
{
  "type": "true_false",
  "question": "Python is an interpreted language.",
  "correct": true,
  "explanation": "Python code is interpreted at runtime"
}
```

**Code Completion:**
```json
{
  "type": "code_completion",
  "question": "Complete the function",
  "code_template": "def add(a, b):\n    return ___",
  "correct_answer": "a + b"
}
```

### Asset Management

#### Image Optimization

```bash
# Recommended image formats and sizes
# Icons: SVG or PNG, 64x64px
# Screenshots: PNG, max 1200px width
# Diagrams: SVG preferred, PNG fallback
# Photos: JPEG, optimized for web

# Example directory structure
static/
├── images/
│   ├── icons/           # UI icons (SVG)
│   ├── screenshots/     # Interface screenshots (PNG)
│   ├── diagrams/        # Technical diagrams (SVG)
│   └── photos/          # Photography (JPEG)
├── videos/
│   ├── tutorials/       # Tutorial videos (MP4)
│   └── demos/          # Demo recordings (MP4)
└── downloads/
    ├── code-samples/    # Code examples (ZIP)
    └── datasets/        # Practice data (CSV, JSON)
```

#### Video Integration

```markdown
# Embed videos in content
{{< video src="../static/videos/intro.mp4" poster="../static/images/video-poster.jpg" >}}

# YouTube integration
{{< youtube id="dQw4w9WgXcQ" title="Tutorial Video" >}}

# Video with transcript
{{< video src="../static/videos/lesson1.mp4" transcript="../static/transcripts/lesson1.vtt" >}}
```

## Workflow Optimization

### Batch Operations

#### Creating Multiple Modules

```bash
#!/bin/bash
# create-course.sh - Create a complete course structure

COURSE_NAME="python-fundamentals"
MODULES=("basics" "functions" "classes" "modules" "testing")

for module in "${MODULES[@]}"; do
    info_tech_cli create "${COURSE_NAME}-${module}" \
      --template module-programming \
      --category programming \
      --difficulty beginner
done
```

#### Module Maintenance

```bash
#!/bin/bash
# validate-all.sh - Validate all modules in directory

for dir in */; do
    if [ -f "$dir/module.json" ]; then
        echo "Validating $dir..."
        info_tech_cli validate "$dir"
    fi
done
```

### Git Integration

#### Automated Git Workflow

```bash
# .info-tech-cli/hooks/post-create.sh
#!/bin/bash
# Automatically initialize Git repository after module creation

MODULE_DIR="$1"
cd "$MODULE_DIR"

# Initialize repository
git init
git add .
git commit -m "Initial module structure"

# Add remote if GitHub token is configured
if [ ! -z "$GITHUB_TOKEN" ]; then
    gh repo create "$MODULE_DIR" --public
    git remote add origin "https://github.com/$GITHUB_ORG/$MODULE_DIR.git"
    git push -u origin main
fi
```

### CI/CD Integration

#### GitHub Actions Workflow

```yaml
# .github/workflows/validate-modules.yml
name: Validate Modules

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Info-Tech CLI
      run: pip install info-tech-cli

    - name: Validate all modules
      run: |
        for dir in */; do
          if [ -f "$dir/module.json" ]; then
            echo "Validating $dir..."
            info_tech_cli validate "$dir"
          fi
        done
```

## Performance Optimization

### Large Module Management

#### Efficient File Organization

```bash
# For large modules with many assets
large-module/
├── content/
│   ├── chapters/        # Split into chapters
│   │   ├── ch01/
│   │   ├── ch02/
│   │   └── ch03/
│   └── shared/          # Shared content
├── static/
│   ├── by-chapter/      # Organize assets by chapter
│   │   ├── ch01/
│   │   └── ch02/
│   └── shared/          # Shared assets
└── quizzes/
    ├── chapter-quizzes/ # Chapter-specific quizzes
    └── final-exam/      # Comprehensive assessments
```

#### Content Optimization

```bash
# Optimize images before adding to modules
for img in static/images/*.png; do
    pngquant --quality=65-80 --output "${img%.png}-optimized.png" "$img"
done

# Compress videos
for video in static/videos/*.mp4; do
    ffmpeg -i "$video" -vcodec h264 -acodec mp2 "${video%.mp4}-compressed.mp4"
done
```

### Development Efficiency

#### Template Shortcuts

```bash
# Create aliases for common operations
alias itc='info_tech_cli'
alias create-py='info_tech_cli create --template module-programming --category programming'
alias create-doc='info_tech_cli create --template module-documentation --category documentation'

# Quick validation
alias validate-all='find . -name "module.json" -execdir info_tech_cli validate . \;'
```

#### IDE Integration

**VS Code Integration:**
```json
// .vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Validate Module",
            "type": "shell",
            "command": "info_tech_cli",
            "args": ["validate", "."],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ]
}
```

## Troubleshooting

### Common Issues

#### Validation Failures

```bash
# Check common validation issues
info_tech_cli validate ./module --verbose

# Common fixes:
# 1. Invalid module.json syntax
jsonlint module.json

# 2. Missing required files
ls -la content/index.md

# 3. Broken internal links
grep -r "ref \"" content/

# 4. Invalid quiz format
python -m json.tool quizzes/quiz1.json
```

#### GitHub Integration Issues

```bash
# Check GitHub token permissions
gh auth status

# Test repository creation
gh repo create test-repo --public --confirm

# Verify organization access
gh api user/orgs
```

#### Template Issues

```bash
# List available templates
info_tech_cli create --help | grep -A 10 "template"

# Check template syntax
find ~/.info-tech-cli/templates -name "*.json" -exec jsonlint {} \;

# Reset to default templates
rm -rf ~/.info-tech-cli/templates
info_tech_cli create test --template module-basic
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Set debug environment variable
export INFO_TECH_DEBUG=true

# Use verbose flag
info_tech_cli create module-name --verbose

# Check logs
tail -f ~/.info-tech-cli/cli.log
```

## Best Practices

### Content Creation

1. **Start with Learning Objectives** - Define clear, measurable goals
2. **Use Progressive Complexity** - Build from simple to advanced concepts
3. **Include Practical Examples** - Real-world applications and use cases
4. **Add Interactive Elements** - Quizzes, exercises, and hands-on practice
5. **Provide Multiple Formats** - Text, video, audio, and interactive content

### Technical Standards

1. **Validate Frequently** - Check module structure during development
2. **Use Version Control** - Track changes and collaborate effectively
3. **Optimize Assets** - Compress images and videos for web delivery
4. **Test Across Platforms** - Ensure compatibility with different devices
5. **Document Dependencies** - Clear prerequisites and setup instructions

### Team Collaboration

1. **Establish Conventions** - Consistent naming and structure
2. **Use Templates** - Standardize module creation
3. **Code Review Process** - Peer review of educational content
4. **Automated Testing** - CI/CD validation workflows
5. **Regular Updates** - Keep content current and accurate

---

*Need technical implementation details? Check out our [Developer Documentation]({{< ref "developer" >}}) or explore [Contributing Guidelines]({{< ref "contributing" >}}).*