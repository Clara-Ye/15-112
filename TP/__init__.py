# integrates all the modes and classes:
  # four modes: Login, Dorm, Schedule, Map
  # class Hero

# modes not yet completely separated into files
  # this file still has Login and Schedule

# loosely adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingModalApp

from cmu_112_graphics import *
from _map import *
from dorm import *

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
    app.month = 1 # Jan
    app.date = 12 # 12th
    app.day = 7   # Mon
    (app.hours, app.mins) = (20, 0) # 8:00 pm
    app.hero = Hero(None, None, 1*app.width/1125)
    app.createGraph()
  
  def createGraph(app):
    # hardcode the locations -> graph
    app.createBuildings()
    app.graph = {app.UC:  {app.WH:  app.UC.getDistance(app.WH),
                           app.PCA: app.UC.getDistance(app.PCA),  
                           app.CUT: app.UC.getDistance(app.CUT),
                           app.TC:  app.UC.getDistance(app.TC),
                           app.WWG: app.UC.getDistance(app.WWG),
                           app.GS:  app.UC.getDistance(app.GS)},
                 app.PCA: {app.UC:  app.PCA.getDistance(app.UC),  
                           app.CUT: app.PCA.getDistance(app.CUT),
                           app.GHC: app.PCA.getDistance(app.GHC),
                           app.WH:  app.PCA.getDistance(app.WH)},
                 app.CUT: {app.UC:  app.CUT.getDistance(app.UC),
                           app.PCA: app.CUT.getDistance(app.PCA),
                           app.FE:  app.CUT.getDistance(app.FE),
                           app.TC:  app.CUT.getDistance(app.TC),
                           app.FAL: app.CUT.getDistance(app.FAL)},
                 app.GHC: {app.PCA: app.GHC.getDistance(app.PCA),
                           app.NSH: app.GHC.getDistance(app.NSH)},
                 app.DH:  {app.FE:  app.DH.getDistance(app.FE),
                           app.MAL: app.DH.getDistance(app.MAL),
                           app.WEH: app.DH.getDistance(app.WEH)},
                 app.TC:  {app.UC:  app.TC.getDistance(app.UC),
                           app.CUT: app.TC.getDistance(app.CUT),
                           app.FAL: app.TC.getDistance(app.FAL),
                           app.MM:  app.TC.getDistance(app.MM),
                           app.WWG: app.TC.getDistance(app.WWG)},
                 app.DON: {app.MM:  app.DON.getDistance(app.MM),
                           app.GYM: app.DON.getDistance(app.GYM),
                           app.HIL: app.DON.getDistance(app.HIL),
                           app.RES: app.DON.getDistance(app.RES),
                           app.SF:  app.DON.getDistance(app.SF)},
                 app.BH:  {app.PH:  app.BH.getDistance(app.PH),
                           app.MAL: app.BH.getDistance(app.MAL),
                           app.FE:  app.BH.getDistance(app.FE),
                           app.HL:  app.BH.getDistance(app.HL)},
                 app.PH:  {app.HH:  app.PH.getDistance(app.HH),
                           app.MAL: app.PH.getDistance(app.MAL),
                           app.BH:  app.PH.getDistance(app.BH),
                           app.WEH: app.PH.getDistance(app.WEH)},
                 app.HL:  {app.BH:  app.HL.getDistance(app.BH),
                           app.FE:  app.HL.getDistance(app.FE),
                           app.CFA: app.HL.getDistance(app.CFA)},
                 app.NSH: {app.GHC: app.NSH.getDistance(app.GHC),
                           app.WEH: app.NSH.getDistance(app.WEH)},
                 app.WEH: {app.PH:  app.WEH.getDistance(app.PH),
                           app.MAL: app.WEH.getDistance(app.MAL),
                           app.DH:  app.WEH.getDistance(app.DH),
                           app.NSH: app.WEH.getDistance(app.NSH),
                           app.HH:  app.WEH.getDistance(app.HH)},
                 app.WWG: {app.UC:  app.WWG.getDistance(app.UC),
                           app.TC:  app.WWG.getDistance(app.TC),
                           app.MM:  app.WWG.getDistance(app.MM),
                           app.RES: app.WWG.getDistance(app.RES),
                           app.GS:  app.WWG.getDistance(app.GS)},
                 app.RES: {app.GS:  app.RES.getDistance(app.GS),
                           app.SF:  app.RES.getDistance(app.SF),
                           app.HIL: app.RES.getDistance(app.HIL),
                           app.DON: app.RES.getDistance(app.DON),
                           app.WWG: app.RES.getDistance(app.WWG)},
                 app.MM:  {app.DON: app.MM.getDistance(app.DON),
                           app.DON: app.MM.getDistance(app.WWG),
                           app.TC:  app.MM.getDistance(app.TC),
                           app.FAL: app.MM.getDistance(app.FAL),
                           app.POS: app.MM.getDistance(app.POS),
                           app.GYM: app.MM.getDistance(app.GYM)},
                 app.GS:  {app.UC:  app.GS.getDistance(app.UC),
                           app.WWG: app.GS.getDistance(app.WWG),
                           app.RES: app.GS.getDistance(app.RES),
                           app.SF:  app.GS.getDistance(app.SF)},
                 app.SF:  {app.GS:  app.SF.getDistance(app.GS),
                           app.RES: app.SF.getDistance(app.RES),
                           app.HIL: app.SF.getDistance(app.HIL)},
                 app.HIL: {app.SF:  app.HIL.getDistance(app.SF),
                           app.RES: app.HIL.getDistance(app.RES),
                           app.DON: app.HIL.getDistance(app.DON)},
                 app.GYM: {app.DON: app.GYM.getDistance(app.DON),
                           app.MM:  app.GYM.getDistance(app.MM),
                           app.POS: app.GYM.getDistance(app.POS)},
                 app.POS: {app.CFA: app.POS.getDistance(app.CFA),
                           app.FAL: app.POS.getDistance(app.FAL),
                           app.MM:  app.POS.getDistance(app.MM),
                           app.GYM: app.POS.getDistance(app.GYM)},
                 app.CFA: {app.FE:  app.CFA.getDistance(app.FE),
                           app.FAL: app.CFA.getDistance(app.FAL),
                           app.POS: app.CFA.getDistance(app.POS),
                           app.HL:  app.CFA.getDistance(app.HL)},
                 app.FE:  {app.CUT: app.FE.getDistance(app.CUT),
                           app.MAL: app.FE.getDistance(app.MAL),
                           app.CFA: app.FE.getDistance(app.CFA),
                           app.HL:  app.FE.getDistance(app.HL),
                           app.BH:  app.FE.getDistance(app.BH),
                           app.DH:  app.FE.getDistance(app.DH),
                           app.FAL: app.FE.getDistance(app.FAL)},
                 app.MAL: {app.WEH: app.MAL.getDistance(app.WEH),
                           app.DH:  app.MAL.getDistance(app.DH),
                           app.BH:  app.MAL.getDistance(app.BH)},
                 app.FAL: {app.CUT: app.FAL.getDistance(app.CUT),
                           app.FE:  app.FAL.getDistance(app.FE),
                           app.CFA: app.FAL.getDistance(app.CFA),
                           app.POS: app.FAL.getDistance(app.POS),
                           app.MM:  app.FAL.getDistance(app.MM),
                           app.TC:  app.FAL.getDistance(app.TC)},
                 app.HH:  {app.WEH: app.HH.getDistance(app.WEH),
                           app.PH:  app.HH.getDistance(app.PH)},
                 app.WH:  {app.TQ:  app.WH.getDistance(app.TQ),
                           app.MOR: app.WH.getDistance(app.MOR),
                           app.UC:  app.WH.getDistance(app.UC),
                           app.PCA: app.WH.getDistance(app.PCA)},
                 app.TQ:  {app.TEP: app.TQ.getDistance(app.TEP),
                           app.MOR: app.TQ.getDistance(app.MOR),
                           app.WH:  app.TQ.getDistance(app.WH),
                           app.GHC: app.TQ.getDistance(app.GHC)},
                 app.TEP: {app.ROF: app.TEP.getDistance(app.ROF),
                           app.TQ:  app.TEP.getDistance(app.TQ)},
                 app.MOR: {app.STE: app.MOR.getDistance(app.STE),
                           app.WH:  app.MOR.getDistance(app.WH),
                           app.TQ:  app.MOR.getDistance(app.TQ)},
                 app.STE: {app.MUD: app.STE.getDistance(app.MUD),
                           app.ROF: app.STE.getDistance(app.ROF),
                           app.MOR: app.STE.getDistance(app.MOR)},
                 app.MUD: {app.ROF: app.MUD.getDistance(app.ROF),
                           app.STE: app.MUD.getDistance(app.STE)},
                 app.ROF: {app.MUD: app.ROF.getDistance(app.MUD),
                           app.STE: app.ROF.getDistance(app.STE),
                           app.TEP: app.ROF.getDistance(app.TEP)}}

  def createBuildings(app):
    app.buildings = set()
    
    app.UC = Building("UC", "Cohon University Center", 
                      (app.width*760/1125, app.height*510/825))
    Gallo = DiningPlace("Gallo", "El Gallo de Oro", 
                        (app.width*760/1125, app.height*510/825),
                        "Dining", 1, app.UC, [(10, 22)], 0)
    ABP = DiningPlace("ABP", "Au Bon Pain at Skibo Cafe", 
                      (app.width*760/1125, app.height*510/825),
                      "Dining", 2, app.UC, [(8, 2)], 2)

    app.DH = Building("Doherty", "Doherty Hall", 
                      (app.width*562/1125, app.height*598/825))
    DH2210 = Classroom("DH2210", "DH2210", (app.width*562/1125, app.height*598/825),  
                       "Classroom", 2, app.DH, [(0, 24)], "15112 Lecture")

    app.GHC = Building("Gates", "Gates & Hillman Centers", 
                       (app.width*561/1125, app.height*523/825))
    CLR = Classroom("Clusters", "Clusters", 
                    (app.width*561/1125, app.height*523/825),
                    "Classroom", 5, app.GHC, [(0, 24)], "15112 Lab")
    Rour = DiningPlace("Rour Cafe", "Rour Cafe - Tazza D'Oro",
                       (app.width*561/1125, app.height*523/825), "Dining",
                       3, app.GHC, [(0, 24)], 2)

    app.PCA = Building("Purnell Center", "Purnell Center for the Arts",
                       (app.width*641/1125, app.height*532/825))

    app.DON = Building("Donner", "Donner House", 
                       (app.width*892/1125, app.height*655/825))
    MyRoom = InnerPlace("My Room", "My Room", 
                        (app.width*892/1125, app.height*655/825),
                        "Dorm", 2, app.DON, [(0, 24)])

    app.CUT = Building("The Cut", "The Cut", 
                       (app.width*667/1125, app.height*588/825))

    app.TC = Building("Tennis Court", "Tennis Court",
                      (app.width*753/1125, app.height*610/825))
    TennisCourt = InnerPlace("Tennis Court", "Tennis Court",
                             (app.width*753/1125, app.height*610/825),
                             "Fitness", 1, app.TC, [(0, 24)])

    app.BH = Building("Baker", "Baker Hall", 
                      (app.width*533/1125, app.height*696/825))
    
    app.PH = Building("Potter", "Potter Hall",
                      (app.width*443/1125, app.height*672/825))
    
    app.HL = Building("Hunt", "Hunt Library",
                       (app.width*631/1125, app.height*732/825))
    MaggieMurph = DiningPlace("Maggie Murph", "Maggie Murph Café",
                              (app.width*631/1125, app.height*732/825), 
                              "Dining", 1, app.HL, [(8, 22)], 2)                   
    
    app.NSH = Building("Newell-Simon", "Newell-Simon Hall",
                       (app.width*494/1125, app.height*511/825))
    iNoodle = DiningPlace("iNoodle", "iNoodle",
                          (app.width*494/1125, app.height*511/825), "Dining",
                          3, app.NSH, [(10, 20)], 2)

    app.WEH = Building("Wean", "Wean Hall",
                       (app.width*478/1125, app.height*580/825))
    LaPrima = DiningPlace("La Prima", "La Prima Espresso",
                          (app.width*491/1125, app.height*580/825), "Dining",
                          5, app.WEH, [(8, 18)], 1)
    
    app.WWG = Building("West Wing", "West Wing",
                       (app.width*832/1125, app.height*570/825))
    
    app.RES = Building("Resnik", "Resnik House",
                       (app.width*904/1125, app.height*596/825))
    
    app.MM = Building("Margaret Morrison", "Margaret Morrison Carnegie Hall",
                      (app.width*797/1125, app.height*646/825))
    
    app.GS = Building("Gesling Stadium", "Gesling Stadium",
                      (app.width*887/1125, app.height*530/825))
    
    app.SF = Building("Soccer Field", "Intramural Soccer Field",
                      (app.width*1004/1125, app.height*579/825))
    
    app.HIL = Building("The Hill", "The Hill",
                       (app.width*1000/1125, app.height*674/825))

    app.GYM = Building("Skibo Gymnasium", "Skibo Gymnasium",
                       (app.width*813/1125, app.height*736/825))

    app.POS = Building("Posner", "Posner Hall",
                       (app.width*752/1125, app.height*712/825))
    
    app.CFA = Building("CFA", "College of Fine Arts",
                       (app.width*692/1125, app.height*689/825))
    
    app.FE = Building("The Fence", "The Fence",
                      (app.width*652/1125, app.height*634/825))
    
    app.MAL = Building("The Mall", "The Mall",
                       (app.width*537/1125, app.height*648/825))
    
    app.FAL = Building("Fine Arts Lot", "Fine Arts Lot",
                       (app.width*726/1125, app.height*650/825))
    
    app.HH = Building("Hamerschlag", "Hamerschlag Hall",
                      (app.width*413/1125, app.height*611/825))
    
    app.WH = Building("Warner", "Warner Hall",
                      (app.width*659/1125, app.height*431/825))

    app.TQ = Building("Tepper Quad", "Tepper Quad",
                      (app.width*582/1125, app.height*351/825))

    app.TEP = Building("Tepper", "Tepper Building",
                       (app.width*533/1125, app.height*321/825))

    app.MOR = Building("Morewood", "Morewood Gardens",
                       (app.width*674/1125, app.height*319/825))

    app.MUD = Building("Mudge", "Mudge House",
                       (app.width*699/1125, app.height*168/825))

    app.STE = Building("Stever", "Stever House",
                       (app.width*710/1125, app.height*228/825))

    app.ROF = Building("Rez", "Residence on the Fifth",
                       (app.width*409/1125, app.height*172/825))

app = MyModalApp(width=1125, height=825)
