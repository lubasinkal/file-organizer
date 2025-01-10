import typer
import os
import platform
import toml
import shutil
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

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

# Initialize Typer app
app = typer.Typer()

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
        print(f"{path} does not exist.")
        return

    files = os.listdir(path)
    print(f"Organizing files in directory: {path}")

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
                print(f"Skipping {item} due to error: {e}.")

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
        print(f"Added {name}")
    else:
        print(f"Path {name} is already in the configuration.")

@app.command(short_help="Remove path")
def rm(name: str):
    """Remove a path from the configuration."""
    config = load_config()
    if "paths" in config and name in config["paths"]:
        config["paths"].remove(name)
        save_config(config)
        print(f"Removed {name}")
    else:
        print(f"Path {name} not found in the configuration.")

@app.command(short_help="List paths")
def list():
    """List all paths in the configuration."""
    config = load_config()
    paths = config.get("paths", [])
    if paths:
        print("Configured paths:")
        for path in paths:
            print(f" - {path}")
    else:
        print("No paths configured.")

@app.command(short_help="Organise action")
def run():
    """Run the organisation process on the configured paths."""
    config = load_config()
    paths = config.get("paths", [])
    if not paths:
        print("No paths configured. Please add paths first.")
    else:
        print("Organising the following paths:")
        for path in paths:
            print(f" - {path}")
            organize(path)

if __name__ == "__main__":
    app()
