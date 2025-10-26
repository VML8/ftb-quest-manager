from . import (
    display_chapters, display_quests, display_quest_details, display_task_details, display_reward_details,
    find_chapters_directory, load_chapter_data, parse_chapters,
    Chapter, Quest, Task, Reward, Item,
    edit_chapter_title, edit_chapter_subtitle, edit_chapter_icon,
    edit_chapter_tags, add_quest_to_chapter, remove_quest_from_chapter,
    edit_quest_in_chapter, edit_quest_position, add_task_to_quest,
    remove_task_from_quest, edit_task_in_quest, add_reward_to_quest,
    remove_reward_from_quest, edit_reward_in_quest, create_task,
    create_reward, create_quest, create_chapter
)

def main():
    """Main execution function with match-case loop."""

    # Find and load chapter data
    chapters_dir = find_chapters_directory()
    raw_chapter_data = load_chapter_data(chapters_dir)
    parsed_chapters = parse_chapters(raw_chapter_data)

    # Navigation state
    current_chapter = None
    chapter_keys = list(parsed_chapters.keys())

    print("FTB Quests CLI. Type 'help' for commands.")

    while True:
        if current_chapter is None:
            # Chapter level
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
                    print("Invalid. Try 'help'.")
        else:
            # Quest level
            display_quests(current_chapter)
            user_input = input("Select quest index, 'back', 'edit', or 'exit': ").strip().lower()
            match user_input.split():
                case ['exit']:
                    break
                case ['back']:
                    current_chapter = None
                case [index] if index.isdigit() and 0 <= int(index) < len(current_chapter.quests):
                    selected_quest = current_chapter.quests[int(index)]
                    # Quest details sub-menu
                    while True:
                        display_quest_details(selected_quest)
                        sub_input = input("Select task/reward index (e.g., 'task 0'), 'edit', 'back', or 'exit': ").strip().lower()
                        match sub_input.split():
                            case ['exit']:
                                return
                            case ['back']:
                                break
                            case ['task', t_index] if t_index.isdigit() and 0 <= int(t_index) < len(selected_quest.tasks):
                                display_task_details(selected_quest.tasks[int(t_index)], selected_quest.id)
                            case ['reward', r_index] if r_index.isdigit() and 0 <= int(r_index) < len(selected_quest.rewards):
                                display_reward_details(selected_quest.rewards[int(r_index)], selected_quest.id)
                            case ['edit']:
                                # Edit quest
                                print("Edit quest: Type 'position x y' or 'back'")
                                edit_input = input().strip()
                                match edit_input.split():
                                    case ['position', x, y] if x.replace('.', '').replace('-', '').isdigit() and y.replace('.', '').replace('-', '').isdigit():
                                        current_chapter = edit_quest_in_chapter(current_chapter, selected_quest.id, edit_quest_position(selected_quest, float(x), float(y)))
                                        selected_quest = edit_quest_position(selected_quest, float(x), float(y))
                                        print("Quest position updated.")
                                    case ['back']:
                                        pass
                                    case _:
                                        print("Invalid edit command.")
                            case _:
                                print("Invalid. Use 'task <num>', 'reward <num>', 'edit', 'back', or 'exit'.")
                case ['edit']:
                    # Example edit
                    print("Edit mode: Type 'title <new_title>' or 'back'")
                    edit_input = input().strip()
                    match edit_input.split():
                        case ['title', *title]:
                            new_title = ' '.join(title)
                            current_chapter = edit_chapter_title(current_chapter, new_title)
                            print("Chapter updated.")
                        case ['back']:
                            pass
                        case _:
                            print("Invalid edit command.")
                case _:
                    print("Invalid. Try 'help'.")

    print("\nExiting FTB Quests CLI. Goodbye!")

if __name__ == "__main__":
    main()
