import os
from module.controller.ftb_loader import ftb_loader
from module.navigation.NavigationState import NavigationState
from module.view.display_data import display_object

def main():
    os.system("cls")
    print(os.environ.get('DEBUG_CWD'))
    path = os.getcwd()

    data, data_quests, data_quest_rewards, data_quest_tasks, data_quest_task_container, data_quest_rewards_container = ftb_loader(path)

    # print(data)

    navigation = NavigationState()
    
    navigation.go('welcome')
    navigation.go('2B665C5D30FC7E86')

    print(navigation.state)
    

if __name__ == "__main__":
    main()