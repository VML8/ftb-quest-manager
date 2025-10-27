import argparse
import sys
from typing import Dict, Optional, List, Tuple, Union

# Import all necessary components from the module
from module import (
    display_chapters, display_quests, display_quest_details, display_task_details, display_reward_details,
    load_chapter_data, load_language_data, parse_chapters, find_chapters_directory,
    Chapter, Quest,
    edit_chapter_title, edit_quest_in_chapter, edit_quest_position
)

# --- Shared Utility ---

def load_data_for_cli() -> Optional[Dict[str, Chapter]]:
    """Loads and parses data once for any CLI mode."""
    try:
        # 1. Discover chapters directory
        chapters_dir = find_chapters_directory()
        
        # 2. Load chapter data
        raw_chapter_data = load_chapter_data(chapters_dir)
        
        # --- FIX: Load language data using the discovered chapters directory ---
        lang_data = load_language_data(chapters_dir)
        # ----------------------------------------------------------------------
        
        # 3. Parse and return
        return parse_chapters(raw_chapter_data, lang_data)
        
    except Exception as e:
        print(f"Error loading quest data: {e}")
        return None

# --- Interactive CLI Helper Functions ---

def _handle_chapter_level_input(
    parsed_chapters: Dict[str, Chapter], 
    chapter_keys: List[str], 
    user_input: str
) -> Union[Chapter, str, None]:
    """
    Handles input when at the main Chapter selection level.
    Returns: Chapter object, 'EXIT' sentinel, or None (invalid input).
    """
    match user_input.split():
        case ['exit']:
            return 'EXIT'
        case [index] if index.isdigit() and 0 <= int(index) < len(chapter_keys):
            return parsed_chapters[chapter_keys[int(index)]]
        case [key] if key in parsed_chapters:
            return parsed_chapters[key]
        case _:
            print("Invalid chapter selection.")
            return None

def _handle_chapter_edit(current_chapter: Chapter) -> Chapter:
    """Handles the 'edit' command at the Chapter level (currently title only)."""
    print("Edit chapter: Type 'title <new_title>' or 'back'")
    edit_input = input().strip()
    match edit_input.split():
        case ['title', *title]:
            new_title = ' '.join(title)
            updated_chapter = edit_chapter_title(current_chapter, new_title)
            print(f"Chapter title updated to '{new_title}'.")
            return updated_chapter
        case ['back']:
            return current_chapter
        case _:
            print("Invalid edit command.")
            return current_chapter

def _handle_quest_detail_edit(selected_quest: Quest, current_chapter: Chapter) -> Tuple[Quest, Chapter]:
    """Handles the 'edit' command at the Quest Detail level (e.g., position)."""
    print("Edit quest: Type 'position x y' or 'back'")
    edit_input = input().strip()
    match edit_input.split():
        case ['position', x, y] if x.replace('.', '').replace('-', '').isdigit() and y.replace('.', '').replace('-', '').isdigit():
            # 1. Update quest position (creates new Quest object due to Pydantic immutability)
            updated_q = edit_quest_position(selected_quest, float(x), float(y))
            # 2. Update the quest in the chapter's list (creates new Chapter object)
            updated_chapter = edit_quest_in_chapter(current_chapter, selected_quest.id, updated_q)
            print("Quest position updated.")
            return updated_q, updated_chapter
        case ['back']:
            return selected_quest, current_chapter
        case _:
            print("Invalid edit command.")
            return selected_quest, current_chapter

