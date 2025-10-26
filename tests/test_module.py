"""
Unit tests for FTB Quest Viewer module.

Run with: pytest tests/
Or run directly: python -m pytest tests/
"""

import sys
from pathlib import Path

# Add the parent directory to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_quest_models():
    """Test that quest models can be imported and instantiated."""
    from module.quest_models import Item, Task, Reward, Quest, Chapter

    # Test Item model
    item = Item(id="minecraft:diamond", count=5)
    assert item.id == "minecraft:diamond"
    assert item.count == 5

    # Test Task model
    task = Task(id="test_task", type="item", item=item)
    assert task.id == "test_task"
    assert task.type == "item"
    assert task.item == item

    # Test Reward model
    reward = Reward(id="test_reward", type="item", item=item)
    assert reward.id == "test_reward"
    assert reward.type == "item"
    assert reward.item == item

    # Test Quest model
    quest = Quest(id="test_quest", x=1.0, y=2.0)
    quest.tasks = [task]
    quest.rewards = [reward]
    quest.dependencies = ["other_quest"]

    assert quest.id == "test_quest"
    assert quest.x == 1.0
    assert quest.y == 2.0
    assert len(quest.tasks) == 1
    assert len(quest.rewards) == 1
    assert "other_quest" in quest.dependencies

def test_config_paths():
    """Test that config paths are properly set."""
    from module.quest_config import FTBQ_DIR, LANG_DIR

    assert FTBQ_DIR == "../config/ftbquests/"
    assert LANG_DIR == "../config/ftbquests/quests/lang/en_us.snbt"

def test_module_exports():
    """Test that module properly exports all required functions and classes."""
    import module

    # Check that all required functions are exported
    required_functions = [
        'display_chapters', 'display_quests', 'display_quest_details',
        'display_task_details', 'display_reward_details',
        'load_chapter_data', 'parse_chapters', 'find_chapters_directory',
        'edit_chapter_title', 'add_quest_to_chapter', 'create_quest'
    ]

    for func_name in required_functions:
        assert hasattr(module, func_name), f"Missing function: {func_name}"

    # Check that all required classes are exported
    required_classes = ['Chapter', 'Quest', 'Task', 'Reward', 'Item']

    for class_name in required_classes:
        assert hasattr(module, class_name), f"Missing class: {class_name}"

def test_navigation_functions():
    """Test that navigation functions are callable."""
    from module.quest_navigator import display_chapters, display_quests, display_quest_details, display_task_details, display_reward_details
    from module.ftb_loader import load_chapter_data, parse_chapters, find_chapters_directory
    from module.quest_models import Chapter, Quest

    # Test that functions are callable
    assert callable(display_chapters)
    assert callable(display_quests)
    assert callable(display_quest_details)
    assert callable(display_task_details)
    assert callable(display_reward_details)
    assert callable(load_chapter_data)
    assert callable(parse_chapters)
    assert callable(find_chapters_directory)

def test_edit_functions():
    """Test that edit functions work correctly."""
    from module.quest_edit import edit_chapter_title, add_quest_to_chapter, create_quest, create_task, edit_quest_position
    from module.quest_models import Chapter, Quest, Task, Item

    # Create test data
    chapter = Chapter(id="test_chapter", filename="test.snbt", group="test_group", order_index=1)
    quest = create_quest("test_quest", 1.0, 2.0)
    task = create_task("test_task", "item", item=Item(id="minecraft:stone"))

    # Test edit chapter title
    updated_chapter = edit_chapter_title(chapter, "New Title")
    assert updated_chapter.title == "New Title"
    assert updated_chapter.id == "test_chapter"

    # Test add quest to chapter
    updated_chapter = add_quest_to_chapter(chapter, quest)
    assert len(updated_chapter.quests) == 1
    assert updated_chapter.quests[0].id == "test_quest"

    # Test edit quest position
    updated_quest = edit_quest_position(quest, 10.0, 20.0)
    assert updated_quest.x == 10.0
    assert updated_quest.y == 20.0

    # Test create functions
    assert quest.id == "test_quest"
    assert task.id == "test_task"

def test_display_functions():
    """Test that display functions print without errors."""
    from module.quest_navigator import display_chapters, display_quests, display_quest_details
    from module.quest_models import Chapter, Quest, Task, Item

    # Create test data
    chapter = Chapter(id="test_chapter", filename="test.snbt", group="test_group", order_index=1, quests=[Quest(id="test_quest", x=1.0, y=2.0)])
    quest = chapter.quests[0]
    quest.tasks = [Task(id="test_task", type="item", item=Item(id="minecraft:stone"))]

    # Test display functions (capture output or just ensure no errors)
    try:
        display_chapters({"test": chapter})
        display_quests(chapter)
        display_quest_details(quest)
        print("✅ Display functions executed without errors")
    except Exception as e:
        pytest.fail(f"Display function failed: {e}")

if __name__ == "__main__":
    # Run tests directly
    print("🧪 Running unit tests...")

    tests = [
        test_quest_models,
        test_config_paths,
        test_module_exports,
        test_navigation_functions,
        test_edit_functions,
        test_display_functions
    ]

    for test_func in tests:
        try:
            test_func()
            print(f"✅ {test_func.__name__} passed")
        except Exception as e:
            print(f"❌ {test_func.__name__} failed: {e}")

    print("\n🎯 Unit tests complete!")
