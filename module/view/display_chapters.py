from colorama import init, Fore, Style
from typing import Dict
from ..model.quest_models import Chapter

init(autoreset=True)

# Styling Constants
TITLE_STYLE = Fore.YELLOW
GROUP_STYLE = Fore.LIGHTBLACK_EX
ID_STYLE = Fore.CYAN
INDEX_STYLE = Fore.LIGHTBLACK_EX

def display_chapters(data: Dict[str, Chapter]) -> None:
    """Display the list of chapters."""
    print("\n" + Fore.CYAN + "="*40)
    print(Fore.YELLOW + "CHAPTERS")
    print(Fore.CYAN + "="*40)

    chapter_keys = sorted(data.keys())
    for i, key in enumerate(chapter_keys):
        group_name = data[key].group if data[key].group else "[no group]"
        quest_count = len(data[key].quests)
        info_text = f"{GROUP_STYLE}{group_name}{Style.RESET_ALL} ({quest_count})"
        print(f"[{INDEX_STYLE}{i}{Style.RESET_ALL}] {TITLE_STYLE}{key.upper()}{Style.RESET_ALL} {info_text}")