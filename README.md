The README file has been renewed based on the current project structure, ensuring the file paths and module names align with the uploaded code.

# FTB Quest Viewer

A Python tool for viewing and navigating FTB (Feed The Beast) quest data from Minecraft modpacks. This tool parses SNBT quest and language files and provides an interactive, modular command-line interface to explore quest chapters, individual quests, tasks, and rewards.

## Features

- **Localization Support (New in 1.1.0):** Automatically loads quest titles and names from the `en_us.snbt` language file for a localized experience.
- **Interactive Navigation:** Browse quest chapters and individual quests with a modular, user-friendly command-line interface.
- **Detailed Quest Information:** View comprehensive quest details including coordinates, dependencies, and settings, displayed with color-coded clarity.
- **Task & Reward Analysis:** Drill down into specific tasks and rewards with detailed information including:
  - Item requirements and rewards with quantities
  - Task types and optional status
  - Advancement requirements
  - Item components and metadata
- **SNBT File Support:** Automatically loads and parses FTB quest data from SNBT files.

***

## Installation

### From Source

1. Clone or download the repository
2. Navigate to the Quest Manager directory
3. Install dependencies (Requires Python 3.10+):
```bash
   pip install -r requirements.txt
```

4.  Run the application:
    ```bash
    python cli.py
    ```

### As a Package

1.  Install the package:
    ```bash
    pip install .
    ```
2.  Run the viewer:
    ```bash
    ftb-quest-manager
    # or alternatively:
    ftb-manager
    ```

### Development Installation

For development with editable installs:

```bash
pip install -e .
```

-----

## Usage

### Command-Line Interface

The application provides a hierarchical navigation system via the main `cli:main` entry point. Run the command without arguments for interactive mode, or with arguments for quick lookups (e.g., `ftb-quest-manager view chapters`).

1.  **Chapter Selection**: Choose from available quest chapters
2.  **Quest Selection**: Browse individual quests within a chapter
3.  **Detail View**: Explore detailed information about quests, tasks, and rewards

#### Navigation Commands (Interactive Mode)

  - `exit` or `quit`: Exit the application
  - `back`: Return to the previous level
  - `task <number>`: View detailed information about a specific task (e.g., `task 0`)
  - `reward <number>`: View detailed information about a specific reward (e.g., `reward 1`)
  - `edit`: Enter the edit sub-menu for the current chapter or quest (functionality is limited in the current version).

### Programmatic Usage

The package exposes Pydantic models and utility functions for programmatic use:

```python
from module import load_chapter_data, parse_chapters, load_language_data
from module.model.quest_models import Chapter, Quest # Note: Model classes are in module.model

# 1. Load data
chapters_dir = find_chapters_directory()
raw_data = load_chapter_data(chapters_dir)
lang_data = load_language_data(chapters_dir) # Load localization data

# 2. Parse into Pydantic models
chapters = parse_chapters(raw_data, lang_data)

# Access quest data directly
chapter: Chapter = chapters['chapter_key']
for quest in chapter.quests:
    print(f"Title: {quest.title}")
    print(f"Tasks: {len(quest.tasks)}")
```

### Data Models

The package provides Pydantic models for type-safe quest data in `module/model/quest_models.py`.

```python
from module.model.quest_models import Quest, Chapter, Task, Reward, Item

# Access quest properties
quest: Quest = chapter.quests[0]
print(f"Quest Title: {quest.title}")
print(f"Position: ({quest.x}, {quest.y})")
print(f"Dependencies: {quest.dependencies}")
```

-----

## Configuration

The application automatically attempts to find quest data. It looks for the chapters directory and the language file based on the script's location or current working directory. The default path definition is maintained in `module/controller/quest_config.py`:

```python
# Modify these constants to adjust file discovery if necessary
FTBQ_DIR = "../config/ftbquests/"
LANG_DIR = "../config/ftbquests/quests/lang/en_us.snbt"
```

-----

## Requirements

  - Python **3.10+** (Required by `python_requires`)
  - pydantic\>=2.0.0
  - ftb-snbt-lib==0.4.0
  - colorama\>=0.4.6

-----

## Project Structure

The project follows a modified Model-View-Controller (MVC) pattern, separating data models, display logic, and control/loading logic.

```
Quest Manager/
├── module/                 # Main Python package
│   ├── __init__.py         # Package initialization and exports
│   ├── __main__.py         # Entry point for module execution
│   ├── controller/         # Business logic and file I/O
│   │   ├── ftb_loader.py   # SNBT file loading and parsing (includes lang file logic)
│   │   ├── quest_config.py # Configuration constants
│   │   └── quest_edit.py   # Data editing functions
│   ├── model/              # Pydantic data models
│   │   └── quest_models.py # Chapter, Quest, Task, Reward, Item models
│   └── view/               # Display and presentation logic
│       ├── display_chapters.py # Chapter list display
│       ├── display_quests.py   # Quest list and detail display
│       └── display_task_reward.py # Task and reward detail display
├── tests/                  # Unit tests directory
│   └── test_full_suite.py  # Comprehensive test suite
├── cli.py                  # Main command-line entry point
├── pyproject.toml          # Modern Python packaging configuration
├── setup.py                # Setuptools configuration
├── requirements.txt        # Python dependencies
├── LICENSE                 # Project license (MIT)
└── README.md
```

-----

## Development

### Running Tests

```bash
# Unit tests (pytest format)
pytest tests/
```

### Building the Package

```bash
# Build distribution packages
python -m build
```

-----

## License

MIT License - see [LICENSE](https://www.google.com/search?q=vml8/ftb-quest-manager/ftb-quest-manager-b4673cda0a5fde99923584b5cebae8ef495beb4d/LICENSE) file for details.

-----

## Contributing

1.  Fork the repository
2.  Create a feature branch
3.  Make your changes
4.  Add tests if applicable
5.  Submit a pull request

-----

## Support

For issues, questions, or contributions, please:

  - Check the Issues page on GitHub
  - Create a new issue with detailed information
  - Include your Python version and FTB modpack version

-----

## Changelog

### Version 1.1.0 \<- New Minor Release

  - ✅ **Feature:** Implemented logic to find and inject localized Quest Titles from `en_us.snbt` into models.
  - ✅ **Refactor (MVC Writeover):** Modularized interactive CLI logic in `cli.py` for improved readability.
  - ✅ **Refactor:** Renamed viewing logic from `view` to `display` across functions and files (e.g., `quest_navigator.py`).
  - ✅ **Fix:** Resolved `TypeError` in quest display by converting the dependency list to a string (`", ".join()`).
  - ✅ **Fix:** Updated path logic for robust cross-platform language file discovery.

### Version 1.0.1

  - ✅ Fixed config directory paths for Quest Manager structure
  - ✅ Added comprehensive test suite (`test_package.py`, `quick_test.py`)
  - ✅ Added unit tests (`tests/test_module.py`)
  - ✅ Updated documentation with testing instructions
  - ✅ Restructured package into Quest Manager folder
  - ✅ Corrected main script reference to `cli.py` and noted entry point discrepancies

### Version 1.0.0

  - Initial release
  - Interactive quest navigation
  - Detailed task and reward viewing
  - SNBT file parsing
  - Command-line interface

<!-- end list -->

```
```
