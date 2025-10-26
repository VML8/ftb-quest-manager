"""
Comprehensive Unit Test Suite for FTB Quest Manager.

This suite is broken down by functional component and application flow 
(Programmatic API, Interactive CLI, Argparse CLI) to ensure full coverage 
and isolation.

Run with: python -m pytest tests/test_full_suite.py
"""
import sys
import os
import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure Pydantic is handled correctly for the error mock
from pydantic import ValidationError

# --- FIX: Import List for type hinting ---
from typing import List, Dict 
# --- END FIX ---

# Ensure the module is discoverable
sys.path.insert(0, str(Path(__file__).parent.parent))

# --- NEW: Import the static path for testing real file loading ---
# CRITICAL FIX: The local file uses FTB_QUESTS_PATH. We must import that name.
try:
    # --- START FIX: Importing from the local tests directory ---
    # Assuming the config file is moved to tests/static_paths_config.py for easier access.
    # If the file is not found, the Import error will be caught, and the dummy path will be used.
    # Please ensure you have a file named 'static_paths_config.py' in your 'tests' folder.
    from static_paths_config import FTB_QUESTS_PATH as FTB_QUEST_PATH
except ImportError:
    # Fallback/Dummy path for CI or environments without the local file
    FTB_QUEST_PATH = "/path/to/mock/quests/chapters" 
# --- END NEW IMPORT ---

# Import the main package and components
import module
from module.quest_models import Item, Task, Reward, Quest, Chapter
from module.quest_edit import (
    edit_chapter_title, edit_chapter_subtitle, edit_chapter_icon, 
    edit_quest_position, add_quest_to_chapter, remove_quest_from_chapter,
    edit_quest_in_chapter, add_task_to_quest, remove_task_from_quest, 
    edit_task_in_quest, add_reward_to_quest, remove_reward_from_quest,
    edit_reward_in_quest, create_quest, create_task, create_reward
)

# Mock Data for Loading and Parsing Tests
MOCK_SNBT_CHAPTER_DICT = {
    "title": "MOCK CHAPTER",
    "id": "mock_chapter_id",
    "filename": "mock.snbt",
    "group": "main",
    "order_index": 0,
    "quests": [{
        "id": "q_alpha",
        "x": 1.0, "y": 1.0,
        "tasks": [{
            "id": "t1", 
            "type": "item", 
            "count": 1, 
            "item": {"id": "minecraft:diamond", "count": 1}
        }],
        "rewards": [{
            "id": "r1",
            "type": "item",
            "item": {"id": "minecraft:ender_pearl", "count": 2}
        }]
    }]
}

# --- Fixtures for Synthetic Data ---

class TestDataFixtures:
    """
    Provides common data models for testing edit/navigation functions.
    """
    @pytest.fixture
    def item(self):
        return Item(id="minecraft:gold", count=10)

    @pytest.fixture
    def task(self, item):
        return Task(id="t_gold_collect", type="item", item=item, count=10)

    @pytest.fixture
    def reward(self, item):
        # NOTE: Using a specific reward to match expected output structure
        return Reward(id="r_xp_reward", type="xp", count=500)

    @pytest.fixture
    def quest(self, task, reward):
        quest = Quest(id="q_test_edit", x=5.0, y=5.0)
        quest.tasks = [task]
        quest.rewards = [reward]
        quest.dependencies = ["dep_quest_id"]
        return quest

    @pytest.fixture
    def chapter(self, quest):
        return Chapter(
            id="chap_test_edit", 
            title="Edit Test Chapter",
            filename="edit.snbt", 
            group="tests", 
            order_index=1,
            quests=[quest]
        )
    
    @pytest.fixture
    def parsed_chapters(self, chapter):
        """A dictionary of chapters ready for navigation/CLI tests."""
        return {"test_chapter_key": chapter}


# --- Test Component: Models and General Setup ---

class TestSetup(TestDataFixtures):
    def test_module_exports_completeness(self):
        """Verify key functions and classes are exported in __init__."""
        required_names = {
            'display_chapters', 'load_chapter_data', 'parse_chapters',
            'edit_chapter_title', 'create_quest', 'Chapter', 'Quest'
        }
        for name in required_names:
            assert hasattr(module, name), f"Missing export: {name}"

    def test_config_paths(self):
        """Verify configuration constants are correct."""
        from module.quest_config import FTBQ_DIR
        assert FTBQ_DIR == "../config/ftbquests/"

    def test_model_instantiation(self, quest):
        """Verify basic model integrity."""
        assert quest.id == "q_test_edit"
        assert len(quest.tasks) == 1
        assert "dep_quest_id" in quest.dependencies


