import os
from module.controller.snbt_to_json_loader import snbt_to_json
from typing import Dict, Any, List
import json
from rich import print

def list_to_id_dict(lst: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert a list of dicts containing 'id' into a dict keyed by id."""
    new_dict = {}
    for item in lst:
        new_dict[item["id"]] = item
    return new_dict
    # return {item["id"]: item for item in lst} # I can't read this smh

def ftb_loader(cwd = os.getcwd()) -> Dict[str, Any]:
    _lang_data = {} # temp, don't use, for processing only

    parsed_lang_data = {}
    chapter_group_data = {}

    #!################################!#
    # Container for tasks and rewards
    #? For add or remove tasks/rewards
    data_quest_tasks_container = {}
    data_quest_rewards_container = {}

    # Use this variable
    data = {} # Chapter data access
    
    # Deeper data reference, use for direct access
    data_quests = {}
    data_quest_rewards = {}
    data_quest_tasks = {}
    #!################################!#

    # Masking full directory path
    _relpath_start = os.path.join(cwd, "config", "ftbquests")
    _to_quest = os.path.join(_relpath_start, "quests")

    # File path
    chapters_dir = os.path.join(_to_quest, "chapters")
    lang_file = os.path.join(_to_quest, "lang", "en_us.snbt")
    chapter_groups_file = os.path.join(_to_quest, "chapter_groups.snbt")
    
    # Open en_us lang file
    print(f"[bold green]Opening Lang data[/bold green] \n{os.path.relpath(lang_file, _relpath_start)}")
    try :
        with open(lang_file, "r") as f:
            _lang_data = json.loads(snbt_to_json(f.read()))
    except FileNotFoundError:
        print("[bold red]Lang file not found[/bold red]")
    except PermissionError:
        print("[bold red]Permission denied[/bold red]")

    # Open chapter_groups_data
    print(f"[bold green]Opening Chapter groups data[/bold green] \n{os.path.relpath(chapter_groups_file, _relpath_start)}")
    try:
        with open(chapter_groups_file, "r") as f:
            chapter_group_data = json.loads(snbt_to_json(f.read()))
            chapter_group_data = chapter_group_data.get("chapter_groups")
    except FileNotFoundError:
        print("[bold red]Chapter groups data file not found[/bold red]")
    except PermissionError:
        print("[bold red]Permission denied[/bold red]")

    # Load each chapter file into a dictionary
    print(f"[bold green]Loading Chapter data[/bold green] \n{os.path.relpath(chapters_dir, _relpath_start)}")
    try :
        for file in os.listdir(chapters_dir):
            with open(os.path.join(chapters_dir, file), "r") as f:
                obj = json.loads(snbt_to_json(f.read()))
                filename = obj["filename"]
                data[filename] = obj
    except FileNotFoundError:
        print("[bold red]Chapter file not found[/bold red]")
    except PermissionError:
        print("[bold red]Permission denied[/bold red]")

    # Parse Lang Data
    for key, value in _lang_data.items():
        context, id, attr = key.split(".")
        parsed_lang_data[id] = {'context': context, 'attr': attr, 'value': value}

    #! ############ !#
    #! PHASE 1 DONE !#
    #! ############ !#
    #? Parsed data into :

    # data as dict[str, Any]
    # parsed_lang_data as dict[str, Any]
    # ? { 
    # ?   {'id'} :
    # ?     {'context': context, 'attr': attr, 'value': value} 
    # ? }

    # chapter_group_data as list[dict['id', str(id)]]
    # ---------------------------------^ Literal 'id' string
    #! ############ !#

    # Transform for easier navigation
    for chapter in data:
        _quest_list = data[chapter]["quests"]

        # list to dict
        _quest_dict = {}
        for quest in _quest_list:
            _key = quest["id"]                 # take quest id
            
            # list to dict for task and rewards
            if "rewards" in quest and isinstance(quest["rewards"], list):
                quest["rewards"] = list_to_id_dict(quest["rewards"])
            if "tasks" in quest and isinstance(quest["tasks"], list):
                quest["tasks"] = list_to_id_dict(quest["tasks"])
            
            _quest_dict[_key] = quest          # put as key on temp dict   
        data[chapter]["quests"] = _quest_dict  # replace list with dict


    # Map Language to data (not chapter_group)
    for _id, _value in parsed_lang_data.items():
        match _value['context']:
            
            case 'chapter':
                for _ch_key, chapter in data.items():
                    if chapter['id'] == _id:
                        data[_ch_key][_value['attr']] = _value['value']
            
            case 'quest':
                for _ch_key, chapter in data.items():
                    for _q_key, quest in chapter['quests'].items():
                        if quest['id'] == _id:
                            data[_ch_key]['quests'][_q_key][_value['attr']] = _value['value']

            case 'task':
                for _ch_key, chapter in data.items():
                    for _q_key, quest in chapter['quests'].items():
                        for _t_key, task in quest['tasks'].items():
                            if task['id'] == _id:
                                data[_ch_key]['quests'][_q_key]['tasks'][_t_key][_value['attr']] = _value['value']

            case 'reward':
                for _ch_key, chapter in data.items():
                    for _q_key, quest in chapter['quests'].items():
                        for _r_key, reward in quest['rewards'].items():
                            if reward['id'] == _id:
                                data[_ch_key]['quests'][_q_key]['rewards'][_r_key][_value['attr']] = _value['value']

    # Store deeper reference in variable, flattened quest
    for chapter in data: # loop chapter data ! get chapter key

        if "quests" in data[chapter]: # check if chapter has 'quests' key
            for quest in data[chapter]["quests"]: # loop quest inside chapter value (using chapter key)
                
                # take title as key, fallback to id if no title
                if "title" in data[chapter]["quests"][quest]:
                    _for_flat_quest_key = data[chapter]["quests"][quest]["title"]
                else:
                    _for_flat_quest_key = data[chapter]["quests"][quest]["id"]
                
                # flatten data_quest | using 'title' or 'id'
                data_quests[_for_flat_quest_key] = data[chapter]["quests"][quest]
                

                # flatten data_quest_rewards
                if "rewards" in data[chapter]['quests'][quest]:

                    _rewards = data[chapter]["quests"][quest]["rewards"]

                    #! Required Reference
                    data_quest_rewards_container[_for_flat_quest_key] = _rewards
                    
                    for reward_id, reward_dict in _rewards.items():
                        _for_flat_reward_key = reward_dict.get("title", reward_dict.get("id"))
                        
                        # flatten data_quest rewards
                        data_quest_rewards[_for_flat_reward_key] = reward_dict

                # flatten data_quest_tasks
                if "tasks" in data[chapter]['quests'][quest]:

                    _tasks = data[chapter]["quests"][quest]["tasks"]

                    #! Required Reference
                    data_quest_tasks_container[_for_flat_quest_key] = _tasks

                    for task_id, task_dict in _tasks.items():
                        _for_flat_task_key = task_dict.get("title", task_dict.get("id"))
                        
                        # flatten data_quest tasks (individual task)
                        data_quest_tasks[_for_flat_task_key] = task_dict

    return data, data_quests, data_quest_rewards, data_quest_tasks, data_quest_rewards_container, data_quest_tasks_container
