from colorama import init, Fore, Style
from ..model.quest_models import Chapter, Quest

init(autoreset=True)

def display_quests(chapter: Chapter) -> None:
    """Display the quests within a chapter."""
    print("\n" + Fore.CYAN + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + f"CHAPTER: {chapter.filename.upper()} (Quests: {len(chapter.quests)})")
    print(Fore.CYAN + "="*40)

    for i, quest in enumerate(chapter.quests):
        deps = f"({len(quest.dependencies)} deps)" if quest.dependencies else ""
        print(f"[{i}] Quest ID: {quest.id[:8]}... {deps}")

def display_quest_details(quest: Quest) -> None:
    """Display details of a single quest."""
    print("\n" + Fore.CYAN + "="*60)
    print(Fore.YELLOW + Style.BRIGHT + f"QUEST DETAILS: {quest.id}")
    print(Fore.CYAN + "="*60)
    print(f"Coords: ({quest.x}, {quest.y})")
    print(f"Dependencies: {quest.dependencies if quest.dependencies else 'None'}")
    print(f"Hidden Until Startable: {quest.hide_details_until_startable}")

    print(Fore.GREEN + "\n--- TASKS ---")
    if not quest.tasks:
        print("No tasks defined.")
    else:
        for i, task in enumerate(quest.tasks):
            item_info = f"Item: {task.item.id} x{task.item.count}" if task.item else "Checkmark"
            optional = " (OPTIONAL)" if task.optional_task else ""
            print(f"[{i}] Type: {task.type} | Count: {task.count} | {item_info}{optional}")
            if task.advancement:
                print(f"    Advancement: {task.advancement}")

    print(Fore.GREEN + "\n--- REWARDS ---")
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