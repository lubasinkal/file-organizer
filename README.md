# Gniphyl

Gniphyl is a cross-platform command-line interface (CLI) tool that allows users to organize files within specified directories. It enables users to add, delete, list, and organize directories, ensuring that files are neatly sorted based on their type (e.g., `images`, `videos`, `documents`). This tool is available as an executable for **Windows**, **macOS**, and **Linux**.

---

## Features

- Add directory paths to a configuration file.
- Delete paths by their index.
- List all configured paths.
- Organize files into categorized folders based on their extensions (e.g., `images`, `videos`, `documents`).

---

## Installation

### Prerequisites
- No installation of Python required if using the precompiled executables.
- For **Windows**, **macOS**, and **Linux**, you can download the respective executables.
- To build from source, ensure **Python 3.6** or higher is installed.

### Steps to Install the Executables

1. **Clone the repository** (only required if you plan to build from source):
   ```bash
   git clone https://github.com/lubasinkal/gniphyl.git
   cd gniphyl
   ```

2. **Install dependencies** (if building from source):
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Executables** from the [Releases](https://github.com/lubasinkal/gniphyl/releases) section:

   - **For Windows**: Download `gniphyl.exe`.
   - **For macOS**: Download `gniphyl`.
   - **For Linux**: Download `gniphyl-linux`.

4. **Move Executables to a Directory in the PATH**:

   To make it easier to run the `gniphyl` commands from any terminal session, move the downloaded executable to a directory that is part of your system's `PATH`.

   #### On **Windows**:
   - Move `gniphyl.exe` to a directory like `C:\Windows\System32` or another directory already in your system’s `PATH`.
   - Alternatively, add the directory where `gniphyl.exe` is located to your system’s `PATH` environment variable.

     To add a directory to the `PATH`:
     1. Right-click on **This PC** or **Computer** and select **Properties**.
     2. Select **Advanced system settings**.
     3. Click the **Environment Variables** button.
     4. In the **System variables** section, scroll to find the `Path` variable and click **Edit**.
     5. Add the path to the directory containing `gniphyl.exe` and click **OK**.

   #### On **macOS** and **Linux**:
   - Move the executable to `/usr/local/bin` (or another directory in your system’s `PATH`).
     ```bash
     sudo mv gniphyl /usr/local/bin/
     ```
     For **Linux**:
     ```bash
     sudo mv gniphyl-linux /usr/local/bin/
     ```
   - Ensure the executable is accessible by running:
     ```bash
     sudo chmod +x /usr/local/bin/gniphyl
     ```

     For **Linux**:
     ```bash
     sudo chmod +x /usr/local/bin/gniphyl-linux
     ```

---

## Usage

### Run as a CLI Tool

The tool is a command-line utility, which means it is run from the terminal/command prompt. Use the following commands to interact with the tool:

### Add a New Path
```bash
gniphyl add <directory_path>
```
Adds a directory path to the configuration.

### Delete a Path
```bash
gniphyl rm <index>
```
Deletes a path by its index number (use `gniphyl list` to see indices).

### List All Paths
```bash
gniphyl list
```
Lists all paths stored in the configuration.

### Organize Files
```bash
gniphyl run
```
Organizes files in all configured paths into categorized folders (e.g., `images`, `videos`, etc.).

---

## Example

1. Add a new path:
   ```bash
   gniphyl add /users/name/downloads
   ```

2. List paths:
   ```bash
   gniphyl list
   ```
   Output:
   ```
   Configured paths:
   1. /users/name/downloads
   ```

3. Organize files in the paths:
   ```bash
   gniphyl run
   ```

---

## Releases

The compiled executables for each platform are available in the [Releases](https://github.com/lubasinkal/gniphyl/releases) section. You can download the appropriate file for your operating system.

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
- **GitHub:** [lubasinkal](https://github.com/lubasinkal)