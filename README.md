# FTB Quest Viewer

A Python tool for viewing and navigating FTB (Feed The Beast) quest data from Minecraft modpacks. This tool parses SNBT quest files and provides an interactive command-line interface to explore quest chapters, individual quests, tasks, and rewards.

## Features

- **Interactive Navigation**: Browse quest chapters and individual quests with a user-friendly command-line interface
- **Detailed Quest Information**: View comprehensive quest details including coordinates, dependencies, and settings
- **Task & Reward Analysis**: Drill down into specific tasks and rewards with detailed information including:
  - Item requirements and rewards with quantities
  - Task types and optional status
  - Advancement requirements
  - Item components and metadata
- **SNBT File Support**: Automatically loads and parses FTB quest data from SNBT files
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Installation

### From Source

1. Clone or download the repository
2. Navigate to the Quest Manager directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Note: If requirements.txt is empty, install from pyproject.toml dependencies: `pip install pydantic>=2.0.0 ftb_snbt_lib>=1.0.0`
4. Run the application:
   ```bash
   python cli.py
   ```

### As a Package

1. Install the package:
   ```bash
   pip install .
   ```
2. Run the viewer:
   ```bash
   ftb-quest-viewer
   # or alternatively:
   ftb-viewer
   ```

### Development Installation

For development with editable installs:
```bash
pip install -e .
```

## Usage

### Command-Line Interface

The application provides a hierarchical navigation system:

1. **Chapter Selection**: Choose from available quest chapters
2. **Quest Selection**: Browse individual quests within a chapter
3. **Detail View**: Explore detailed information about quests, tasks, and rewards

#### Navigation Commands

- `exit` or `quit`: Exit the application
- `back`: Return to the previous level
- `TASKS <number>`: View detailed information about a specific task (e.g., `TASKS 0`)
- `REWARDS <number>`: View detailed information about a specific reward (e.g., `REWARDS 1`)

### Programmatic Usage

You can also use the package programmatically:

```python
from module import load_chapter_data, parse_chapters, view_chapters

# Load quest data
raw_data = load_chapter_data()
chapters = parse_chapters(raw_data)

# Navigate chapters
chapter = view_chapters(chapters)

# Access quest data directly
for quest in chapter.quests:
    print(f"Quest: {quest.id}")
    print(f"Tasks: {len(quest.tasks)}")
    print(f"Rewards: {len(quest.rewards)}")
```

### Data Models

The package provides Pydantic models for type-safe quest data:

```python
from module import Quest, Chapter, Task, Reward, Item

# Access quest properties
quest: Quest = chapter.quests[0]
print(f"Quest ID: {quest.id}")
print(f"Position: ({quest.x}, {quest.y})")
print(f"Dependencies: {quest.dependencies}")

# Access task details
for task in quest.tasks:
    print(f"Task Type: {task.type}")
    print(f"Count: {task.count}")
    if task.item:
        print(f"Item: {task.item.id} x{task.item.count}")

# Access reward details
for reward in quest.rewards:
    print(f"Reward Type: {reward.type}")
    if reward.item:
        print(f"Item: {reward.item.id} x{reward.item.count}")
```

## Configuration

The application looks for quest data in the `../config/ftbquests/` directory by default (relative to the Quest Manager folder). You can modify this in `module/quest_config.py`:

```python
# Modify the FTBQ_DIR constant to point to your quest directory
FTBQ_DIR = "../path/to/your/ftbquests/"
```

## Requirements

- Python 3.8+
- pydantic>=2.0.0
- ftb_snbt_lib>=1.0.0

## Project Structure

```
Quest Manager/
├── module/                 # Main package directory
│   ├── __init__.py        # Package initialization and exports
│   ├── quest_models.py    # Pydantic data models
│   ├── quest_navigator.py # Navigation and display logic
│   ├── ftb_loader.py      # SNBT file loading and parsing
│   └── quest_config.py    # Configuration constants
├── tests/                 # Unit tests directory
│   ├── __init__.py
│   └── test_module.py     # pytest-style tests
├── cli.py                 # Main entry point script
├── test_package.py        # Comprehensive test suite
├── quick_test.py          # Quick verification script
├── pyproject.toml         # Modern Python packaging configuration
├── setup.py              # Fallback packaging configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Development

### Running Tests

The package includes comprehensive test suites:

```bash
# Quick verification (recommended)
python quick_test.py

# Comprehensive testing
python test_package.py

# Unit tests (pytest format)
python -m pytest tests/
# or if pytest is installed:
pytest tests/

# Or run the main application directly
python cli.py
```

### Building the Package

```bash
# Build distribution packages
python -m build

# Or with setuptools
python setup.py sdist bdist_wheel
```

### Adding New Features

1. Add functionality to the appropriate module in `module/`
2. Update the `__init__.py` to export new functions/classes
3. Add tests in `tests/test_module.py`
4. Update documentation in README.md
5. Update version in `__init__.py` and `pyproject.toml`

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues, questions, or contributions, please:
- Check the Issues page on GitHub
- Create a new issue with detailed information
- Include your Python version and FTB modpack version

## Changelog

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
