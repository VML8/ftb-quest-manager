#!/usr/bin/env python3
"""
FTB Quest Viewer - Quick Test
Quick verification that the basic package functionality works.
"""

import os
import sys
from pathlib import Path

from .venv.static_path import FTB_QUEST_PATH


def quick_test():
    """Quick test of essential functionality."""
    print("🚀 FTB Quest Viewer - Quick Test")
    print("=" * 40)

    # Use static path for testing
    static_path = FTB_QUEST_PATH
    print(f"📁 Using static path: {static_path}")

    # Test 1: Imports
    print("\n1️⃣ Testing imports...")
    try:
        from module import display_chapters, load_chapter_data, parse_chapters, Chapter
        print("   ✅ Basic imports successful")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

    # Test 2: Data loading
    print("\n2️⃣ Testing data loading...")
    try:
        raw_data = load_chapter_data(static_path)
        if raw_data:
            print(f"   ✅ Loaded {len(raw_data)} chapters")

            # Try to parse chapters
            chapters = parse_chapters(raw_data)
            if chapters:
                print(f"   ✅ Parsed {len(chapters)} chapters successfully")
                # Test display
                print("\n3️⃣ Testing display functions...")
                display_chapters(chapters)
                sample_chapter = next(iter(chapters.values()))
                print(f"   Sample chapter: {sample_chapter.filename}")
                print(f"   Quests: {len(sample_chapter.quests)}")
                if sample_chapter.quests:
                    sample_quest = sample_chapter.quests[0]
                    print(f"   Sample quest: {sample_quest.id}")
                    print(f"   Tasks: {len(sample_quest.tasks)}, Rewards: {len(sample_quest.rewards)}")
            else:
                print("   ❌ No chapters parsed")
                return False
        else:
            print("   ❌ No data loaded")
            return False
    except Exception as e:
        print(f"   ❌ Data loading failed: {e}")
        return False

    print("\n🎉 All quick tests passed!")
    print("\n💡 Ready to run: python -c \"from module.cli import main; main()\"")
    return True

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
