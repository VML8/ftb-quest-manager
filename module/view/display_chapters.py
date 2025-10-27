from colorama import init, Fore, Style
from typing import Dict
from ..model.quest_models import Chapter

init(autoreset=True)

def display_chapters(data: Dict[str, Chapter]) -> None:
    """Display the list of chapters."""
    print("\n" + Fore.CYAN + "="*40)
    print(Fore.YELLOW + Style.BRIGHT + "CHAPTERS")
    print(Fore.CYAN + "="*40)

    chapter_keys = sorted(data.keys())
    for i, key in enumerate(chapter_keys):
        chapter = data[key]
        print(f"[{i}] {key.upper()} (Quests: {len(chapter.quests)}, Group: {chapter.group[:8]}...)")