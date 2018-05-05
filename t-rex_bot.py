import os
import time
import datetime
import webbrowser
import pyautogui
import mss
import mss.tools
from numpy import array
from PIL import Image, ImageGrab, ImageOps 


# game area position
game_area_x = 680
game_area_y = 234
game_area_width = 1200
game_area_height = 258

# obstacle line position
line_rel_y = 220
line_rel_x_start = 175
line_rel_x_end = 400

# game over position
g_x = 418
g_y = 70
r_x = 790
r_y = 76
e_x = 574
e_y = 85
o_x = 643
o_y = 85
button_x = 631
button_y = 134

# colors (rgb)
background = (247, 247, 247)
black = (83, 83, 83)
white = (255, 255, 255)
night = (0,0,0)
night_obstacle = (172, 172, 172)


def startGame():
	os.system("networksetup -setairportpower airport off")  # turn off wi-fi to play T-Rex game
	time.sleep(0.1)
	webbrowser.open('https://www.google.it')  # visit any page
	time.sleep(0.5)


def jump():
	pyautogui.keyUp('down')
	time.sleep(0.001)
	pyautogui.keyDown('space')
	time.sleep(0.18)
	pyautogui.keyUp('space')
	time.sleep(0.001)
	pyautogui.keyDown('down')
	time.sleep(0.001)


def screenshot(save):
	with mss.mss() as sct:
	    # screen part to capture
	    game_area = (game_area_x/2, game_area_y/2, (game_area_x+game_area_width)/2, (game_area_y+game_area_height)/2)

	    sct_img = sct.grab(game_area)  # screenshot

	    im = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')  # convert to Image object

	if(save):
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
		im.save(os.getcwd() + '/screenshots/screenshot_' + now + '.png', 'PNG')

	return im


def checkIfGameOver(im):
	# chech presence of specific dark pixels (part of 'game over' letters and button) at specific points
	g_present = im.getpixel((g_x, g_y)) != im.getpixel((g_x+1, g_y+1))
	e_present = im.getpixel((e_x, e_y)) != im.getpixel((e_x+1, e_y+1))
	o_present = im.getpixel((o_x, o_y)) != im.getpixel((o_x+1, o_y+1))
	r_present = im.getpixel((r_x, r_y)) != im.getpixel((r_x+1, r_y+1))
	button_present = im.getpixel((button_x, button_y)) != im.getpixel((button_x+1, button_y+1))

	return g_present and e_present and o_present and r_present and button_present


def getJumpingWindow(time_elapsed):
	# account for t-rex acceleration
	if (time_elapsed < 20):
		return line_rel_x_start, line_rel_x_end
	elif (time_elapsed < 40):
		return line_rel_x_start+100, line_rel_x_end+100
	elif (time_elapsed < 60):
		return line_rel_x_start+200, line_rel_x_end+200
	elif (time_elapsed < 80):
		return line_rel_x_start+300, line_rel_x_end+300
	else:
		return line_rel_x_start+400, line_rel_x_end+400


def obstacleAhead(im, time_elapsed):
	# chech presence of 2 consecutive pixel of different color (part of an obstacle) in an horizontal line
	line_start, line_end = getJumpingWindow(time_elapsed)

	for i in range(line_start, line_end-1):
		if (im.getpixel((i, line_rel_y)) != im.getpixel((i+1, line_rel_y))):
			return True
	return False


def main():
	startGame()
	starting_time = time.time()
	jump()  # start game
	
	game_over = False
	while(True):
		im = screenshot(save=False)

		if checkIfGameOver(im):
			print('game over')
			break

		time_elapsed = time.time()-starting_time
		if obstacleAhead(im, time_elapsed):
			jump()
		
	im = screenshot(save=True)  # save screenshot to analyze death condition
	os.system("networksetup -setairportpower airport on")  # turn on wi-fi

	 
if __name__ == '__main__':
	main()