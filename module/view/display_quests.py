from colorama import init, Fore, Style
from ..model.quest_models import Chapter, Quest

init(autoreset=True)

# Styling Constants
TITLE_STYLE = Fore.YELLOW + Style.BRIGHT
DEPS_STYLE = Fore.MAGENTA
ID_STYLE = Fore.LIGHTBLACK_EX
INDEX_STYLE = Fore.LIGHTBLACK_EX
# Note: Use Fore.RESET to stop color bleed when manually concatenating inside a single print
# However, Autoreset=True generally handles the end of the line.

def display_quests(chapter: Chapter) -> None:
    """Display the quests within a chapter."""
    print("\n" + Fore.CYAN + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + f"CHAPTER: {chapter.filename.upper()} (Quests: {len(chapter.quests)})")
    print(Fore.CYAN + "="*40)

    for i, quest in enumerate(chapter.quests):
        # 1. Prepare Styled Index
        # Concatenate style constants directly with the string, and use Style.RESET_ALL to stop the index color from flowing.
        index_text = f"[{INDEX_STYLE}{i}{Style.RESET_ALL}]"

        # 2. Prepare Styled Title (if present)
        # Apply style directly to the variable content.
        title_text = TITLE_STYLE + f" {quest.title}" if quest.title else ""
        
        # 3. Prepare Styled Quest ID
        # Apply style directly to the variable content.
        quest_id_text = ID_STYLE + f" {quest.id}"
        
        # 4. Prepare Styled Dependencies (if present)
        # Apply style directly to the variable content.
        deps_text = DEPS_STYLE + f" ({len(quest.dependencies)} deps)" if quest.dependencies else ""
        
        # 5. Concatenate everything. Since Autoreset=True is active, the final output will reset.
        print(
            index_text 
            + title_text  # Will be styled yellow/bright, or ""
            + quest_id_text # Will be styled lightblack
            + deps_text # Will be styled magenta
        )

def display_quest_details(quest: Quest) -> None:
    """Display details of a single quest."""
    
    # Header Construction
    title_text = TITLE_STYLE + f" {quest.title}" if quest.title else ""
    header_line = Fore.YELLOW + Style.BRIGHT + "QUEST DETAILS:" + title_text + f" {quest.id}"
    
    print("\n" + Fore.CYAN + "="*60)
    print(header_line)
    print(Fore.CYAN + "="*60)
    
    # Details
    print(f"Coords: ({quest.x}, {quest.y})")
    
    # Apply DEPS_STYLE directly to the content, outside the f-string variable itself.
    deps_info = DEPS_STYLE + (quest.dependencies if quest.dependencies else 'None')
    print(f"Dependencies: {deps_info}")
    
    print(f"Hidden Until Startable: {quest.hide_details_until_startable}")

    print(Fore.GREEN + "\n--- TASKS ---")
    if not quest.tasks:
        print("No tasks defined.")
    else:
        for i, task in enumerate(quest.tasks):
            # Apply INDEX_STYLE and reset for the index brackets
            index_part = f"[{INDEX_STYLE}{i}{Style.RESET_ALL}]"
            
            # Apply INDEX_STYLE to the item info for highlighting
            item_info_styled = INDEX_STYLE + f"Item: {task.item.id} x{task.item.count}" if task.item else "Checkmark"
            
            optional = " (OPTIONAL)" if task.optional_task else ""
            
            # Concatenate the styled segments
            print(
                f"{index_part} Type: {task.type} | Count: {task.count} | {item_info_styled}{optional}"
            )
            
            if task.advancement:
                print(f"    Advancement: {task.advancement}")

    print(Fore.GREEN + "\n--- REWARDS ---")
    if not quest.rewards:
        print("No rewards defined.")
    else:
        for i, reward in enumerate(quest.rewards):
            # Apply INDEX_STYLE and reset for the index brackets
            index_part = f"[{INDEX_STYLE}{i}{Style.RESET_ALL}]"
            
            # Apply INDEX_STYLE to the item info for highlighting
            item_info_styled = INDEX_STYLE + f"Item: {reward.item.id} x{reward.item.count}" if reward.item else "Unknown"
            
            # Concatenate the styled segments
            print(
                f"{index_part} Type: {reward.type} | {item_info_styled}"
            )
            
            if reward.advancement:
                print(f"    Advancement: {reward.advancement}")
            if reward.count:
                print(f"    Count: {reward.count}")