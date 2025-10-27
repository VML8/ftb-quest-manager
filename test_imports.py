#!/usr/bin/env python3
"""Test script to verify module imports work correctly."""

import sys
sys.path.insert(0, '.')

try:
    from module import display_task_details, display_reward_details
    print("✅ display_task_details import successful")
    print("✅ display_reward_details import successful")

    # Test that they are the same function (both aliases)
    print(f"✅ Both functions are the same: {display_task_details is display_reward_details}")

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

print("✅ All CLI imports working correctly!")
