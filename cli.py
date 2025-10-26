import argparse
import sys
from typing import Dict, Optional, List

# Import all necessary components from the module
from module import (
    display_chapters, display_quests, display_quest_details, 
    load_chapter_data, parse_chapters, find_chapters_directory,
    Chapter, Quest, Task, Reward, Item,
    edit_chapter_title, edit_quest_in_chapter, edit_quest_position
)

# --- Shared Utility ---

def load_data_for_cli() -> Optional[Dict[str, Chapter]]:
    """Loads and parses data once for any CLI mode."""
    try:
        chapters_dir = find_chapters_directory()
        raw_chapter_data = load_chapter_data(chapters_dir)
        return parse_chapters(raw_chapter_data)
    except Exception as e:
        print(f"Error loading quest data: {e}")
        return None


# --- 2. Interactive CLI Main Function ---

def interactive_cli_main(parsed_chapters: Dict[str, Chapter]):
    """
    The full-featured, stateful, and interactive command-line interface 
    for deep navigation and editing. (Logic adapted from module/__main__.py)
    """
    current_chapter: Optional[Chapter] = None
    chapter_keys = list(parsed_chapters.keys())

    print("FTB Quests CLI (Interactive Mode). Type 'help' for commands.")

    while True:
        if current_chapter is None:
            # Chapter selection level
            display_chapters(parsed_chapters)
            user_input = input("Select chapter index, key, or 'exit': ").strip().lower()
            match user_input.split():
                case ['exit']:
                    break
                case [index] if index.isdigit() and 0 <= int(index) < len(chapter_keys):
                    current_chapter = parsed_chapters[chapter_keys[int(index)]]
                case [key] if key in parsed_chapters:
                    current_chapter = parsed_chapters[key]
                case _:
                    print("Invalid chapter selection.")
        else:
            # Quest selection level
            display_quests(current_chapter)
            user_input = input("Select quest index, 'back', 'edit', or 'exit': ").strip().lower()
            match user_input.split():
                case ['exit']:
                    break
                case ['back']:
                    current_chapter = None
                case [index] if index.isdigit() and 0 <= int(index) < len(current_chapter.quests):
                    selected_quest = current_chapter.quests[int(index)]
                    # Simple display
                    display_quest_details(selected_quest)
                case ['edit']:
                    # Simplified chapter edit example
                    print("Edit chapter: Type 'title <new_title>' or 'back'")
                    edit_input = input().strip()
                    match edit_input.split():
                        case ['title', *title]:
                            new_title = ' '.join(title)
                            current_chapter = edit_chapter_title(current_chapter, new_title)
                            print(f"Chapter title updated to '{new_title}'.")
                        case ['back']:
                            pass
                        case _:
                            print("Invalid edit command.")
                case _:
                    print("Invalid. Try 'back', 'edit', or a number.")

    print("\nExiting FTB Quests CLI. Goodbye!")


# --- 3. Rapid Argparse Tool Main Function ---

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