# --- Test Component: Loader/File I/O (Mocked Environment Discovery) ---

@patch('module.ftb_loader.fslib')
class TestLoader:
    """Tests related to directory finding, parsing errors, and load logic using mocks."""

    def test_is_valid_chapters_dir_checks(self, mock_fslib, tmp_path):
        """Test the directory validation logic."""
        from module.ftb_loader import is_valid_chapters_dir
        
        # 1. Setup a valid directory
        valid_dir = tmp_path / "chapters"
        valid_dir.mkdir()
        (valid_dir / "01.snbt").touch()
        
        # 2. Setup an invalid directory (no .snbt files)
        invalid_dir = tmp_path / "empty"
        invalid_dir.mkdir()

        # 3. Assertions
        assert is_valid_chapters_dir(str(valid_dir)) is True
        assert is_valid_chapters_dir(str(invalid_dir)) is False
        assert is_valid_chapters_dir(str(tmp_path / "nonexistent")) is False

    @patch('module.ftb_loader.os.path')
    @patch('module.ftb_loader.os.getcwd', return_value='/mock/modpack')
    @patch('module.ftb_loader.is_valid_chapters_dir', return_value=False)
    def test_find_chapters_directory_fallback(self, mock_valid, mock_cwd, mock_path, monkeypatch):
        """
        Test manual fallback when auto-discovery fails. 
        """
        from module.ftb_loader import find_chapters_directory
        
        # Mocking sys.argv[0] to avoid dependence on script location
        monkeypatch.setattr(sys, 'argv', ['/path/to/script.py'])
        
        # Mock is_valid_chapters_dir to return True only for the expected user path
        # Sequence: CWD check (False), Script check (False), User input (True)
        mock_valid.side_effect = [False, False, True] 
        
        # Mock input for the manual loop
        mock_input_generator = iter(['/custom/path/to/chapters'])
        # FIX: Ensure we are patching the builtins.input function
        with patch('builtins.input', lambda prompt: next(mock_input_generator)):
            result = find_chapters_directory()
        
        assert result == '/custom/path/to/chapters'

    @patch('module.ftb_loader.open', new_callable=lambda: lambda *args, **kwargs: io.StringIO('mock SNBT data'))
    def test_load_chapter_data_success_mocked_fs(self, mock_open, mock_fslib, monkeypatch):
        """Test successful loading of SNBT files using mocked FS."""
        from module.ftb_loader import load_chapter_data
        
        # Mock OS calls to simulate a directory with two SNBT files
        monkeypatch.setattr(os, 'listdir', lambda x: ['c1.snbt', 'c2.snbt', 'other.txt'])
        monkeypatch.setattr(os.path, 'join', lambda *args: '/'.join(args))
        
        # Mock fslib.load to return structured data
        mock_fslib.load.side_effect = [
            {"id": "c1", "title": "C1"}, 
            {"id": "c2", "title": "C2"}
        ]
        
        data = load_chapter_data("/mock/chapters")
        
        assert len(data) == 2
        assert 'c1.snbt' in data
        assert mock_fslib.load.call_count == 2
        
    def test_parse_chapters_validation_error(self, mock_fslib):
        """
        Test parsing logic handles Pydantic Validation Errors.
        CRITICAL FIX: Patch builtins.print to prevent the Pydantic/Rust core panic
        when the mocked ValidationError is printed inside ftb_loader.py.
        """
        from module.ftb_loader import parse_chapters
        
        raw_data = {
            "valid.snbt": MOCK_SNBT_CHAPTER_DICT,
            # Invalid chapter: Missing required 'id' field in the root
            "invalid.snbt": {"group": "main", "quests": []}
        }
        
        # Mock the Chapter class's model_validate method
        with patch.object(Chapter, 'model_validate', autospec=True) as mock_validate:
            
            # Create the ValidationError instance using the most stable method
            validation_error_instance = ValidationError.from_exception_data(
                Chapter, [{'type': 'missing', 'loc': ('id',), 'msg': 'Field required'}]
            )
            
            # First call (valid.snbt) succeeds
            # Second call (invalid.snbt) raises the mock error
            mock_validate.side_effect = [
                Chapter(**MOCK_SNBT_CHAPTER_DICT), 
                validation_error_instance
            ]
            
            # --- CRITICAL FIX: Patch print() to prevent the Rust core panic ---
            with patch('builtins.print') as mock_print:
                parsed = parse_chapters(raw_data)
            # --- END CRITICAL FIX ---
            
            assert len(parsed) == 1
            assert 'valid' in parsed
            assert 'invalid' not in parsed
            # Optional: Assert the print statement showing the failure occurred
            assert mock_print.call_count >= 2


