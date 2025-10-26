from typing import Dict

from .quest_models import Chapter, Quest, Task, Reward


def display_chapters(data: Dict[str, Chapter]) -> None:
    """Display the list of chapters."""
    print("\n" + "="*40)
    print("CHAPTERS")
    print("="*40)

    chapter_keys = sorted(data.keys())
    for i, key in enumerate(chapter_keys):
        chapter = data[key]
        print(f"[{i}] {key.upper()} (Quests: {len(chapter.quests)}, Group: {chapter.group[:8]}...)")


def display_quests(chapter: Chapter) -> None:
    """Display the quests within a chapter."""
    print("\n" + "="*40)
    print(f"CHAPTER: {chapter.filename.upper()} (Quests: {len(chapter.quests)})")
    print("="*40)

    for i, quest in enumerate(chapter.quests):
        deps = f"({len(quest.dependencies)} deps)" if quest.dependencies else ""
        print(f"[{i}] Quest ID: {quest.id[:8]}... {deps}")


def display_quest_details(quest: Quest) -> None:
    """Display details of a single quest."""
    print("\n" + "="*60)
    print(f"QUEST DETAILS: {quest.id}")
    print("="*60)
    print(f"Coords: ({quest.x}, {quest.y})")
    print(f"Dependencies: {quest.dependencies if quest.dependencies else 'None'}")
    print(f"Hidden Until Startable: {quest.hide_details_until_startable}")

    print("\n--- TASKS ---")
    if not quest.tasks:
        print("No tasks defined.")
    else:
        for i, task in enumerate(quest.tasks):
            item_info = f"Item: {task.item.id} x{task.item.count}" if task.item else "Checkmark"
            optional = " (OPTIONAL)" if task.optional_task else ""
            print(f"[{i}] Type: {task.type} | Count: {task.count} | {item_info}{optional}")
            if task.advancement:
                print(f"    Advancement: {task.advancement}")

    print("\n--- REWARDS ---")
    if not quest.rewards:
        print("No rewards defined.")
    else:
        for i, reward in enumerate(quest.rewards):
            item_info = f"Item: {reward.item.id} x{reward.item.count}" if reward.item else "Unknown"
            print(f"[{i}] Type: {reward.type} | {item_info}")
            if reward.advancement:
                print(f"    Advancement: {reward.advancement}")
            if reward.count:
                print(f"    Count: {reward.count}")


def display_task_details(task: Task, quest_id: str = "Unknown Quest") -> None:
    """Display comprehensive details of a task."""
    print("\n" + "="*50)
    print(f"TASK DETAILS: {task.type.upper()}")
    print(f"Quest: {quest_id}")
    print("="*50)

    print(f"Task ID: {task.id}")
    print(f"Type: {task.type}")
    print(f"Count: {task.count if task.count else 'Not specified'}")

    if task.item:
        print(f"Item: {task.item.id}")
        print(f"Item Count: {task.item.count}")
        if task.item.components:
            print(f"Item Components: {task.item.components}")

    if hasattr(task, 'advancement') and task.advancement:
        print(f"Advancement: {task.advancement}")

    print(f"Optional Task: {'Yes' if task.optional_task else 'No'}")

    print("\n" + "="*50)


def display_reward_details(reward: Reward, quest_id: str = "Unknown Quest") -> None:
    """Display comprehensive details of a reward."""
    print("\n" + "="*50)
    print(f"REWARD DETAILS: {reward.type.upper()}")
    print(f"Quest: {quest_id}")
    print("="*50)

    print(f"Reward ID: {reward.id}")
    print(f"Type: {reward.type}")

    if reward.item:
        print(f"Item: {reward.item.id}")
        print(f"Item Count: {reward.item.count}")
        if reward.item.components:
            print(f"Item Components: {reward.item.components}")
    else:
        print("No item associated with this reward")

    if hasattr(reward, 'advancement') and reward.advancement:
        print(f"Advancement: {reward.advancement}")

    if hasattr(reward, 'count') and reward.count:
        print(f"Count: {reward.count}")

    print("\n" + "="*50)
