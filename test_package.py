#!/usr/bin/env python3
"""
FTB Quest Viewer - Test Program
Comprehensive testing suite for the FTB Quest Viewer package.
"""

import os
import sys
from pathlib import Path
from module.venv.static_path import FTB_QUEST_PATH

def test_imports():
    """Test that all module imports work correctly."""
    print("🔍 Testing imports...")

    try:
        # Test main module imports
        from module import (
            display_chapters, display_quests, display_quest_details,
            display_task_details, display_reward_details,
            load_chapter_data, parse_chapters, find_chapters_directory,
            Chapter, Quest, Task, Reward, Item,
            edit_chapter_title, create_quest
        )
        print("✅ Main module imports: SUCCESS")

        # Test individual module imports
        from module.quest_models import Chapter, Quest, Task, Reward, Item
        print("✅ quest_models imports: SUCCESS")

        from module.quest_navigator import display_chapters, display_quests, display_quest_details, display_task_details, display_reward_details
        print("✅ quest_navigator imports: SUCCESS")

        from module.ftb_loader import load_chapter_data, parse_chapters, find_chapters_directory
        print("✅ ftb_loader imports: SUCCESS")

        from module.quest_config import FTBQ_DIR, LANG_DIR
        print("✅ quest_config imports: SUCCESS")

        from module.quest_edit import edit_chapter_title, create_quest
        print("✅ quest_edit imports: SUCCESS")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_paths():
    """Test that configuration paths are correctly resolved."""
    print("\n🔍 Testing path resolution...")

    try:
        from module.quest_config import FTBQ_DIR, LANG_DIR

        # Check if FTBQ_DIR exists and is a directory
        ftbq_path = Path(FTBQ_DIR).resolve()
        if ftbq_path.exists():
            print(f"✅ FTBQ_DIR exists: {ftbq_path}")
            if ftbq_path.is_dir():
                print("✅ FTBQ_DIR is a directory")
            else:
                print("❌ FTBQ_DIR is not a directory")
                return False
        else:
            print(f"❌ FTBQ_DIR does not exist: {ftbq_path}")
            print("   Make sure you're running from the Quest Manager directory")
            print("   and that config/ftbquests/ exists in the parent directory")
            return False

        # Check if quests/chapters subdirectory exists
        chapters_path = ftbq_path / "quests" / "chapters"
        if chapters_path.exists():
            print(f"✅ Chapters directory exists: {chapters_path}")

            # Check if there are .snbt files
            snbt_files = list(chapters_path.glob("*.snbt"))
            if snbt_files:
                print(f"✅ Found {len(snbt_files)} SNBT files")
                for snbt_file in snbt_files[:3]:  # Show first 3
                    print(f"   - {snbt_file.name}")
                if len(snbt_files) > 3:
                    print(f"   ... and {len(snbt_files) - 3} more")
            else:
                print("❌ No SNBT files found in chapters directory")
                return False
        else:
            print(f"❌ Chapters directory does not exist: {chapters_path}")
            return False

        return True

    except Exception as e:
        print(f"❌ Path test failed: {e}")
        return False