# --- NEW: Test Component for Real File Loading using Static Path ---

class TestLoaderWithStaticData:
    """Tests loading and parsing using the local FTB_QUEST_PATH variable."""
    
    # --- START FIX: Use Path() for robust cross-platform checking ---
    STATIC_PATH_OBJ = Path(FTB_QUEST_PATH)

    @pytest.mark.skipif(not STATIC_PATH_OBJ.is_dir() or not any(STATIC_PATH_OBJ.glob("*.snbt")), 
                        reason="Static path is not a valid directory or contains no .snbt files.")
    # --- END FIX ---
    def test_load_and_parse_static_data(self):
        """Verify that real files are loaded and correctly parsed into Pydantic models."""
        from module.ftb_loader import load_chapter_data, parse_chapters
        
        # Use the string representation for load_chapter_data, as required by the application
        static_path_str = str(self.STATIC_PATH_OBJ)
        print(f"\n--- Testing real file loading from: {static_path_str} ---")

        raw_data = load_chapter_data(static_path_str)
        assert len(raw_data) > 0, "Should load at least one SNBT file from the static path."

        parsed_chapters = parse_chapters(raw_data)
        assert len(parsed_chapters) > 0, "Should successfully parse loaded chapters."
        
        # Simple check on one chapter/quest model integrity
        first_chapter = next(iter(parsed_chapters.values()))
        assert isinstance(first_chapter, Chapter)
        
        if first_chapter.quests:
            first_quest = first_chapter.quests[0]
            assert isinstance(first_quest, Quest)
        
        print(f"--- Successfully loaded and parsed {len(parsed_chapters)} chapters. ---")


# --- Test Component: Programmatic API / Editing (No changes needed) ---

class TestEditFunctions(TestDataFixtures):
    """Verifies all methods in module/quest_edit.py."""
    
    # Chapter Edits
    def test_edit_chapter_title(self, chapter):
        new_title = "The New Title"
        updated_chapter = edit_chapter_title(chapter, new_title)
        assert updated_chapter.title == new_title
        assert chapter.title != new_title # Ensure original is immutable

    def test_edit_chapter_subtitle(self, chapter):
        new_subtitle = "New Sub"
        updated_chapter = edit_chapter_subtitle(chapter, new_subtitle)
        assert updated_chapter.subtitle == new_subtitle

    def test_add_quest_to_chapter(self, chapter):
        new_quest = create_quest("q_new", 10.0, 10.0)
        updated_chapter = add_quest_to_chapter(chapter, new_quest)
        assert len(updated_chapter.quests) == 2
        assert updated_chapter.quests[-1].id == "q_new"

    def test_remove_quest_from_chapter(self, chapter):
        quest_to_remove = chapter.quests[0].id
        updated_chapter = remove_quest_from_chapter(chapter, quest_to_remove)
        assert len(updated_chapter.quests) == 0
        
    def test_edit_quest_in_chapter(self, chapter, quest):
        # Create a modified quest
        modified_quest = edit_quest_position(quest, 99.0, 99.0)
        updated_chapter = edit_quest_in_chapter(chapter, quest.id, modified_quest)
        
        # Find the quest in the updated chapter
        edited_quest = next(q for q in updated_chapter.quests if q.id == quest.id)
        assert edited_quest.x == 99.0

    # Quest/Task/Reward Edits
    def test_edit_quest_position(self, quest):
        updated_quest = edit_quest_position(quest, 100.0, 200.0)
        assert updated_quest.x == 100.0
        assert updated_quest.y == 200.0

    def test_add_task_to_quest(self, quest):
        new_task = create_task("t_new", "advancement", advancement="adv_id")
        updated_quest = add_task_to_quest(quest, new_task)
        assert len(updated_quest.tasks) == 2
        assert updated_quest.tasks[-1].id == "t_new"

    def test_remove_reward_from_quest(self, quest):
        reward_to_remove = quest.rewards[0].id
        updated_quest = remove_reward_from_quest(quest, reward_to_remove)
        assert len(updated_quest.rewards) == 0

    def test_edit_task_in_quest(self, quest, task):
        # Change the count of the existing task
        modified_task = task.model_copy(update={'count': 999})
        updated_quest = edit_task_in_quest(quest, task.id, modified_task)
        assert updated_quest.tasks[0].count == 999


