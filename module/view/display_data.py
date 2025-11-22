from rich import print
import os, sys
from os import path
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

def display_object(data, target_navigation):
    console = Console()
    panel: Panel = None
    print_buffer = []
    child_panel = []

    def handle_container(container_name, parent_value, i = len(target_navigation)-1):
        key_buffer = []
        for k2, v2 in parent_value.items():
            key_buffer.append(k2)
        child_panel.append(Panel.fit(f"{'\n'.join(key_buffer)}", title=f"{target_navigation[i]}", border_style="green", subtitle=f"{len(key_buffer)} {container_name}"))


    match len(target_navigation):
        case 1:
            for k,v in data.items():
                print_buffer.append(k)
            panel = Panel.fit(f"{'\n'.join(print_buffer)}", title=f"{target_navigation[0]}", border_style="green", subtitle=f"{len(data)} Chapters")
        case 2:
            for k,v in data[target_navigation[1]].items():  # second item
                if k == 'quests':    # when found quests
                    handle_container('Quests', v)
                else:
                    print_buffer.append(f"{k} : {v}")
            panel = Panel.fit(f"{'\n'.join(print_buffer)}", title=f"{target_navigation[1]}", border_style="green", subtitle="Chapter")
        case 3:
            for k,v in data[target_navigation[1]]['quests'][target_navigation[2]].items():
                if k == 'tasks':
                    handle_container('Tasks', v)
                elif k == 'rewards':
                    handle_container('Rewards', v)
                else:
                    print_buffer.append(f"{k} : {v}")
            panel = Panel.fit(f"{'\n'.join(print_buffer)}", title=f"{target_navigation[2]}", border_style="green", subtitle="Quests")
        case 4:
            # Need context check since it branches to either tasks or rewards.
            # if target_navigation[3] in 'tasks'. use navigate to tasks data at data[target_navigation[1]]['quests'][target_navigation[2]['tasks'][target_navigation[3]]]
            _data_ref = data[target_navigation[1]]['quests'][target_navigation[2]]
            _target_id = target_navigation[3]

            for container_name in ("tasks", "rewards"):
                container = _data_ref.get(container_name, {})
                if _target_id in container:
                    for k,v in container[_target_id].items():
                        print_buffer.append(f"{k} : {v}")  
            panel = Panel.fit(f"{'\n'.join(print_buffer)}", title=f"{target_navigation[3]}", border_style="green", subtitle="Chapter")
                

    console.print(panel)
    if len(child_panel) != 0 :
        console.print(Columns(child_panel))
    

# if __name__ == "__main__":

    # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    # if project_root not in sys.path:
    #     sys.path.insert(0, project_root)
        
    # from module.controller.ftb_loader import ftb_loader
    # from module.navigation.NavigationState import NavigationState

    # cwd = path.abspath("V:\\Quest_Manager\\tests\\cwd_test")
    # data, data_quests, data_quest_rewards, data_quest_tasks, data_quest_task_container, data_quest_rewards_container = ftb_loader(cwd)
    # navigation = NavigationState()

    # navigation.go('welcome')
    # navigation.go('2B665C5D30FC7E86')
    # navigation.go('65AC6680636196E9')
    # display_object(data, navigation.state)