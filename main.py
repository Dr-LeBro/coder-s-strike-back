import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# To debug: print("Debug messages...", file=sys.stderr)


class Boost:
    def __init__(self):
        self.best_checkpoint = -1
    
    def searchBestBoost(self, checkpoints):
        best_check_dist = 0
        best_check_angle = 180
        checkpoints_count = len(checkpoints)
        for i in range(checkpoints_count) :
            if best_check_dist <= checkpoints[i]["dist"] and checkpoints[i]["dist"] > 6000:
                if best_check_angle >= abs(checkpoints[i]["angle"]):
                    self.best_checkpoint = i
                    best_check_dist = checkpoints[i]["dist"]
                    best_check_angle = checkpoints[i]["angle"]
        print("best boost: "+str(self.best_checkpoint), file=sys.stderr)

class Rounds:
    def __init__(self):
        self.checkpoints = []
        self.rounds_count = 0
        self.on_start = False
        self.flag_round_two = False
        self.boost = Boost()
    
    def setCheckpoint(self, x, y, dist, angle):
        checkpoint_tuple = {"x": x, "y": y, "dist": dist, "angle": angle}
        self.checkpoints.append(checkpoint_tuple)
        
    def newCheckpoint(self, x, y ,dist, angle):
        if self.checkpointExist(x, y) == -1:
            self.setCheckpoint(x, y, dist, angle)
    
    def checkpointExist(self, x, y):
        checkpoints_count = len(self.checkpoints)
        for i in range(checkpoints_count) :
            if self.checkpoints[i]["x"] == x and self.checkpoints[i]["y"] == y:
                return i
        return -1

    def printCheckpoints(self):
        checkpoints_count = len(self.checkpoints)
        for i in range(checkpoints_count) :
            print("["+str(i)+"] "+ "x: "+ str(self.checkpoints[i]["x"]) + " y: " + str(self.checkpoints[i]["y"]) + " dist: " + str(self.checkpoints[i]["dist"]) + " angle: " + str(self.checkpoints[i]["angle"]), file=sys.stderr)
    
    def checkRoundNumber(self, x, y):
        if len(self.checkpoints) > 0 and self.checkpoints[0]["x"] == x and self.checkpoints[0]["y"] == y:
            if self.on_start == False:
                self.rounds_count += 1
            self.on_start = True
        else:
            self.on_start = False
    
    def setNextCheckpoint(self, x, y):
        self.nextCheckpoint = self.checkpointExist(x, y)
    
    
    def mainCall(self, x, y, dist, angle):
        self.checkRoundNumber(x, y)
        #print("round: "+str(self.rounds_count), file=sys.stderr)
        if self.rounds_count <= 1:
            self.newCheckpoint(x, y, dist, angle)
        self.setNextCheckpoint(x, y)
        print("new checkpoint: ["+str(self.nextCheckpoint)+"]", file=sys.stderr)
    
    def boostCall(self, x, y):
        if self.rounds_count == 2:
            if self.flag_round_two == False:
                self.boost.searchBestBoost(self.checkpoints)
                self.flag_round_two = True
            elif self.boost.best_checkpoint != -1 and self.checkpoints[self.boost.best_checkpoint]["x"] == x and self.checkpoints[self.boost.best_checkpoint]["y"] == y:
                return True
        return False
        
    def callPositionCheckpoint(self):
        if self.checkpoints[self.nextCheckpoint]["angle"] > 0:
            return "right"
        elif self.checkpoints[self.nextCheckpoint]["angle"] < 0:
            return "left"
        else:
            return "straight"
                
            
class Thrust:    
    def __init__(self):
        self.thrust = 0
    
    def setThrust(self, dist, angle, reduct):
        if dist < 3999:
            if abs(angle) > 10:
                self.thrust = 70
            elif abs(angle) > 5:
                self.thrust = 50
            else:
                self.thrust = 100
        elif dist <= 4000:
            if abs(angle) > 90:
                self.thrust = 0
            else:
                self.thrust = 100
        else:
            self.thrust = 150 - abs(angle)
        print("angle: "+str(angle)+"° "+"dist: "+str(dist)+"m "+str(reduct), file=sys.stderr)
        self.thrust -= reduct
        self.capThrust()
    
    def capThrust(self):
        if self.thrust > 100:
            self.thrust = 100
        elif self.thrust < 0:
            self.thrust = 0
    
    def askForBoost(self, doBoost, angle):
        if self.thrust >= 90 and doBoost and abs(angle) < 10:
            self.thrust = "BOOST"

class Opponent:
    def __init__(self):
        self.opponent_x = 0
    
    def detectOpponent(self, x, y, opponent_x, opponent_y):
        dist_x = opponent_x - x
        dist_y = opponent_y - y
        dist = abs(dist_x) + abs(dist_y)
        print("->"+str(dist), file=sys.stderr)
        if dist <= 2000:
            print("ALERTE", file=sys.stderr)
            return 20
        if dist <= 1000:
            print("COLLISION", file=sys.stderr)
            return 50
        return 0

# INIT

rounds = Rounds()
thrustObject = Thrust()
opponentObject = Opponent()
rapport = 1.8
# game loop
while True:
    thrust = 100
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    rounds.mainCall(next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle)
    # Write an action using print
    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"

    thrustObject.setThrust(next_checkpoint_dist, next_checkpoint_angle, opponentObject.detectOpponent(x,y,opponent_x,opponent_y))
    thrustObject.askForBoost(rounds.boostCall(next_checkpoint_x, next_checkpoint_y), next_checkpoint_angle)
    
        
    #rounds.printCheckpoints()    
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " "+str(thrustObject.thrust))
    
    
    