from phystables import BasicTable, SimpleTable

###################################
# Helper Functions To Make Tables #
###################################

def make_wall(ulx, uly, lrx, lry):
    '''Walls'''
    return ((ulx, uly), (lrx, lry))

def make_goal(ulx, uly, lrx, lry):
    '''Goals'''
    return make_wall(ulx, uly, lrx, lry)

def make_ball(px, py, vx, vy):
    '''Balls'''
    return ((px, py), (vx, vy))

def make_table(B1, B2, G1, G2, walls, B1_on=True, B2_on=True, dim=(1000,600)):
    '''Tables'''
    if (not B1_on) and (not B2_on):
        raise Exception("Need at least one ball to simulate")
    if B1_on and B2_on:
        table = BasicTable(dims=dim)
    else:
        table = SimpleTable(dims=dim)
    for wall in walls:
        ul, lr = wall
        table.add_wall(ul, lr)
    table.add_goal(G1[0], G1[1], REDGOAL, RED)  # first argument RED
    table.add_goal(G2[0], G2[1], GREENGOAL, GREEN)  # second argument GREEN
    if B1_on:
        table.add_ball(initpos=B1[0], initvel=B1[1], color=GOLD)
    if B2_on:
        table.add_ball(initpos=B2[0], initvel=B2[1], color=PURPLE)
    return table


########################
# Collection of Tables #
########################

CG1 = make_goal(250,550,350,600)
CG2 = make_goal(650,550,750,600)

CW1 = make_wall(175,350,225,600)
CW2 = make_wall(375,350,425,600)
CW3 = make_wall(575,350,825,400)
CW4 = make_wall(525,350,575,600)

CB1 = make_ball(100,300,140,-400)
CB2 = make_ball(700,150,300,300)

tableC_both = make_table(CB1,CB2,CG1,CG2,{CW1,CW2,CW3,CW4})
tableC_gold = make_table(CB1,CB2,CG1,CG2,{CW1,CW2,CW3,CW4}, B2_on=False)
tableC_purp = make_table(CB1,CB2,CG1,CG2,{CW1,CW2,CW3,CW4}, B1_on=False)

########################

FG1 = make_goal(50,50,150,100)
FG2 = make_goal(600,400,700,450)

FW1 = make_wall(350,0,400,250)
FW2 = make_wall(0,350,250,400)
FW3 = make_wall(900,250,950,500)
FW4 = make_wall(500,350,550,600)

FB1 = make_ball(450,450,-300,-300)
FB2 = make_ball(650,200,300,300)

tableF_both = make_table(FB1,FB2,FG1,FG2,{FW1,FW2,FW3,FW4})
tableF_gold = make_table(FB1,FB2,FG1,FG2,{FW1,FW2,FW3,FW4}, B2_on=False)
tableF_purp = make_table(FB1,FB2,FG1,FG2,{FW1,FW2,FW3,FW4}, B1_on=False)

