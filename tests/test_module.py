"""
Modularized Unit tests for FTB Quest Manager module.

Run with: python -m pytest tests/test_module.py
"""

import sys
import pytest
from pathlib import Path

# Add the parent directory to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all necessary components
import module
from module.quest_models import Item, Task, Reward, Quest, Chapter
from module.quest_edit import edit_chapter_title, add_quest_to_chapter, create_quest, edit_quest_position, create_task, create_chapter


class TestData:
    """Fixture class to provide common test data."""
    @pytest.fixture
    def test_item(self):
        return Item(id="minecraft:diamond", count=5, components={"Enchantments": "..."})

    @pytest.fixture
    def test_task(self, test_item):
        return Task(id="test_task_01", type="item", item=test_item, count=5)

    @pytest.fixture
    def test_reward(self, test_item):
        return Reward(id="test_reward_01", type="item", item=test_item, count=1)

    @pytest.fixture
    def test_quest(self, test_task, test_reward):
        quest = Quest(id="test_quest_alpha", x=1.0, y=2.0)
        quest.tasks = [test_task]
        quest.rewards = [test_reward]
        quest.dependencies = ["other_quest"]
        return quest

    @pytest.fixture
    def test_chapter(self, test_quest):
        return Chapter(
            id="test_chapter_a", 
            filename="test_a.snbt", 
            group="test_group", 
            order_index=1,
            quests=[test_quest]
        )


class TestModels(TestData):
    """Tests related to the Quest Pydantic data models."""
    def test_item_instantiation(self, test_item):
        """Test Item model creation and basic attributes."""
        assert test_item.id == "minecraft:diamond"
        assert test_item.count == 5
        assert "Enchantments" in test_item.components

    def test_task_instantiation(self, test_task, test_item):
        """Test Task model creation and item linkage."""
        assert test_task.id == "test_task_01"
        assert test_task.type == "item"
        assert test_task.item == test_item

    def test_quest_instantiation(self, test_quest):
        """Test Quest model creation and list initialization."""
        assert test_quest.id == "test_quest_alpha"
        assert test_quest.x == 1.0
        assert test_quest.y == 2.0
        assert len(test_quest.tasks) == 1
        assert "other_quest" in test_quest.dependencies

    def test_chapter_instantiation(self, test_chapter):
        """Test Chapter model creation."""
        assert test_chapter.id == "test_chapter_a"
        assert len(test_chapter.quests) == 1


class TestConfigAndExports:
    """Tests for setup and configuration files."""
    def test_config_paths(self):
        """Test that config paths are properly set."""
        from module.quest_config import FTBQ_DIR, LANG_DIR
        assert FTBQ_DIR == "../config/ftbquests/"
        assert LANG_DIR == "../config/ftbquests/quests/lang/en_us.snbt"

    def test_module_exports_completeness(self):
        """Test that module properly exports key functions and classes."""
        # Check a subset of required items
        required_names = {
            'display_chapters', 'load_chapter_data', 'parse_chapters',
            'edit_chapter_title', 'create_quest',
            'Chapter', 'Quest', 'Task', 'Reward', 'Item'
        }
        for name in required_names:
            assert hasattr(module, name), f"Missing export: {name}"

        # Ensure all items in __all__ are present (if needed, but TestPackage.py covers this better)


class TestEditFunctions(TestData):
    """Tests related to the quest_edit functions."""
    
    # Test Create functions (smoke test, as they are simple wrappers)
    def test_create_quest(self):
        quest = create_quest("new_quest_id", 50.0, 50.0, hide_details_until_startable=True)
        assert quest.id == "new_quest_id"
        assert quest.hide_details_until_startable is True

    # Test Chapter Edits
    def test_edit_chapter_title(self, test_chapter):
        """Test updating chapter title."""
        updated_chapter = edit_chapter_title(test_chapter, "New Chapter Title")
        assert updated_chapter.title == "New Chapter Title"
        # Ensure original chapter is unchanged (immutability of Pydantic copy)
        assert test_chapter.title is None

    def test_add_quest_to_chapter(self, test_chapter):
        """Test adding a quest to a chapter."""
        new_quest = create_quest("q_added", 10.0, 10.0)
        updated_chapter = add_quest_to_chapter(test_chapter, new_quest)
        assert len(updated_chapter.quests) == 2
        assert updated_chapter.quests[-1].id == "q_added"
        # Ensure original chapter is unchanged
        assert len(test_chapter.quests) == 1

    # Test Quest Edits
    def test_edit_quest_position(self, test_quest):
        """Test updating quest coordinates."""
        updated_quest = edit_quest_position(test_quest, 100.0, 200.0)
        assert updated_quest.x == 100.0
        assert updated_quest.y == 200.0
        # Ensure original quest is unchanged
        assert test_quest.x == 1.0


class TestNavigation(TestData):
    """Tests related to display/navigation functions (smoke tests)."""

    def test_display_functions_callable(self):
        """Test that navigation functions are callable."""
        from module.quest_navigator import display_chapters, display_quests, display_quest_details
        assert callable(display_chapters)
        assert callable(display_quests)
        assert callable(display_quest_details)

    def test_display_functions_smoke(self, test_chapter, test_quest):
        """Test that display functions print without crashing."""
        from module.quest_navigator import display_chapters, display_quests, display_quest_details

        try:
            # Note: We can't easily capture and verify console output here, 
            # so we just check for absence of exceptions.
            display_chapters({"test_chap": test_chapter})
            display_quests(test_chapter)
            display_quest_details(test_quest)
        except Exception as e:
            pytest.fail(f"Display function crashed: {e}")