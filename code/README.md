#  Research track 1, assignment 1

## Description of the assignment

In this assignment a robot has to move inside a map in anti-clockwise direction.
As it moves it must avoid touching the golden tokens, and when the robot encounters a silver token it should grab it, and move it behind itself.

## How to run the code
from a linux shell:
```
$python2 run.py assignment1_Murgia_Camillo.py
```



## Pseudocode
In this pseudocode is described how the program should work, what are the decision and the action that the robot takes, and how it gets to take them.

```
def drive(speed, seconds):
	Function for setting a linear velocity
	
	start moving forward (or backward)
	wait for 'seconds' time
	stop moving

def turn(speed, seconds):
	Function for setting an angular velocity
	
	start the right and left motors in opposite direction
	wait for 'seconds'
	stop the motors

def find_token_silver():
	find the closest silver token within a certain distance 'min_dist' and a 	
	certain angle of view 'angle_view' in front of the robot
    Return distance and direction of the token
	
	define: dist = 100
	define: min_dist = 2
	define: angle_view = 45
	for all the token:
		if color == silver-token 
			AND it is in front of the robot 
				AND it is the closest one:
					dist = token.dist
					rot_y = token.rot_y
	if dist == 100
		no token presence
	else
		return dist, rot_y
		
	

def find_token_gold():
	Find the closest gold token
	Return distance and direction

	define: dist = 100
	for all the token:
		if color == gold-token
			and it is the closest one
				dist = token.dist
				rot_y = token.rot_y
	if dist == 100
		no token presence
	else
		return dist, rot_y


def find_gold_corner():
	Find the closest gold token to the right and to the left side of the robot
	inside a cone of 20 degree 'v_a*2'
	Return the distance of the 2 closest gold tokens on for each side

	define: dist_right = 100
	define: dist_left = 100
	define: v_a = 10
	
	for all the token
		if color == gold-token
			AND into the cone on the left side
				AND the closest one
					dist_left = token.dist
	
	for all the token
		if color == gold-token
			AND into the cone on the right side
				AND the closest one
					dist_right = token.dist
	
	return dist_right, dist_left


def allign_angle(actual_angle):
	On the base of the args: actual_angle decide if turn clockwise, turn
	anticlock-wise or do not turn
	The calls of this function performs "a small turn" in this way multiple calls
	of the function can perform a precise turn until the correct allignment

	NOTE: (-a_th, a_th) is the bound of the correct allignment
	Return:
	0 if alligned with the closest silver-token
	1 if not alligned with the closest silver-token

	if actual_angle into the bound
		return 0
	else
		if actual_angle > 0
			call 'turn' function on clockwise direction
			and return 1
		else
			call 'turn' function on anti-clockwise direction
			and return 1

def grab_and_thow_token():
	Grab the token in from of the robot
	turn of ~180 degree
	release the token
	turn back
	
		

def check_silver_token():
	call find_token_silver() function
	on the base of the return:
		do nothing -> there is no silver token in closer to the robot to be taken
		call get_silver() function -> there is a close silver token to be taken	

def get_silver():
	When the robot is in range to get a silver token:
	allign the robot, drive it in the way of the tooken and grab it

	distance, angle = find_token_silver()
	
	//turn until the robot is alligned with the silver token
	define: flag = 1
	while(flag)
		flag = allign_angle(angle)
		distance, angle = find_token_sliver()
	
	if the robot is close enough to the token
		call 'grab_and_throw_token()' function
	else
		call 'drive' function and drive forward closer to the silver token

		
def avoid_gold():
	Check the presence of gold token within a certain distance 'min_dist' and,
	in case of presence, avoid it turning in the opposite direction.
	It also perform turning when the robot is at a corner of its path,
	if the gold token is in front of the robot it (nearly always) means that the
	robot is close to a corner and ti have to perform a 90 degree turn in 
	the correct direction. Otherwise is the gold token is on the left or on the
	right of the robot it just has to adjust its trajectory in order to
	do not hit the gold token.
	
	define: min_dist = 0.7
	distance, angle = find_token_gold()
	if the robot is too close
		if the gold token is on the left of the robot
			call 'allign_border(0)' function and turn clockwise
		elif the gold token is on the right of the robot
			call 'allign_borger(1)' function and turn anti-clockwise
		elif the gold token is in front of the robot
			call 'corner()' function and perform a 90 degree turn in the correct
			direction

def corner():
	call a function to check the distance of the closest gold token on the
	 right and on the left side of the robot, and decide the correct direction
	 to turn.
	 The right direction is the one where the distance to the closest gold token
	 is grater, this is trivially deductable from the conformation of the arena.

	dist_right, dist_left = find_token_gold_corner()
	if dist_right > dist_left
		call 'turn' function and turn clockwise of ~90 degree
	else
		call 'turn' function and turn anti-clockwise of ~90 degree
	 

def allign_border(direction):
	turn until angle between the heading of the robot and the distance vector from
	the robot to the closest gold token is ~|90|

	args:
	direction = 0 -> perform a clockwise turn
	direction = 1 -> perform an anti-clockwise turn
	
	if required a clockwise turn
		flag = 1
		while(flag)
			call 'turn' function in clockwise direction of a small step
			distance, angle = find_token_gold()
			if the target angle is achived
				flag = 0
	else
		flag = 1
		while(flag)
			call 'turn' function in anti-clockwise direction of a small step
			distance, angle = find_token_gold()
			if the target angle is achived
				flag = 0

def main():
	In an infinite while loop calls the 3 main component of the guidance algorithm

	while(1)
		call 'avoid_gold()' function
		call 'drive()' function and drive forward of a small step
		call 'check_silver_token()' funtion
```

## Tuning of the algorithm

The hardest part in the development of this specific guidance algorithm is the tuning of all the parameter. In particular it is extremely important for a correct, nice and fast execution of the task, by the robot, to properly tunes all the bound present in the algorithm. The most important ones are the angles of vision and decision between a turn when the robot is too close to a wall, or when the robot is approaching to a corner in its path. An other important parameter is the minimum distance for triggering the turning procedure, and the minimum distance for starting the procedure related to the grabbing of silver token.








<!--stackedit_data:
eyJoaXN0b3J5IjpbMTg2NTIxMDI4Nl19
-->
