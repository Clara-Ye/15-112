# integrates all the modes and classes:
  # four modes: Login, Dorm, Schedule, Map
  # class Hero

# modes not yet separated into files
# Map Mode does not work unless copy-paste code from map_ into this file, debug later

# loosely adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingModalApp

from cmu_112_graphics import *
from map_ import *
from hero import *

class LoginMode(Mode):

  def appStarted(mode):
    mode.buttonW, mode.buttonH = mode.width/4, mode.height/10
    mode.space = mode.height/8

  def redrawAll(mode, canvas):
    canvas.create_text(mode.width/2, 100, text = "Login Screen",
                       font = "Arial 26 bold")
    canvas.create_rectangle(mode.width/2 - mode.buttonW/2, mode.height/2,
                            mode.width/2 + mode.buttonW/2, mode.height/2 + mode.buttonH)
    canvas.create_rectangle(mode.width/2 - mode.buttonW/2, 
                            mode.height/2 + mode.space,
                            mode.width/2 + mode.buttonW/2, 
                            mode.height/2 + mode.space + mode.buttonH)
    canvas.create_rectangle(mode.width/2 - mode.buttonW/2, 
                            mode.height/2 + mode.space*2,
                            mode.width/2 + mode.buttonW/2, 
                            mode.height/2 + mode.space*2 + mode.buttonH)
    canvas.create_text(mode.width/2, mode.height/2 + mode.buttonH/2,
                       text = "New Game", font = "Arial 20 bold")
    canvas.create_text(mode.width/2, mode.height/2 + mode.buttonH/2 + mode.space,
                       text = "Load Game", font = "Arial 20 bold")
    canvas.create_text(mode.width/2, mode.height/2 + mode.buttonH/2 + mode.space*2,
                       text = "Quit Game", font = "Arial 20 bold")

  def mousePressed(mode, event):
    if ((event.x > mode.width/2 - mode.buttonW/2) and 
        (event.x < mode.width/2 + mode.buttonW/2) and
        (event.y > mode.height/2) and
        (event.y < mode.height/2 + mode.buttonH)):
      mode.app.hero.location = mode.app.DON
      mode.app.hero.coordinates = mode.app.DON.coordinates
      mode.app.setActiveMode(mode.app.dormMode)
    elif ((mode.width/2 - mode.buttonW/2 < event.x < mode.width/2 + mode.buttonW/2) and
          (mode.height/2 + mode.space*2 < event.y < mode.height/2 + mode.space*2 + mode.buttonH)):
      mode.app.quit()
      pass

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

  def timerFired(mode):
    # calculate time
    # calculate date
    pass

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

class ScheMode(Mode):

  def appStarted(mode):
    mode.background = mode.loadImage('images\schePic.png')
    scale = min(mode.width/mode.background.size[0], mode.height/mode.background.size[1])
    mode.background = mode.scaleImage(mode.background, scale)
    # load icons for going to dorm mode / map mode
    mode.iconWidth = mode.width/37.5
    (mode.dormIconX, mode.dormIconY) = (mode.width*4/75, mode.height*4/55)
    (mode.mapIconX, mode.mapIconY) = (mode.width*10/75, mode.height*4/55)

  def redrawAll(mode, canvas):
    canvas.create_image(mode.width/2, mode.height/2, 
                        image = ImageTk.PhotoImage(mode.background))
    # will be replaced by icon images:
    canvas.create_rectangle(mode.dormIconX-mode.iconWidth, mode.dormIconY-mode.iconWidth,
                            mode.dormIconX+mode.iconWidth, mode.dormIconY+mode.iconWidth, 
                            fill = "pink")
    canvas.create_rectangle(mode.mapIconX-mode.iconWidth, mode.mapIconY-mode.iconWidth,
                            mode.mapIconX+mode.iconWidth, mode.mapIconY+mode.iconWidth, 
                            fill = "cyan")
    canvas.create_text(mode.width/2, 100, text = "Schedule Screen",
                       font = "Arial 26 bold")
    
  def mousePressed(mode, event):
    if ((mode.dormIconX-mode.iconWidth < event.x < mode.dormIconX+mode.iconWidth) and
        (mode.dormIconY-mode.iconWidth < event.y < mode.dormIconY+mode.iconWidth)):
      # and if hero.location == "Dorm":
      mode.app.setActiveMode(mode.app.dormMode)
    elif ((mode.mapIconX-mode.iconWidth < event.x < mode.mapIconX+mode.iconWidth) and
          (mode.mapIconY-mode.iconWidth < event.y < mode.mapIconY+mode.iconWidth)):
      mode.app.setActiveMode(mode.app.mapMode)

