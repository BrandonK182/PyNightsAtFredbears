# PyNightsAtFred's
A PyGame recreation of the popular Five Nights at Freddy's game featuring legally distinct enemies
- Fred
- Bunnie
- Chick
- Vixen

# DEMO
![alt text](https://github.com/BrandonK182/PyNightsAtFredbears/blob/main/PyNightDemo.gif)

# Current Features
- Map layout reminiscent of official FNAF game
- Enemies moving around the map
- Door stops enemies from entering
- Game over when enemies reach player location
- Player wins by reaching 6 AM
- 5 Nights that can be played ranging in difficulty
- Energy meter that depletes and causes player to lose if reaches 0
- Vixen's special mechanic with a timer that slowly ticks down but pauses when a player views the camera

# How To Play
- run main.py
- PyGame should launch in a window
- click to begin the game
- Try to reach 6 AM without letting enemies in or the power reach 0
- Beat all 5 Nights to win the game

## The Security Office
The office is the first thing you will see as you enter the game.
### Doors
- Pressing the red door button will cause it to close the door and turn green.
- Closed doors will block enemies that are standing next to you but drains power.
- Pressing the green door button will open the door and turn the button red.
### Lights
- Pressing and holding the grey lights button will light up the office window alerting you if an enemy is right outside
- Lights use up power to keep on.
### Cameras
- Hover your mouse over the rectangle at the bottom to flip up the camera screen.
- When in the camera screen, the bottom right will have a mini map of the building.
- Clicking the white squares will switch which camera is being viewed.
- Viewing the cameras consumes power.
- Hove your mouse over the bottom rectangle to return to office view.

## Enemies
### Bunnie
- Bunnie is represented by the blue dot.
- Goes through the left hallway towards the player.
- Faster than any other enemy, but also leaves just as fast.

### Chick
- Chick is represented by the yellow dot.
- Goes through the right hallway towards the player.
- Slower movement to Bunnie, but lingers outside the office longer too.

### Vixen
- Vixen is represented by the red dot.
- Special mechanic which requires the player to monitor them.
- If not watched will begin a mad sprint towards the office.

### Fred
- Fred is represented by the brown dot.
- Slowest of the enemy and also approaches through the right hallway.
- Will not leave the hallway once they enter.

## PLANNED STRETCH FEATURES
- Start menu
- Camera visuals
- Prevent Enemies from entering occupied rooms
