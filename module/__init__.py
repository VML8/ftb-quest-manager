"""
FTB Quest Viewer - A Python package for viewing and navigating FTB quest data.

This package provides tools to load, parse, and navigate FTB (Feed The Beast)
quest data from SNBT files.
"""

# Data navigation and viewing functions
from .view.display_chapters import display_chapters
from .view.display_quests import display_quests, display_quest_details
from .view.view import (
    display_task_reward_details as display_task_details,
    display_task_reward_details as display_reward_details
)
from .ftb_loader import (
                        find_chapters_directory, 
                        load_chapter_data, 
                        parse_chapters
                        )

# Data editing functions
from .quest_edit import (
                         #  Edit chapter functions
                         edit_chapter_title, 
                         edit_chapter_subtitle, 
                         edit_chapter_icon, 
                         edit_chapter_tags,
                         
                         #  Edit quest functions
                         add_quest_to_chapter, 
                         remove_quest_from_chapter, 
                         edit_quest_in_chapter, 
                         edit_quest_position,
                         
                         #  Edit task functions
                         add_task_to_quest, 
                         remove_task_from_quest, 
                         edit_task_in_quest, 
                         
                         #  Edit reward functions
                         add_reward_to_quest, 
                         remove_reward_from_quest, 
                         edit_reward_in_quest, 
                         
                         #  Create functions
                         create_task, 
                         create_reward, 
                         create_quest, 
                         create_chapter
                         )

# Model classes
from .model.quest_models import Chapter, Quest, Task, Reward, Item

__version__ = "1.0.0"
__all__ = [
    # Viewing functions
    "display_chapters",
    "display_quests",
    "display_quest_details",
    "display_task_reward_details",

    # Loading functions
    "find_chapters_directory",
    "load_chapter_data",
    "parse_chapters",

    # Model classes
    "Chapter",
    "Quest",
    "Task",
    "Reward",
    "Item",

    # Data editing functions
    "edit_chapter_title",
    "edit_chapter_subtitle",
    "edit_chapter_icon",
    "edit_chapter_tags",

    "add_quest_to_chapter",
    "remove_quest_from_chapter",

    "edit_quest_in_chapter",
    "edit_quest_position",
    
    "add_task_to_quest",
    "remove_task_from_quest",
    "edit_task_in_quest",

    "add_reward_to_quest",
    "remove_reward_from_quest",
    "edit_reward_in_quest",
    
    "create_task",
    "create_reward",
    "create_quest",
    "create_chapter",
]