def _handle_quest_detail_level_loop(selected_quest: Quest, current_chapter: Chapter) -> Tuple[str, Optional[Chapter], Optional[Quest]]:
    """
    Manages the nested loop for viewing and editing a specific Quest's details.
    Returns: (action, updated_chapter, updated_quest)
    Action can be 'break' (to go back to quest list), 'exit', or 'continue' (to repeat loop).
    """
    
    # Loop while viewing details of the selected quest
    while True:
        display_quest_details(selected_quest)
        sub_input = input("Select task/reward index (e.g., 'task 0'), 'edit', 'back', or 'exit': ").strip().lower()
        
        match sub_input.split():
            case ['exit']:
                return 'exit', None, None
            case ['back']:
                return 'break', current_chapter, None
            case ['task', t_index] if t_index.isdigit() and 0 <= int(t_index) < len(selected_quest.tasks):
                display_task_details(selected_quest.tasks[int(t_index)], selected_quest.id)
            case ['reward', r_index] if r_index.isdigit() and 0 <= int(r_index) < len(selected_quest.rewards):
                display_reward_details(selected_quest.rewards[int(r_index)], selected_quest.id)
            case ['edit']:
                # Edit returns the new quest and the new chapter object
                selected_quest, current_chapter = _handle_quest_detail_edit(selected_quest, current_chapter)
                # Continue in this loop with the updated objects
            case _:
                print("Invalid. Use 'task <num>', 'reward <num>', 'edit', 'back', or 'exit'.")
    
    return 'continue', current_chapter, selected_quest # Fall-Through Safegaurd

def _handle_quest_level_input(current_chapter: Chapter, user_input: str) -> Tuple[str, Chapter]:
    """
    Handles input when at the Quest selection level for a specific chapter.
    Returns: (action, updated_chapter)
    Action can be 'exit', 'back', or 'continue' (to repeat loop with potentially updated chapter).
    """
    match user_input.split():
        case ['exit']:
            return 'exit', current_chapter
        case ['back']:
            return 'back', current_chapter
        case ['edit']:
            updated_chapter = _handle_chapter_edit(current_chapter)
            return 'continue', updated_chapter
        case [index] if index.isdigit() and 0 <= int(index) < len(current_chapter.quests):
            selected_quest = current_chapter.quests[int(index)]
            
            # Enter Quest Details loop
            action, updated_chapter, _ = _handle_quest_detail_level_loop(selected_quest, current_chapter)
            
            if action == 'exit':
                return 'exit', current_chapter # Propagate exit
            
            # Action 'break' (go back to quest list) or 'continue' (edit finished).
            # We return to the main loop with the potentially updated chapter.
            return 'continue', updated_chapter if updated_chapter else current_chapter
        case _:
            print("Invalid. Try 'back', 'edit', or a number.")
            return 'continue', current_chapter

# --- 2. Interactive CLI Main Function (Refactored) ---

def interactive_cli_main(parsed_chapters: Dict[str, Chapter]):
    """
    The full-featured, stateful, and interactive command-line interface 
    for deep navigation and editing, using helper functions for readability.
    """
    # State variables
    current_chapter: Optional[Chapter] = None
    chapter_keys = list(parsed_chapters.keys())

    print("FTB Quests CLI (Interactive Mode).")

    while True:
        if current_chapter is None:
            # Chapter selection level
            display_chapters(parsed_chapters)
            user_input = input("Select chapter index, key, or 'exit': ").strip().lower()

            result = _handle_chapter_level_input(parsed_chapters, chapter_keys, user_input)
            
            if result == 'EXIT':
                break
            elif isinstance(result, Chapter):
                current_chapter = result
                
        else:
            # Quest selection level
            display_quests(current_chapter)
            user_input = input("Select quest index, 'back', 'edit', or 'exit': ").strip().lower()

            action, updated_chapter = _handle_quest_level_input(current_chapter, user_input)

            if action == 'exit':
                break
            elif action == 'back':
                current_chapter = None
            elif action == 'continue':
                # Update the chapter state after selection or an edit
                current_chapter = updated_chapter


    print("\nExiting FTB Quests CLI. Goodbye!")

# --- 3. Rapid Argparse Tool Main Function (Unchanged) ---

