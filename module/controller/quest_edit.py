from typing import List, Optional

from .quest_models import Chapter, Quest, Task, Reward, Item, QuestComponent


def edit_chapter_title(chapter: Chapter, new_title: str) -> Chapter:
    """Update the title of a chapter."""
    return chapter.model_copy(update={'title': new_title})


def edit_chapter_subtitle(chapter: Chapter, new_subtitle: str) -> Chapter:
    """Update the subtitle of a chapter."""
    return chapter.model_copy(update={'subtitle': new_subtitle})


def edit_chapter_icon(chapter: Chapter, new_icon: Optional[Item]) -> Chapter:
    """Update the icon of a chapter."""
    return chapter.model_copy(update={'icon': new_icon})


def edit_chapter_tags(chapter: Chapter, new_tags: List[str]) -> Chapter:
    """Update the tags of a chapter."""
    return chapter.model_copy(update={'tags': new_tags})


def add_quest_to_chapter(chapter: Chapter, quest: Quest) -> Chapter:
    """Add a new quest to the chapter's quests list."""
    updated_quests = chapter.quests + [quest]
    return chapter.model_copy(update={'quests': updated_quests})


def remove_quest_from_chapter(chapter: Chapter, quest_id: str) -> Chapter:
    """Remove a quest from the chapter by its ID."""
    updated_quests = [q for q in chapter.quests if q.id != quest_id]
    return chapter.model_copy(update={'quests': updated_quests})


def edit_quest_in_chapter(chapter: Chapter, quest_id: str, updated_quest: Quest) -> Chapter:
    """Replace a quest in the chapter with an updated version."""
    updated_quests = [updated_quest if q.id == quest_id else q for q in chapter.quests]
    return chapter.model_copy(update={'quests': updated_quests})


def edit_quest_position(quest: Quest, new_x: float, new_y: float) -> Quest:
    """Update the position of a quest."""
    return quest.model_copy(update={'x': new_x, 'y': new_y})


def add_task_to_quest(quest: Quest, task: Task) -> Quest:
    """Add a new task to the quest's tasks list."""
    updated_tasks = quest.tasks + [task]
    return quest.model_copy(update={'tasks': updated_tasks})


def remove_task_from_quest(quest: Quest, task_id: str) -> Quest:
    """Remove a task from the quest by its ID."""
    updated_tasks = [t for t in quest.tasks if t.id != task_id]
    return quest.model_copy(update={'tasks': updated_tasks})


def edit_task_in_quest(quest: Quest, task_id: str, updated_task: Task) -> Quest:
    """Replace a task in the quest with an updated version."""
    updated_tasks = [updated_task if t.id == task_id else t for t in quest.tasks]
    return quest.model_copy(update={'tasks': updated_tasks})


def add_reward_to_quest(quest: Quest, reward: Reward) -> Quest:
    """Add a new reward to the quest's rewards list."""
    updated_rewards = quest.rewards + [reward]
    return quest.model_copy(update={'rewards': updated_rewards})


def remove_reward_from_quest(quest: Quest, reward_id: str) -> Quest:
    """Remove a reward from the quest by its ID."""
    updated_rewards = [r for r in quest.rewards if r.id != reward_id]
    return quest.model_copy(update={'rewards': updated_rewards})


def edit_reward_in_quest(quest: Quest, reward_id: str, updated_reward: Reward) -> Quest:
    """Replace a reward in the quest with an updated version."""
    updated_rewards = [updated_reward if r.id == reward_id else r for r in quest.rewards]
    return quest.model_copy(update={'rewards': updated_rewards})


def create_task(task_id: str, task_type: str, **kwargs) -> Task:
    """Create a new Task with given parameters."""
    return Task(id=task_id, type=task_type, **kwargs)


def create_reward(reward_id: str, reward_type: str, **kwargs) -> Reward:
    """Create a new Reward with given parameters."""
    return Reward(id=reward_id, type=reward_type, **kwargs)


def create_quest(quest_id: str, x: float, y: float, **kwargs) -> Quest:
    """Create a new Quest with given parameters."""
    return Quest(id=quest_id, x=x, y=y, **kwargs)


def create_chapter(chapter_id: str, filename: str, group: str, order_index: int, **kwargs) -> Chapter:
    """Create a new Chapter with given parameters."""
    return Chapter(id=chapter_id, filename=filename, group=group, order_index=order_index, **kwargs)