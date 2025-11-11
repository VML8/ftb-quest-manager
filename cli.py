from module.controller.ftb_loader import ftb_loader
from module.navigation.NavigationState import NavigationState
import os
from typing import List

def main():
    os.system("cls")
    
    data, data_quests, data_quest_rewards, data_quest_tasks, data_quest_task_container, data_quest_rewards_container = ftb_loader()

    navigation = NavigationState()
    navigation.get_status()
    navigation.go('chapter')
    navigation.get_status()
    navigation.back()
    navigation.get_status()
    navigation.go('chapter/quest')
    navigation.get_status()
    navigation.reset()
    navigation.go('chapter > quest')
    navigation.get_status()

if __name__ == "__main__":
    main()