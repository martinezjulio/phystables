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
    walls = [WallData(upperleft=(200, 150), lowerright=(500,250))]
    walls.append(WallData(upperleft=(450, 400), lowerright=(550,600)))
    walls.append(WallData(upperleft=(650, 100), lowerright=(700,200)))
    walls.append(WallData(upperleft=(650, 200), lowerright=(1000,250)))
    goals = [GoalData(upperleft=(250,550), lowerright=(350,600), onreturn=REDGOAL, color=RED)]
    goals.append(GoalData(upperleft=(650,550), lowerright=(750,600), onreturn=GREENGOAL, color=GREEN))
    balls = [BallData(initpos=(70, 500), initvel=(300, -300), color=PURPLE)]
    balls.append(BallData(initpos=(250, 100), initvel=(300, 300), color=GOLD))
    tableDims = (1000,600)
    tables = [TableData(tableDims, walls, goals, balls)]

    # table 1
    walls = [WallData(upperleft=(200, 150), lowerright=(500,250))]
    walls.append(WallData(upperleft=(450, 400), lowerright=(550,600)))
    walls.append(WallData(upperleft=(650, 100), lowerright=(700,200)))
    walls.append(WallData(upperleft=(650, 200), lowerright=(1000,250)))
    goals = [GoalData(upperleft=(250,550), lowerright=(350,600), onreturn=REDGOAL, color=RED)]
    goals.append(GoalData(upperleft=(650,550), lowerright=(750,600), onreturn=GREENGOAL, color=GREEN))
    balls = [BallData(initpos=(70, 500), initvel=(300, -300), color=PURPLE)]
    balls.append(BallData(initpos=(250, 100), initvel=(300, 300), color=GOLD))
    tableDims = (1000,600)
    tables.append([TableData(tableDims, walls, goals, balls)])

    # table 3
    walls = [WallData(upperleft=(200, 150), lowerright=(500,250))]
    walls.append(WallData(upperleft=(450, 400), lowerright=(550,600)))
    walls.append(WallData(upperleft=(650, 100), lowerright=(700,200)))
    walls.append(WallData(upperleft=(650, 200), lowerright=(1000,250)))
    goals = [GoalData(upperleft=(250,550), lowerright=(350,600), onreturn=REDGOAL, color=RED)]
    goals.append(GoalData(upperleft=(650,550), lowerright=(750,600), onreturn=GREENGOAL, color=GREEN))
    balls = [BallData(initpos=(70, 500), initvel=(300, -300), color=PURPLE)]
    balls.append(BallData(initpos=(250, 100), initvel=(300, 300), color=GOLD))
    tableDims = (1000,600)
    tables.append([TableData(tableDims, walls, goals, balls)])

    ## SAVE
    save_object(tables, 'tables_metadata.pkl')