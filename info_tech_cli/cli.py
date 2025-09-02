"""
Main CLI interface for InfoTech.io platform tools.
"""

import click
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()

# Import commands
from .commands.create import create_module
from .commands.delete import delete_module

@click.group()
@click.version_option(version="0.1.0", prog_name="info_tech_cli")
@click.pass_context
def cli(ctx):
    """
    InfoTech CLI - Command-line interface for InfoTech.io educational platform.
    
    Create, manage and deploy learning modules with integrated Quiz Engine support.
    
    Examples:
        info_tech_cli create my-python-course
        info_tech_cli delete old-course
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Check for required environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        click.echo(click.style("Warning: GITHUB_TOKEN not found in environment", fg="yellow"))
        click.echo("Some features may not work properly.")
        click.echo("Please set GITHUB_TOKEN in your .env file.")

@cli.command()
@click.argument('module_name')
@click.option('--template', '-t', default='module-basic', 
              help='Template to use for the module (default: module-basic)')
@click.option('--category', '-c', default='programming',
              help='Module category (default: programming)')
@click.option('--difficulty', '-d', default='beginner',
              type=click.Choice(['beginner', 'intermediate', 'advanced']),
              help='Module difficulty level (default: beginner)')
@click.option('--language', '-l', default='ru',
              type=click.Choice(['ru', 'en']),
              help='Primary language (default: ru)')
@click.option('--interactive', '-i', is_flag=True,
              help='Run in interactive mode with prompts')
@click.pass_context
def create(ctx, module_name, template, category, difficulty, language, interactive):
    """Create a new learning module from template.
    
    MODULE_NAME: Name of the module to create (kebab-case)
    
    Examples:
        info_tech_cli create python-basics
        info_tech_cli create linux-admin --category devops --difficulty intermediate
        info_tech_cli create --interactive
    """
    create_module(ctx, module_name, template, category, difficulty, language, interactive)

@cli.command()
@click.argument('module_name')
@click.option('--force', '-f', is_flag=True,
              help='Force deletion without confirmation')
@click.option('--remove-repo', is_flag=True,
              help='Also remove GitHub repository (if exists)')
@click.pass_context
def delete(ctx, module_name, force, remove_repo):
    """Delete a learning module.
    
    MODULE_NAME: Name of the module to delete
    
    Examples:
        info_tech_cli delete old-module
        info_tech_cli delete test-module --force --remove-repo
    """
    delete_module(ctx, module_name, force, remove_repo)

@cli.command()
@click.argument('path', default='.')
def validate(path):
    """Validate a learning module structure.
    
    PATH: Path to the module directory (default: current directory)
    
    Examples:
        info_tech_cli validate
        info_tech_cli validate ./my-module
    """
    click.echo(f"🔍 Validating module at: {path}")
    click.echo("⚠️  Validation feature coming soon...")

@cli.command()
def version():
    """Show version information."""
    click.echo("info_tech_cli version 0.1.0")
    click.echo("InfoTech.io Educational Platform CLI")
    click.echo("Author: A1eksMa <a1ex_ma@mail.ru>")

def main():
    """Entry point for the CLI application."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()