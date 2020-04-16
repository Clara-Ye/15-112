# Classes and functions to get the Dorm mode to work:
  # the Hero class
  # functions to get the hero do activities

from cmu_112_graphics import *

class Hero(object):
  
  def __init__(self, location, coordinates, speed):
    self.health = 100

    self.location = location
    self.coordinates = coordinates
    self.speed = speed
    self.rushCapacity = self.health

class DormMode(Mode):
  def appStarted(mode):
    mode.background = mode.loadImage('images\dormPic.png')
    scale = min(mode.width/mode.background.size[0], mode.height/mode.background.size[1])
    mode.background = mode.scaleImage(mode.background, scale)
    mode.bedLocation = (mode.width*20/75, mode.height*32/55)
    mode.windowLocation = (mode.width*7/75, mode.height*9/55)
    mode.scheLocation = (mode.width*60/75, mode.height*12/55)
    # hardcode locations for desk and clock
    mode.r = mode.width/50

  def mousePressed(mode, event):
    if ((mode.windowLocation[0] - mode.r < event.x < mode.windowLocation[0] + mode.r) and
        (mode.windowLocation[1] - mode.r < event.y < mode.windowLocation[1] + mode.r)):
       mode.app.setActiveMode(mode.app.mapMode)
    if ((mode.scheLocation[0] - mode.r < event.x < mode.scheLocation[0] + mode.r) and
        (mode.scheLocation[1] - mode.r < event.y < mode.scheLocation[1] + mode.r)):
       mode.app.setActiveMode(mode.app.scheMode)
    # click on bed to call Hero.sleep()
    # click on desk to call Hero.study()

  def redrawAll(mode, canvas):
    canvas.create_image(mode.width/2, mode.height/2, 
                        image = ImageTk.PhotoImage(mode.background))
    canvas.create_oval(mode.bedLocation[0] - mode.r, mode.bedLocation[1] - mode.r,
                       mode.bedLocation[0] + mode.r, mode.bedLocation[1] + mode.r,
                       fill = "pink")
    canvas.create_oval(mode.windowLocation[0] - mode.r, mode.windowLocation[1] - mode.r,
                       mode.windowLocation[0] + mode.r, mode.windowLocation[1] + mode.r,
                       fill = "pink")
    canvas.create_oval(mode.scheLocation[0] - mode.r, mode.scheLocation[1] - mode.r,
                       mode.scheLocation[0] + mode.r, mode.scheLocation[1] + mode.r,
                       fill = "pink")
    # draw the interactive point for desk
    # draw clock with time
    #canvas.create_text(mode.width/2, mode.height/2, font = "Arial 20 bold",
                       #text = f"Time: ")

print("Loaded dorm")
