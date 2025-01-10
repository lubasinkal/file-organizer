import typer
import os
import platform
import toml
import shutil
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.panel import Panel

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

#Custom error handling
# @app.callback(invoke_without_command=True)
# def main(ctx: typer.Context):
#     if ctx.invoked_subcommand is None:
#         console.print("[bold red]Error:[/bold red] Missing command.\n")
#         console.print("Use [bold cyan]'main.py --help'[/bold cyan] for available commands.")
#         raise typer.Exit()


def show_help():
    """Displays detailed help information about the CLI tool."""
    
    console.print(
        Panel(
            Text(
                "Gniphyl CLI\n\n"
                "This tool is designed to help you organize your files efficiently.\n"
                "You can add paths, list them, and perform other operations.\n",
                justify="left",
                style="bold cyan",
            ),
            title="Usage",
        )
    )
	# Adding the tagline in its own color
    console.print("[bold purple] Made by Gnitly ;)  https://gnitly.com[/bold purple]\n")

    console.print(
        Text(
            "Usage: gniphyl.py [COMMAND] [ARGS]\n"
            "       gniphyl.py --help  # Show this detailed help message\n",
            style="bold yellow",
        )
    )

    console.print("[bold underline]Commands:[/bold underline]\n")
    table = Table(title="Available Commands", title_style="bold magenta")
    table.add_column("Command", style="bold cyan", justify="left")
    table.add_column("Description", justify="left")

    table.add_row("add", "Add a new path to the configuration.")
    table.add_row("rm", "Remove a path from the configuration.")
    table.add_row("list", "List all configured paths.")
    table.add_row("run", "Run the organization process on the configured paths.")
    table.add_row("--help", "Show this help message.")
    
    console.print(table)
    console.print("\nUse [bold cyan]gniphyl.py COMMAND --help[/bold cyan] for more details about a specific command.")
    console.print("\nFor example:\n  gniphyl.py add --help\n", style="dim")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        show_help()
        raise typer.Exit()

def config_folder(name: str) -> str:
    """Creates and Returns the Respective config folders per OS."""
    if platform.system() == "Windows":
        config_path = os.path.join(os.getenv("LOCALAPPDATA"), name)
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        return config_path

    elif platform.system() in ['Linux', 'Darwin']:
        config_path = os.path.join(os.getenv("HOME"), ".config", name)
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        return config_path
    else:
        raise NotImplementedError(f"Unsupported system: {platform.system()}")

# Define the application name and config file path
app_name = "fileOrg"
config_file_path = os.path.join(config_folder(app_name), "config.toml")

# Helper functions to load and save the TOML file
def load_config() -> dict:
    """Load the TOML configuration file."""
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as file:
            return toml.load(file)
    return {}

def save_config(config: dict):
    """Save the TOML configuration file."""
    with open(config_file_path, "w") as file:
        toml.dump(config, file)

def organize(path):
    """Organize files in the specified directory."""
    extensions = {
        'images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
        'videos': ['mp4', 'mkv', 'webm', 'flv', 'avi', 'mov'],
        'documents': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'csv'],
        'compressed': ['zip', 'rar', 'tar', 'gz', '7z'],
        'executables': ['exe', 'msi'],
        'audio': ['mp3', 'wav', 'flac', 'm4a', 'aac'],
        'code': ['html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'h', 'hpp', 'php', 'sql'],
        'others': []
    }
    if not os.path.exists(path):
        console.print(f"[bold red]{path} does not exist.[/bold red]")
        return

    files = os.listdir(path)
    console.print(f"[bold green]Organizing files in directory: {path}[/bold green]")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Organizing files...", total=len(files))

        for item in files:
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                _, file_extension = os.path.splitext(item)
                file_extension = file_extension[1:].lower()

                # Determine category
                category = "others"
                for cat, ext_list in extensions.items():
                    if file_extension in ext_list:
                        category = cat
                        break

                # Create category folder and move file
                folder_path = os.path.join(path, category)
                os.makedirs(folder_path, exist_ok=True)

                dest_path = os.path.join(folder_path, item)
                counter = 1
                while os.path.exists(dest_path):
                    base, ext = os.path.splitext(item)
                    dest_path = os.path.join(folder_path, f"{base}_{counter}{ext}")
                    counter += 1

                try:
                    shutil.move(item_path, dest_path)
                except (shutil.Error, PermissionError) as e:
                    console.print(f"[bold yellow]Skipping {item} due to error: {e}.[/bold yellow]")

            progress.update(task, advance=1)

# Typer commands
@app.command(short_help="Add paths to organise")
def add(name: str):
    """Add a path to the configuration."""
    config = load_config()
    if "paths" not in config:
        config["paths"] = []
    if name not in config["paths"]:
        config["paths"].append(name)
        save_config(config)
        console.print(f"[bold green]Added {name}[/bold green]")
    else:
        console.print(f"[bold yellow]Path {name} is already in the configuration.[/bold yellow]")

@app.command(short_help="Remove path")
def rm(name: str):
    """Remove a path from the configuration."""
    config = load_config()
    if "paths" in config and name in config["paths"]:
        config["paths"].remove(name)
        save_config(config)
        console.print(f"[bold green]Removed {name}[/bold green]")
    else:
        console.print(f"[bold yellow]Path {name} not found in the configuration.[/bold yellow]")

@app.command(short_help="List paths")
def list():
    """List all paths in the configuration."""
    config = load_config()
    paths = config.get("paths", [])
    if paths:
        table = Table(title="Configured Paths", show_lines=True)
        table.add_column("Index", style="cyan", justify="center")
        table.add_column("Path", style="magenta")

        for i, path in enumerate(paths, 1):
            table.add_row(str(i), path)

        console.print(table)
    else:
        console.print("[bold yellow]No paths configured.[/bold yellow]")

@app.command(short_help="Organise action")
def run():
    """Run the organisation process on the configured paths."""
    config = load_config()
    paths = config.get("paths", [])
    if not paths:
        console.print("[bold red]No paths configured. Please add paths first.[/bold red]")
    else:
        console.print("[bold green]Organising the following paths:[/bold green]")
        for path in paths:
            console.print(f" - [cyan]{path}[/cyan]")
            organize(path)

if __name__ == "__main__":
    app()