class MyModalApp(ModalApp):
  def appStarted(app):
    app.loginMode = LoginMode()
    app.dormMode = DormMode()
    app.scheMode = ScheMode()
    app.mapMode = MapMode()
    app.setActiveMode(app.loginMode)
    app.timerDelay = 50
    app.hero = Hero(None, None, 10)
    app.createGraph()
  
  def createGraph(mode):
    # hardcode the locations -> graph
    mode.createBuildings()
    mode.graph = {mode.UC:  {mode.PCA: mode.UC.getDistance(mode.PCA),  
                             mode.CUT: mode.UC.getDistance(mode.CUT),
                             mode.TC:  mode.UC.getDistance(mode.TC)},
                  mode.PCA: {mode.UC:  mode.PCA.getDistance(mode.UC),  
                             mode.CUT: mode.PCA.getDistance(mode.CUT),
                             mode.GHC: mode.PCA.getDistance(mode.GHC)},
                  mode.CUT: {mode.UC:  mode.CUT.getDistance(mode.UC),
                             mode.PCA: mode.CUT.getDistance(mode.PCA),
                             mode.TC:  mode.CUT.getDistance(mode.TC),
                             mode.DH:  mode.CUT.getDistance(mode.DH)},
                  mode.GHC: {mode.PCA: mode.GHC.getDistance(mode.PCA)},
                  mode.DH:  {mode.CUT: mode.DH.getDistance(mode.CUT)},
                  mode.TC:  {mode.UC:  mode.TC.getDistance(mode.UC),
                             mode.CUT: mode.TC.getDistance(mode.CUT),
                             mode.DON: mode.TC.getDistance(mode.DON)},
                  mode.DON: {mode.TC:  mode.DON.getDistance(mode.TC)}}

  def createBuildings(mode):
    mode.buildings = set()
    
    mode.UC = Building("UC", "Cohon University Center", 
                       (mode.width*760/1125, mode.height*510/825))
    Gallo = DiningPlace("Gallo", "El Gallo de Oro", 
                        (mode.width*760/1125, mode.height*510/825),
                        "Dining", 0, mode.UC, [(10, 22)], 0)

    mode.DH = Building("Doherty", "Doherty Hall", 
                       (mode.width*562/1125, mode.height*598/825))
    DH2210 = Classroom("DH2210", "DH2210", (mode.width*562/1125, mode.height*598/825),  
                       "Classroom", 2, mode.DH, [(0, 24)], "15112 Lecture")

    mode.GHC = Building("Gates", "Gates & Hillman Centers", 
                        (mode.width*575/1125, mode.height*491/825))
    CLR = Classroom("Clusters", "Clusters", 
                    (mode.width*575/1125, mode.height*491/825),
                    "Classroom", 5, mode.GHC, [(0, 24)], "15112 Lab")
    Rour = DiningPlace("Rour Cafe", "Rour Cafe - Tazza D'Oro",
                       (mode.width*575/1125, mode.height*491/825), "Dining",
                       3, mode.GHC, [(0, 24)], 2)

    mode.PCA = Building("Purnell Center", "Purnell Center for the Arts",
                        (mode.width*641/1125, mode.height*510/825))

    mode.DON = Building("Donner", "Donner House", 
                        (mode.width*892/1125, mode.height*655/825))
    MyRoom = Place("My Room", "My Room", (mode.width*892/1125, mode.height*655/825),
                   "Dorm", 1, mode.DON, [(0, 24)])

    mode.CUT = Building("The Cut", "The Cut", 
                        (mode.width*661/1125, mode.height*592/825))

    mode.TC = Building("Tennis Court", "Tennis Court",
                       (mode.width*754/1125, mode.height*610/825))

app = MyModalApp(width=1125, height=825)