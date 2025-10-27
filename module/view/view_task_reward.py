from colorama import init, Fore, Back, Style

from typing import Dict, Union

from .quest_models import Chapter, Quest, Task, Reward

init(autoreset=True)


def display_task_reward_details(obj: Union[Task, Reward], quest_id: str = "Unknown Quest", obj_type: str = "AUTO") -> None:
    """Display comprehensive details of a task or reward.

    Args:
        obj: The Task or Reward object to display
        quest_id: The quest ID this belongs to
        obj_type: Either "TASK", "REWARD", or "AUTO" to auto-detect
    """
    # Auto-detect type if not specified
    if obj_type == "AUTO":
        obj_type = "TASK" if isinstance(obj, Task) else "REWARD"

    obj_type = obj_type.upper()
    is_task = obj_type == "TASK"

    print("\n" + Fore.CYAN + "="*50)
    print(Fore.YELLOW + Style.BRIGHT + f"{obj_type} DETAILS: {obj.type.upper()}")
    print(f"Quest: {quest_id}")
    print(Fore.CYAN + "="*50)

    # ID and type with appropriate labels
    id_label = "Task ID" if is_task else "Reward ID"
    print(f"{id_label}: {obj.id}")
    print(f"Type: {obj.type}")

    # Handle count display
    if is_task:
        print(f"Count: {obj.count if obj.count else 'Not specified'}")
    else:
        if hasattr(obj, 'count') and obj.count:
            print(f"Count: {obj.count}")

    # Item information
    if obj.item:
        print(f"Item: {obj.item.id}")
        print(f"Item Count: {obj.item.count}")
        if obj.item.components:
            print(f"Item Components: {obj.item.components}")
    else:
        if not is_task:  # Only show this message for rewards
            print("No item associated with this reward")

    # Advancement information
    if hasattr(obj, 'advancement') and obj.advancement:
        print(f"Advancement: {obj.advancement}")

    # Task-specific information
    if is_task:
        print(f"Optional Task: {'Yes' if obj.optional_task else 'No'}")

    print(Fore.CYAN + "\n" + "="*50)
