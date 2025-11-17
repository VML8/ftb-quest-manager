import os
from typing import List

class NavigationState:
    '''
    Used to store navigation alias.
    Checks are handled outside of this class.
    '''

    cwd_name = os.path.basename(os.getcwd())
        
    def __init__(self):
        self.state : List[str] = [NavigationState.cwd_name]



    def back(self):
        self.state.pop()
    
    def reset(self):
        self.state = [NavigationState.cwd_name]    
    
    def get_status(self):
        printout = " > ".join(self.state)
        print(printout + ' > ')
    
    def get_place(self):
        count = len(self.state)
        match count:
            case 1:
                return 'chapters'
            case 2:
                return 'quests'
            case 3:
                return 'tasks'
            case 4:
                return 'rewards'

    def go(self, navigate_deeper_to: str):

        if '>' in navigate_deeper_to:
            navigate_deeper_to = navigate_deeper_to.strip().split('>')
        elif '/' in navigate_deeper_to:
            navigate_deeper_to = navigate_deeper_to.strip().split('/')
        
        if isinstance(navigate_deeper_to, list):
            self.state.extend(navigate_deeper_to)
        else:
            self.state.append(navigate_deeper_to)