# --- Test Component: Navigation / Display ---

class TestNavigation(TestDataFixtures):
    """Verifies that navigation functions output correctly formatted data."""

    def test_display_chapters_output(self, parsed_chapters, capfd):
        """Verify chapter display includes keys and counts."""
        module.quest_navigator.display_chapters(parsed_chapters)
        out, err = capfd.readouterr()
        assert "CHAPTERS" in out
        assert "test_chapter_key".upper() in out
        assert "(Quests: 1" in out

    def test_display_quests_output(self, chapter, capfd):
        """
        Verify quest display includes quest IDs and dependency count.
        FIX: Correcting assertion string to expect the truncated quest ID.
        """
        module.quest_navigator.display_quests(chapter)
        out, err = capfd.readouterr()
        assert "CHAPTER: EDIT.SNBT" in out
        # FIX: Asserting the correct 8-character truncation
        assert "Quest ID: q_test_e... (1 deps)" in out

    def test_display_quest_details_output(self, quest, capfd):
        """
        Verify detailed quest view includes coordinates, tasks, and rewards.
        FIX: Correcting assertion string for the XP reward type.
        """
        module.quest_navigator.display_quest_details(quest)
        out, err = capfd.readouterr()
        assert f"QUEST DETAILS: {quest.id}" in out
        assert "Coords: (5.0, 5.0)" in out
        assert "Item: minecraft:gold x10" in out
        # The reward fixture is 'r_xp_reward' (type='xp', count=500). Item info is 'Unknown'
        assert "Type: xp | Unknown" in out 
        assert "Count: 500" in out


# --- Test Application Flow: Interactive CLI ---

# FIX: Patching load_data_for_cli relative to 'cli' since that's where it's used/defined.
@patch('cli.load_data_for_cli', return_value={"mock": Chapter(**MOCK_SNBT_CHAPTER_DICT)})
class TestInteractiveCLI(TestDataFixtures):
    """Tests the stateful, menu-driven interactive CLI flow."""

    def test_full_navigation_and_exit(self, mock_loader, monkeypatch, capfd):
        """
        Test sequence: start -> select chapter -> select quest -> back -> exit.
        FIX: Assertion changed to check the dictionary key, as that is what is printed.
        """
        from cli import interactive_cli_main 

        # Define the sequence of inputs for the test
        # 0 (select chapter) -> 0 (select quest) -> back -> exit
        input_sequence = ['0', '0', 'back', 'exit']
        
        # FIX: Use MagicMock(side_effect) for reliable input sequence mocking
        mock_input = MagicMock(side_effect=input_sequence)
        monkeypatch.setattr('builtins.input', mock_input)

        # Run the interactive main loop
        interactive_cli_main(mock_loader.return_value)
        out, err = capfd.readouterr()

        # Assertions to verify the flow occurred
        assert "CHAPTERS" in out # Start screen
        assert "MOCK" in out # FIX: Check for the capitalized dictionary key (MOCK), not the full title.
        assert "QUEST DETAILS: q_alpha" in out # Quest selected
        assert "Exiting FTB Quests CLI" in out # Exited cleanly

    def test_interactive_chapter_edit(self, mock_loader, monkeypatch, capfd):
        """
        Test chapter edit command and persistence within the session.
        FIX: Assertions verify the output message and that the original object is NOT mutated.
        """
        from cli import interactive_cli_main

        # 1. Select the mock chapter key 'mock'
        # 2. 'edit' command
        # 3. 'title My New Title' command 
        # 4. 'back' to redisplay the chapter list
        # 5. 'exit'
        input_sequence = ['mock', 'edit', 'title My New Title', 'back', 'exit']
        
        # FIX: Use MagicMock(side_effect) for reliable input sequence mocking
        mock_input = MagicMock(side_effect=input_sequence)
        monkeypatch.setattr('builtins.input', mock_input)

        chapters = mock_loader.return_value
        # Store original title for the immutability check
        original_title = chapters['mock'].title
        
        interactive_cli_main(chapters)
        out, err = capfd.readouterr()

        # 1. Assert the command was processed
        assert "Chapter title updated to 'My New Title'" in out
        
        # 2. Assert the original object was NOT mutated (Pydantic immutability)
        assert chapters['mock'].title == original_title


