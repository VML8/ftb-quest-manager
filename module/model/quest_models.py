from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict, Any, Union

# For rewards, tasks, etc
class Item(BaseModel):
    id: str
    count: Optional[int] = 1
    components: Optional[Dict[str, Any]] = None

class QuestComponent(BaseModel):
    id: str
    type: str
    # 'item' will hold the Item model if type is 'item'
    item: Optional[Item] = None
    # Use Any for other type-specific fields (e.g., 'advancement' for an advancement task)
    advancement: Optional[str] = None
    optional_task: Optional[bool] = False
    count: Optional[Union[int, str]] = None # Some counts are Longs ('8L' in SNBT, handled as int or string here)

class Task(QuestComponent):
    pass

class Reward(QuestComponent):
    pass

class Quest(BaseModel):
    id: str
    x: float
    y: float
    dependencies: List[str] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    rewards: List[Reward] = Field(default_factory=list)

    # Optional Settings
    hide_details_until_startable: Optional[bool] = False
    hide_dependency_lines: Optional[bool] = False
    hide_lock_icon: Optional[bool] = False
    hide_text_until_complete: Optional[bool] = False
    hide_until_deps_complete: Optional[bool] = False
    hide_until_deps_visible: Optional[bool] = False

class Chapter(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None

    id: str
    icon: Optional[Item] = None
    filename: str
    group: str
    tags: List[str] = Field(default_factory=list)
    order_index: int

    quests: List[Quest] = Field(default_factory=list)

    # Optional Settings from here on

    # Visual
    disable_completion_toast: Optional[bool] = False
    default_quest_shape: Optional[str] = "circle"
    # Visibility
    default_hide_dependency_lines: Optional[bool] = False
    hide_quest_details_until_startable: Optional[bool] = False
    hide_quests_until_deps_visible: Optional[bool] = False
    # Misc
    autofocus_quest_id: Optional[str] = None
    default_progression_mode: Optional[str] = "linear"
    default_repeatable_quest: Optional[bool] = False
    default_item_task_consume_items: Optional[bool] = False
    sequential_task_completion: Optional[bool] = False
