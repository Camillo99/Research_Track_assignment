from __future__ import print_function
import time
from sr.robot import *

"""

    $ python2 run.py assignment1V5.py
"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


turn_angle = 45
""" float: used in function avoid_gold as FOV for turning decision"""


R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
      seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
      seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0




def find_token_silver():
    """
    Find the closest silver token within a certain distance (min_dist) and a certain angle of
    view (angle_view) in front of the robot
    
    Return distance and direction of the token
    """

    dist = 100
    min_dist = 2
    angle_view = 45

    for token in R.see():
        if token.info.marker_type == 'silver-token' and token.rot_y > -(angle_view) and token.rot_y < angle_view and token.dist < min_dist and token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y

    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y
        

def find_token_gold():
    """
    Find the closest gold token

    return distance and direction
    """

    dist = 100
    for token in R.see():
        if token.info.marker_type == 'gold-token' and token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y

    if dist == 100:
        return -1 ,-1
    else:
        return dist, rot_y

def find_token_gold_corner():
    """
    find the closest gold token to the right and to the left of the robot
    inside a cone of 20 degree (v_a*2) for both side
    
    return the distance of the 2 closest gold tokens, one for each side
    
    """

    dist_right = 100
    dist_left = 100
    
    #angle view
    v_a = 10
    
    #check left side -> angle (rot_y) is negative
    for token2 in R.see():
        if 'gold-token' == token2.info.marker_type and  (token2.rot_y > -(90+v_a) and token2.rot_y < -(90-v_a) ) and token2.dist < dist_left :
            dist_left = token2.dist
    
     
    #check right side -> angle (rot_y) is positive
    for token in R.see():
        if 'gold-token' == token.info.marker_type and (token.rot_y > (90-v_a) and token.rot_y < (90+v_a) ) and token.dist < dist_right :
            dist_right = token.dist
     
        

    return dist_right, dist_left


#S_block
def allign_angle(actual_angle):
    """
    on the base of the args: actual_angle decide if turn clockwise, turn anti-clockwise, or do not turn
    
    the calls of this function perform "a small turn"
    in this way multiple call of allign_angle function can perform a precise turn
    until the correct allignment
    
    (-a_th, a_th) is the bound of a correct allignment
    
    return:
    0 if alligned w/ the target
    1 if not alligned w/ the target
    """
    
    
    
    if actual_angle > -a_th and actual_angle < a_th:
        #alligned with the target (silver token)
#        print('alligned')
        return 0
    else:
        #not alligned 
        #check if turn clockwise or anti-clockwise on the base of the sign of the actual_angle
        
        if actual_angle > 0:
            #turn clockwise
#            print('clockwise turn ',actual_angle)
            turn(20,0.05)
            #not alligned
            return 1
        else:
            #turn anti-clockwise
#            print('anti-clockwise turn ', actual_angle)
            turn(-20,0.05)
            #not alligned
            return 1



#S_block
def grab_and_throw_token():
    """
    grab a token, turn and left it behind.
    Then it turns again in the initial position
    """
    
    R.grab()
    turn(60,1)        #~180 degrees turn
    drive(20,1)
    R.release()
    drive(-20,1)    #avoid the hand effector to hits the token while turning back
    turn(-60,1)




def check_silver_token():
    """
    call find_token_silver() and on the base of the return:
    
    do nothing -> there is not silver token in the closest to be taken
    call get_silver() -> there is a close silver token to be taken
    """
    distance, angle = find_token_silver()
#    print(distance,' ',angle)
    
    if distance != -1 or angle != -1:
        #get the silver token
        print('silver found')
        get_silver()
	#else do nothing



def get_silver():
    """
    when the robot is in range to get a silver token: 
    allign the robot, drive it in the way of the token and grab it
    """
    
    distance, angle = find_token_silver()
    
    
    #turn until the robot is alligned w/ the silver token
    #in a while loop the robot keeps turning until the dissalligment angle is ~0
    flag = 1
    while (flag):
        flag = allign_angle(angle)
        distance, angle = find_token_silver()
    
    
    
    #now the robot is alligned w/ the closest silver token
    if distance < d_th:
        #grab
        print('grab a token')
        grab_and_throw_token()
    else:
        #drive forward
 #       print('drive forward')
        drive(80,0.05)
        

#G_block      
def avoid_gold():
    """
    check the presence of gold token wihin a certain distance (min_dist)
    and, in case of presence, avoid it turning in an other direction
    
    also perform turning when the robot is at a corner of its path
    
    if the gold token is in front of the robot it (nearly always) means the robot is close to a corner
    and it have to perform an 90 degree turn in the correct direction
    
    otherwise if the gold token is on the left or the right of the robot it just has to adjust its trajectory
    in order to do not hit the gold token
    """
    distance, angle = find_token_gold()
        
    #minimum distance the robot can gets close to a gold token before deciding to turns and avoids it 
    min_dist = 0.7
        
    if distance < min_dist:
#        print(distance, angle)
            #do something for avoiding a collision w/ a gold token
        if angle > -90 and angle < -turn_angle:
            #turn clockwise until angle ~ -90
            allign_border(0)
                
        elif angle > turn_angle and angle < 90:
            #turn anti-clockwise until angle ~ 90
            allign_border(1)
        elif angle >= -turn_angle and angle <= turn_angle:
            #the robot is close to a corner
            corner()
#       else:
            # angle c { [90,180] || [-180, -90] }
                
#       print('nothing to avoid golden token behind')
#   else:
#       print('nothing to avoid')    
    
    
def corner():
    """
    call a function to check the right and left distance to an other gold token 
    and decide the direction to take
    """
    dist_right, dist_left = find_token_gold_corner()
    
    print('right distance: ',dist_right)
    print('left distance: ',dist_left)
    #turn throught the grater distance
    if dist_right > dist_left:
        #turn right -> clockwise
        print('turn right')
        drive(-20,1)        #goes a bit backward to prevent hitting the obstable
        turn(30,1)          # ~90 degree turns
    else:
        #turn left  -> anti-clockwise
        print('turn left')
        
        drive(-20,1)        #goes a bit backward to prevent hitting the obstable
        turn(-30,1)         # ~90 degree turns



def allign_border(direction):
    """
    turn until angle is ~90 / -90 degree
    args:
    direction = 0 -> clockwise
    direction = 1 -> anti-clockwise
    """
 
    
    if direction == 0 :
        #clockwise
        print('clockwise')
        flag = 1
        while(flag):
            turn(20,0.05)
            distance, angle = find_token_gold()
#            print(angle)
            if angle < (-90):
                flag = 0
            
        
    else:
        #anti-clockwise
        print('anti-clockwise')
        flag = 1
        while(flag):
            turn(-20,0.05)
            distance, angle = find_token_gold()
#            print(angle)
            if angle > (90):
                flag = 0






def main():
    """
    main function
    in a infinite while loop call the 3 main component of the guidance algorithm
    """
    
    while(1):
        avoid_gold()
        drive(60,0.1)
        check_silver_token()
    
    

main()

