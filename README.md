# File Organizer

File Organizer is a Python-based tool designed to manage and organize files within specified directories. It provides a command-line interface to add, delete, list, and organize directories, ensuring your files are neatly sorted based on their type.

---

## Features

- Add directory paths to a database.
- Delete paths by their index.
- List all configured paths.
- Organize files in directories into categorized folders based on their extensions.

---

## Installation

### Prerequisites
- Python 3.6 or higher
- SQLite (pre-installed with Python)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/lubasinkal/file-organizer.git
   cd file-organizer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python main.py
   ```

---

## Usage

Run the tool from the command line using the following commands:

### Add a New Path
```bash
python main.py addpath <directory_path>
```
Adds a directory path to the database.

### Delete a Path
```bash
python main.py deletepath <index>
```
Deletes a path by its index number (use `listpaths` to see indices).

### List All Paths
```bash
python main.py listpaths
```
Lists all paths stored in the database.

### Organize Files
```bash
python main.py organize
```
Organizes files in all configured paths into categorized folders (e.g., `images`, `videos`, etc.).

---

## Example

1. Add a new path:
   ```bash
   python main.py addpath C:\Users\YourName\Downloads
   ```
2. List paths:
   ```bash
   python main.py listpaths
   ```
   Output:
   ```
   Configured paths:
   1. C:\Users\YourName\Downloads
   ```
3. Organize files in the paths:
   ```bash
   python main.py organize
   ```

---

## Releases

The compiled executable and installer are available in the [Releases](https://github.com/lubasinkal/file-organizer/releases) section.

---

## Contributing

Contributions are welcome! Feel free to fork this repository, make improvements, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or issues, please contact:
- **Name:** Lubasi Nkalolang
- **Email:** lubasinkal@outlook.com
- **GitHub:** [your-username](https://github.com/lubasinkal)