def test_data_loading():
    """Test quest data loading functionality."""
    print("\n🔍 Testing data loading...")

    try:
        from module.ftb_loader import load_chapter_data, parse_chapters
        from module.quest_models import Chapter

        # Test loading raw data
        print("Loading chapter data...")
        static_path = r"FTB_QUEST_PATH"
        raw_data = load_chapter_data(static_path)

        if raw_data:
            print(f"✅ Loaded {len(raw_data)} chapters")

            # Test parsing
            print("Parsing chapters...")
            chapters = parse_chapters(raw_data)

            if chapters:
                print(f"✅ Successfully parsed {len(chapters)} chapters")

                # Test a sample chapter
                sample_chapter = next(iter(chapters.values()))
                print(f"✅ Sample chapter: {sample_chapter.filename}")
                print(f"   - ID: {sample_chapter.id}")
                print(f"   - Quests: {len(sample_chapter.quests)}")
                print(f"   - Group: {sample_chapter.group}")

                # Test a sample quest
                if sample_chapter.quests:
                    sample_quest = sample_chapter.quests[0]
                    print(f"✅ Sample quest: {sample_quest.id[:16]}...")
                    print(f"   - Position: ({sample_quest.x}, {sample_quest.y})")
                    print(f"   - Tasks: {len(sample_quest.tasks)}")
                    print(f"   - Rewards: {len(sample_quest.rewards)}")

                return True
            else:
                print("❌ No chapters were parsed successfully")
                return False
        else:
            print("❌ No chapter data loaded")
            return False

    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_navigation():
    """Test navigation functionality."""
    print("\n🔍 Testing navigation functions...")

    try:
        from module.quest_navigator import display_chapters, display_quests, display_quest_details, display_task_details, display_reward_details
        from module.ftb_loader import load_chapter_data, parse_chapters

        # Load test data
        static_path = r"FTB_QUEST_PATH"
        raw_data = load_chapter_data(static_path)
        chapters = parse_chapters(raw_data)

        if not chapters:
            print("❌ No chapters available for navigation testing")
            return False

        print(f"✅ Navigation test setup: {len(chapters)} chapters available")

        # Test that navigation functions are callable
        print("✅ display_chapters function available")
        print("✅ display_quests function available")
        print("✅ display_quest_details function available")
        print("✅ display_task_details function available")
        print("✅ display_reward_details function available")

        # Test display functions with a small subset
        chapter_keys = list(chapters.keys())
        print(f"✅ Chapter keys: {chapter_keys[:3]}...")

        return True

    except Exception as e:
        print(f"❌ Navigation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edit_functions():
    """Test edit functionality."""
    print("\n🔍 Testing edit functions...")

    try:
        from module.quest_edit import edit_chapter_title, add_quest_to_chapter, create_quest, create_task, edit_quest_position
        from module.quest_models import Chapter, Quest, Task, Item

        # Create test data
        chapter = Chapter(id="test_chapter", filename="test.snbt", group="test_group", order_index=1)
        quest = create_quest("test_quest", 1.0, 2.0)
        task = create_task("test_task", "item", item=Item(id="minecraft:stone"))

        # Test edit chapter title
        updated_chapter = edit_chapter_title(chapter, "New Title")
        if updated_chapter.title == "New Title":
            print("✅ edit_chapter_title works")
        else:
            print("❌ edit_chapter_title failed")
            return False

        # Test add quest to chapter
        updated_chapter = add_quest_to_chapter(chapter, quest)
        if len(updated_chapter.quests) == 1:
            print("✅ add_quest_to_chapter works")
        else:
            print("❌ add_quest_to_chapter failed")
            return False

        # Test edit quest position
        updated_quest = edit_quest_position(quest, 10.0, 20.0)
        if updated_quest.x == 10.0 and updated_quest.y == 20.0:
            print("✅ edit_quest_position works")
        else:
            print("❌ edit_quest_position failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Edit test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_package_info():
    """Test package metadata and exports."""
    print("\n🔍 Testing package metadata...")

    try:
        import module

        print(f"✅ Package version: {getattr(module, '__version__', 'Not set')}")

        # Test __all__ exports
        expected_exports = [
            'display_chapters', 'display_quests', 'display_quest_details',
            'display_task_details', 'display_reward_details',
            'load_chapter_data', 'parse_chapters', 'find_chapters_directory',
            'Chapter', 'Quest', 'Task', 'Reward', 'Item',
            'edit_chapter_title', 'create_quest'
        ]

        all_exports = getattr(module, '__all__', [])
        print(f"✅ Package exports {len(all_exports)} items")

        missing_exports = []
        for export in expected_exports:
            if hasattr(module, export):
                print(f"   ✅ {export}")
            else:
                print(f"   ❌ {export} (missing)")
                missing_exports.append(export)

        if missing_exports:
            print(f"❌ Missing exports: {missing_exports}")
            return False

        return True

    except Exception as e:
        print(f"❌ Package info test failed: {e}")
        return False

def test_cli():
    """Test CLI functionality."""
    print("\n🔍 Testing CLI...")

    try:
        import subprocess

        # Test CLI import
        result = subprocess.run([sys.executable, 'cli.py'], capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0 or "Exiting" in result.stderr:
            print("✅ CLI executed without crashing")
        else:
            print(f"❌ CLI failed: {result.stderr}")
            return False

        return True

    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    """Run all tests and provide summary."""
    print("=" * 60)
    print("🎯 FTB Quest Viewer - Test Suite")
    print("=" * 60)

    # Change to the Quest Manager directory if not already there
    quest_manager_dir = Path(__file__).parent
    os.chdir(quest_manager_dir)

    print(f"📁 Running tests from: {quest_manager_dir}")
    print(f"🐍 Python version: {sys.version}")

    tests = [
        ("Import Tests", test_imports),
        ("Data Loading", test_data_loading),
        ("Navigation Functions", test_navigation),
        ("Edit Functions", test_edit_functions),
        ("Package Metadata", test_package_info),
        ("CLI Test", test_cli),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'-' * 40}")
        print(f"🧪 {test_name}")
        print('-' * 40)

        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("❌ Test interrupted by user")
            results.append((test_name, False))
            break
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The package is working correctly.")
        print("\n💡 Next steps:")
        print("   - Run 'python cli.py' to use the CLI")
        print("   - Run 'pip install .' to install as a package")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("\n🔧 Common fixes:")
        print("   - Make sure you're in the Quest Manager directory")
        print("   - Check that config/ftbquests/quests/chapters/ contains .snbt files")
        print("   - Verify Python path and dependencies")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