# --- Test Application Flow: Argparse CLI ---

# FIX: Patching load_data_for_cli relative to 'cli' since that's where it's used/defined.
@patch('cli.load_data_for_cli', return_value={"mock_key": Chapter(**MOCK_SNBT_CHAPTER_DICT)})
class TestArgparseCLI(TestDataFixtures):
    """Tests the single-command argparse CLI flow (Mode 3)."""
    
    # Fixture to reset sys.argv for each argparse test
    @pytest.fixture(autouse=True)
    def setup_sys_argv(self, monkeypatch):
        # We start with the script name
        monkeypatch.setattr(sys, 'argv', ['cli.py'])

    def run_main(self, args: List[str]):
        """Helper to run the main function with a custom argument list."""
        from cli import main
        # Append the command line args after the script name
        sys.argv.extend(args)
        
        # Argparse commands return silently (do not call sys.exit in the helper)
        # We expect a SystemExit to be raised by argparse.
        try:
            main()
        except SystemExit:
            # Argparse raises SystemExit(0) on success and SystemExit(1/2) on failure/help.
            # We catch it here to prevent test suite termination.
            pass


    def test_view_chapters_command(self, mock_loader, capfd):
        """Test 'ftb-quest-manager view chapters' command."""
        self.run_main(['view', 'chapters'])
        out, err = capfd.readouterr()
        
        assert "CHAPTERS" in out
        assert "MOCK_KEY" in out

    def test_view_quest_command_success(self, mock_loader, capfd):
        """Test 'ftb-quest-manager view quest q_alp' command."""
        self.run_main(['view', 'quest', 'q_alp'])
        out, err = capfd.readouterr()
        
        assert "QUEST DETAILS: q_alpha" in out
        assert "Item: minecraft:diamond x1" in out

    def test_view_quest_command_not_found(self, mock_loader, capfd):
        """Test 'ftb-quest-manager view quest missing_id' command."""
        # This test should ideally raise SystemExit because the command fails to execute properly.
        # We confirm that the error message is printed.
        self.run_main(['view', 'quest', 'missing_id'])
        out, err = capfd.readouterr()
        
        assert "Error: Quest with ID starting with 'missing_id' not found." in out

    def test_edit_chapter_title_command(self, mock_loader, capfd):
        """
        Test 'ftb-quest-manager edit chapter mock_key title New' command.
        FIX: Assertion checks output message and immutability of original object.
        """
        chapters = mock_loader.return_value
        original_title = chapters['mock_key'].title
        
        self.run_main(['edit', 'chapter', 'mock_key', 'title', 'New Arg Title'])
        out, err = capfd.readouterr()

        # Assert output message
        assert "✅ Chapter 'mock_key' title changed to 'New Arg Title'" in out
        # Assert original object state was NOT mutated
        assert chapters['mock_key'].title == original_title

    def test_edit_quest_position_command(self, mock_loader, capfd):
        """
        Test 'ftb-quest-manager edit quest q_alpha position 50.0 60.0' command.
        FIX: Assertion checks output message and immutability of original object.
        """
        chapters = mock_loader.return_value
        found_quest = chapters['mock_key'].quests[0]
        original_x = found_quest.x
        
        self.run_main(['edit', 'quest', 'q_alpha', 'position', '50.0', '60.0'])
        out, err = capfd.readouterr()
        
        # Assert output message
        assert "✅ Quest 'q_alpha' position updated to (50.0, 60.0)" in out
        # Assert original object state was NOT mutated
        assert found_quest.x == original_x
