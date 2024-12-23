import os
import shutil
import sqlite3
import sys

# Create a database connection and a cursor
conn = sqlite3.connect('config.db')
cursor = conn.cursor()

# Create a table to store configurable paths
cursor.execute('''
CREATE TABLE IF NOT EXISTS paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL
)
''')

# Function to add a new path to the database
def add_path(path):
    if not os.path.exists(path):
        print(f"The path '{path}' does not exist. Please provide a valid path.")
        return
    cursor.execute('INSERT INTO paths (path) VALUES (?)', (path,))
    conn.commit()
    print(f"Path '{path}' has been added.")

# Function to get all paths from the database
def get_paths():
    cursor.execute('SELECT id, path FROM paths')
    return cursor.fetchall()

# Function to delete a path from the database by index
def delete_path_by_index(index):
    paths = get_paths()
    if index < 1 or index > len(paths):
        print(f"Invalid index: {index}. Please provide a valid index number.")
        return
    path_id = paths[index - 1][0]
    cursor.execute('DELETE FROM paths WHERE id = ?', (path_id,))
    conn.commit()
    print(f"Path '{paths[index - 1][1]}' has been deleted.")

# Function to organize files in a directory
def organize_files(directory):
    extensions = {
        'images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
        'videos': ['mp4', 'mkv', 'webm', 'flv', 'avi', 'mov'],
        'documents': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'],
        'compressed': ['zip', 'rar', 'tar', 'gz', '7z'],
        'executables': ['exe', 'msi'],
        'audio': ['mp3', 'wav', 'flac', 'm4a', 'aac'],
        'code': ['html', 'css', 'js', 'py', 'java', 'c', 'cpp', 'h', 'hpp', 'php', 'sql'],
        'others': []
    }

    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist. Skipping.")
        return

    files = os.listdir(directory)
    print(f"Organizing files in directory: {directory}")

    for item in files:
        if os.path.isfile(os.path.join(directory, item)):
            filename, file_extension = os.path.splitext(item)
            file_extension = file_extension[1:]

            for category, extension in extensions.items():
                if file_extension in extension:
                    folder_path = os.path.join(directory, category)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    dest_path = os.path.join(folder_path, item)
                    if os.path.exists(dest_path):
                        base, extension = os.path.splitext(item)
                        counter = 1
                        new_name = f"{base}_{counter}{extension}"
                        dest_path = os.path.join(folder_path, new_name)
                        while os.path.exists(dest_path):
                            counter += 1
                            new_name = f"{base}_{counter}{extension}"
                            dest_path = os.path.join(folder_path, new_name)
                    try:
                        shutil.move(os.path.join(directory, item), dest_path)
                    except shutil.Error as e:
                        print(f"Skipping {item} because {e}.")
                    except PermissionError:
                        print(f"Skipping {item} because it is in use.")
                    break
            else:
                folder_path = os.path.join(directory, 'others')
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                dest_path = os.path.join(folder_path, item)
                if os.path.exists(dest_path):
                    base, extension = os.path.splitext(item)
                    counter = 1
                    new_name = f"{base}_{counter}{extension}"
                    dest_path = os.path.join(folder_path, new_name)
                    while os.path.exists(dest_path):
                        counter += 1
                        new_name = f"{base}_{counter}{extension}"
                        dest_path = os.path.join(folder_path, new_name)
                try:
                    shutil.move(os.path.join(directory, item), dest_path)
                except shutil.Error as e:
                    print(f"Skipping {item} because {e}.")
                except PermissionError:
                    print(f"Skipping {item} because it is in use.")

# Command-line interface
if len(sys.argv) > 1:
    command = sys.argv[1].lower()

    if command == 'addpath':
        if len(sys.argv) == 3:
            add_path(sys.argv[2])
        else:
            print("Usage: main.py addpath <directory_path>")
    elif command == 'deletepath':
        if len(sys.argv) == 3 and sys.argv[2].isdigit():
            delete_path_by_index(int(sys.argv[2]))
        else:
            print("Usage: main.py deletepath <index>")
    elif command == 'listpaths':
        paths = get_paths()
        if paths:
            print("Configured paths:")
            for idx, (path_id, path) in enumerate(paths, start=1):
                print(f"{idx}. {path}")
        else:
            print("No paths configured.")
    elif command == 'organize':
        paths = get_paths()
        if paths:
            for _, path in paths:
                organize_files(path)
        else:
            print("No paths configured. Use 'addpath' to add a directory.")
    else:
        print("Unknown command. Available commands: addpath, deletepath, listpaths, organize")
else:
    print("Usage: organize-files <command>")
    print("Commands:")
    print("  addpath <directory_path>   Add a new directory path.")
    print("  deletepath <index>         Delete a directory path by index.")
    print("  listpaths                  List all configured paths.")
    print("  organize                   Organize files in all configured paths.")

# Close the database connection
conn.close()
