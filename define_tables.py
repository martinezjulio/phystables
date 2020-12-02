import pickle
from phystables.constants import *

# helper classes to define tables
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

class WallData: 
    def __init__(self, upperleft, lowerright):
        self.upperleft = upperleft
        self.lowerright = lowerright
class GoalData:
    def __init__(self, upperleft, lowerright, onreturn, color):
        self.upperleft = upperleft
        self.lowerright = lowerright
        self.onreturn = onreturn
        self.color = color 
class BallData:
    def __init__(self, initpos, initvel, color):
        self.initpos = initpos
        self.initvel = initvel
        self.color = color
class TableData:
    def __init__(self, dims, walls, goals, balls):
        self.dims = dims
        self.walls = walls
        self.goals = goals
        self.balls = balls

        
if __name__ == "__main__":
    # table 0
    walls = [WallData(upperleft=(200, 150), lowerright=(500,250)),
             WallData(upperleft=(450, 400), lowerright=(550,600)),
             WallData(upperleft=(650, 100), lowerright=(700,200)),
             WallData(upperleft=(650, 200), lowerright=(1000,250))]
    
    goals = [GoalData(upperleft=(250,550), lowerright=(350,600), onreturn=REDGOAL, color=RED),
             GoalData(upperleft=(650,550), lowerright=(750,600), onreturn=GREENGOAL, color=GREEN)]
    
    balls = [BallData(initpos=(70, 500), initvel=(300, -300), color=PURPLE),
             BallData(initpos=(250, 100), initvel=(300, 300), color=GOLD)]
    
    tableDims = (1000,600)
    tables = [TableData(tableDims, walls, goals, balls)]

    # table 1
    walls = [WallData(upperleft=(175,350), lowerright=(225,600)),
             WallData(upperleft=(375,350), lowerright=(425,600)),
             WallData(upperleft=(575,350), lowerright=(825,400)),
             WallData(upperleft=(525,350), lowerright=(575,600))]
    
    goals = [GoalData(upperleft=(250,550), lowerright=(350,600), onreturn=REDGOAL, color=RED),
             GoalData(upperleft=(650,550), lowerright=(750,600), onreturn=GREENGOAL, color=GREEN)]
    
    balls = [BallData(initpos=(100, 300), initvel=(140, -400), color=PURPLE),
             BallData(initpos=(700, 150), initvel=(300, 300), color=GOLD)]
    
    tableDims = (1000,600)
    tables.append(TableData(tableDims, walls, goals, balls))

    # table 2
    walls = [WallData(upperleft=(350,0), lowerright=(400,250)),
             WallData(upperleft=(0,350), lowerright=(250,400)),
             WallData(upperleft=(900,250), lowerright=(950,500)),
             WallData(upperleft=(500,350), lowerright=(550,600))]
    
    goals = [GoalData(upperleft=(50,50), lowerright=(150,100), onreturn=REDGOAL, color=RED),
             GoalData(upperleft=(600,400), lowerright=(700,450), onreturn=GREENGOAL, color=GREEN)]
    
    balls = [BallData(initpos=(450, 450), initvel=(-300, -300), color=PURPLE),
             BallData(initpos=(650, 200), initvel=(300, 300), color=GOLD)]
    
    tableDims = (1000,600)
    tables.append(TableData(tableDims, walls, goals, balls))

    # table 3
    goals = [GoalData(upperleft=(300,275), lowerright=(500,325), onreturn=REDGOAL, color=RED),
             GoalData(upperleft=(500,275), lowerright=(700,325), onreturn=GREENGOAL, color=GREEN)]

    balls = [BallData(initpos=(600,50), initvel=(0,100), color=PURPLE),
             BallData(initpos=(450,550), initvel=(0,-100), color=GOLD)]

    tableDims = (1000,600)
    tables.append(TableData(tableDims, [], goals, balls))

    ## SAVE
    save_object(tables, 'tables_metadata.pkl')