def argparse_cli_main(args: argparse.Namespace, chapters: Dict[str, Chapter]):
    """
    A single-command, non-interactive CLI using argparse.
    Suitable for quick data lookups and atomic edits.
    """
    
    if args.command == 'view':
        if args.entity == 'chapters':
            display_chapters(chapters)
        elif args.entity == 'quest' and args.id:
            # Search for the quest across all chapters
            found_quest = next((
                quest for chapter in chapters.values() for quest in chapter.quests 
                if quest.id.startswith(args.id)
            ), None)
            
            if found_quest:
                display_quest_details(found_quest)
            else:
                print(f"Error: Quest with ID starting with '{args.id}' not found.")
                
    elif args.command == 'edit':
        if args.entity == 'chapter' and args.field == 'title':
            chapter_key = args.id
            if chapter_key in chapters:
                updated_chapter = edit_chapter_title(chapters[chapter_key], args.value)
                # NOTE: You must add file saving logic here for persistent edits.
                print(f"✅ Chapter '{chapter_key}' title changed to '{updated_chapter.title}' (Unsaved).")
            else:
                print(f"Error: Chapter '{chapter_key}' not found.")
        
        elif args.entity == 'quest' and args.field == 'position' and args.x is not None and args.y is not None:
            # Find the quest
            found_quest = next((
                quest for chapter in chapters.values() for quest in chapter.quests 
                if quest.id.startswith(args.id)
            ), None)
            
            if found_quest:
                updated_quest = edit_quest_position(found_quest, args.x, args.y)
                # NOTE: You must add file saving logic here for persistent edits.
                print(f"✅ Quest '{found_quest.id}' position updated to ({updated_quest.x}, {updated_quest.y}) (Unsaved).")
            else:
                print(f"Error: Quest with ID starting with '{args.id}' not found.")
        
        else:
            print("Error: Invalid or incomplete edit command.")


# --- Main Entry Point (Called by console scripts) ---

def main():
    """
    The package's primary entry point. 
    Switches between interactive mode (no arguments) and argparse mode (with arguments).
    """
    # 1. Load data first
    parsed_chapters = load_data_for_cli()
    if not parsed_chapters:
        sys.exit(1)

    # 2. Determine mode
    if len(sys.argv) == 1:
        # No arguments: Run Interactive CLI
        interactive_cli_main(parsed_chapters)
    else:
        # Arguments present: Setup and run Argparse CLI

        parser = argparse.ArgumentParser(description="FTB Quest Viewer Command-Line Interface. Run without arguments for interactive mode.")
        subparsers = parser.add_subparsers(dest='command', required=True)

        # --- 'view' command setup ---
        view_parser = subparsers.add_parser('view', help='View quest data (e.g., view chapters or view quest <ID>).')
        view_subparsers = view_parser.add_subparsers(dest='entity', required=True)
        view_subparsers.add_parser('chapters', help='View all chapter titles.')
        quest_parser = view_subparsers.add_parser('quest', help='View details for a specific quest ID (partial IDs allowed).')
        quest_parser.add_argument('id', type=str, help='The full or partial ID of the quest to view.')

        # --- 'edit' command setup (simplified) ---
        edit_parser = subparsers.add_parser('edit', help='Edit quest data (edits are NOT saved by this example code).')
        edit_subparsers = edit_parser.add_subparsers(dest='entity', required=True)

        # Edit Chapter: title
        chapter_edit_parser = edit_subparsers.add_parser('chapter', help='Edit a chapter property.')
        chapter_edit_parser.add_argument('id', type=str, help='The key of the chapter to edit (e.g., "chapter_1").')
        chapter_edit_parser.add_argument('field', choices=['title'], help='The field to edit.')
        chapter_edit_parser.add_argument('value', type=str, help='The new value for the field.')
        
        # Edit Quest: position
        quest_edit_parser = edit_subparsers.add_parser('quest', help='Edit a quest property.')
        quest_edit_parser.add_argument('id', type=str, help='The full or partial ID of the quest to edit.')
        quest_edit_parser.add_argument('field', choices=['position'], help='The field to edit.')
        quest_edit_parser.add_argument('x', type=float, help='The new X coordinate.')
        quest_edit_parser.add_argument('y', type=float, help='The new Y coordinate.')

        # 3. Run Argparse CLI
        args = parser.parse_args()
        argparse_cli_main(args, parsed_chapters)

if __name__ == '__main__':
    main()