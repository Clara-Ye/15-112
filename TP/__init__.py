# integrates all the modes and classes:
  # four modes: Login, Dorm, Schedule, Map
  # classes: Hero, Course, Event, Location

# modes not yet completely separated into files
  # this file still has Login and Schedule

# loosely adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingModalApp

from cmu_112_graphics import *
from _map import *
from dorm import *
from schedule import *

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

class MyModalApp(ModalApp):
  def appStarted(app):
    app.loginMode = LoginMode()
    app.dormMode = DormMode()
    app.scheMode = ScheMode()
    app.mapMode = MapMode()
    app.setActiveMode(app.loginMode)
    
    app.timerDelay = 4
    app.clockDelay = 200
    app.month = 1 # Jan
    app.date = 12 # 12th
    app.day = 7   # Sun
    app.monthWrapArounds = {1: 31, 2: 29, 3: 31, 4: 30, 5:31}
    (app.hours, app.mins) = (22, 00) # 10:00 pm

    app.windowBorderX = app.width / 5
    app.windowBorderY = app.width / 8
    app.statusBarLength = app.width / 5
    app.statusBarWidth = app.height / 25
    app.buttonLength = app.width / 9
    app.buttonWidth = app.height / 15

    app.hero = Hero(75, 75, 75, 75, 75, None, None, (app.width/1125))
    app.events = dict()
    app.createGraph()
    app.createEvents()

  def clockTicked(app):
    app.setTimeFlowSpeed()
    app.mins += (app.timerDelay/app.clockDelay)
    # wrap around hours:
    if ((app.mins // 60) == 1):
      app.mins -= 60
      app.hours += 1
    # wrap around dates and days:
    if (app.hours == 24):
      app.hours -= 24
      app.date += 1
      app.day += 1
    if (app.day == 8): app.day = 1
    # wrap around months:
    (app.month, app.date) = app.wrapAroundMonth(app.month, app.date)

  def setTimeFlowSpeed(app):
    if (app._activeMode == app.scheMode) and (app.hero.moving == False):
      app.clockDelay = 400
    elif (app._activeMode == app.scheMode) and (app.hero.moving):
      app.clockDelay = float("inf")
    elif (app._activeMode == app.dormMode) and (app.hero.sleeping):
      app.clockDelay = 2
    elif (app.hero.inActivity):
      app.clockDelay = 20
    elif (app._activeMode != app.loginMode):
      app.clockDelay = 200

  def wrapAroundMonth(app, month, date):
    endOfMonth = app.monthWrapArounds[month]
    if (date > endOfMonth):
      month += 1
      date -= endOfMonth
    return (month, date)

  def getDisplayedDate(app):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Dec"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return f"{months[app.month-1]} {app.date}, {days[app.day-1]}"

  def getDisplayedTime(app, time):
    (hours, mins) = time
    hour = 12 if (12 <= hours < 13) else int(hours % 12)
    period = "am" if (hours < 12) else "pm"
    minute = str(int(mins))
    if (len(minute) < 2): minute = "0" + minute
    return f"{hour}:{minute}{period}"
  
  def getDisplayedDateAndTime(app):
    return f"{app.getDisplayedDate()}, {app.getDisplayedTime((app.hours, app.mins))}"

  def getTimeFloat(app, time):
    (hours, mins) = time
    return (hours + mins/60)

  def getTimeTuple(app, time):
    (hours, mins) = (time//1, time%1)
    return (int(hours), mins*60)

  def drawDateAndTime(app, canvas):
    canvas.create_rectangle(app.width/2 - app.width/13, 0,
                            app.width/2 + app.width/13, app.height/28,
                            fill = "white", width = 0)
    canvas.create_text(app.width/2, app.height/50, font = "Arial 12 bold",
                       text = app.getDisplayedDateAndTime())

  def adjustHeroStats(app):
    if (app.hero.sleeping):
      # things slow down when sleeping
      app.hero.sleepy -= 1.0 / app.clockDelay
      app.hero.hunger += 0.3 / app.clockDelay
      app.hero.stress -= 0.1 / app.clockDelay
    else:
      app.hero.hunger += 1.32 / app.clockDelay
      app.hero.stress -= 1.0 / app.clockDelay
      app.hero.health += 0.1 / app.clockDelay
    if (app.hero.eating): app.hero.hunger -= 25.0 / app.clockDelay
    elif (app.hero.studying):
      # will be adjusted according to hero.intelligence
      app.hero.stress += 2.0 / app.clockDelay
    elif (app.hero.socializing):
      # will be adjusted according to hero.social
      app.hero.stress -= 5.0 / app.clockDelay
    elif (app.hero.exercising):
      # will be adjusted according to hero.energy
      app.hero.stress -= 5.0 / app.clockDelay
    app.hero.sleepy += 0.33 / app.clockDelay
    # negative impacts on health:
    if (app.hero.sleepy >= 100): app.hero.health -= 0.2 / app.clockDelay
    if (app.hero.hunger >= 100): app.hero.health -= 0.5 / app.clockDelay
    if (app.hero.stress >= 100): app.hero.health -= 0.3 / app.clockDelay
    # keep stats in range:
    if (app.hero.sleepy < 0): app.hero.sleepy = 0
    elif (app.hero.sleepy > 100): app.hero.sleepy = 100
    if (app.hero.hunger < 0): app.hero.hunger = 0
    elif (app.hero.hunger > 100): app.hero.hunger = 100
    if (app.hero.stress < 0): app.hero.stress = 0
    elif (app.hero.stress > 100): app.hero.stress = 100
    if (app.hero.health < 0): app.hero.health = 0
    elif (app.hero.health > 100): app.hero.health = 100

  def adjustCourseAchievement(app):
    if app.hero.studying:
      courseStudied = app.dormMode.courseStudied
      courseStudied.achieve += 1.0 / app.clockDelay
      if (courseStudied.achieve > 100): courseStudied.achieve = 100
    elif app.hero.inClass:
      courseAttended = app.mapMode.courseAttended
      courseAttended.achieve += 2.0 / app.clockDelay
      if (courseAttended.achieve > 100): courseAttended.achieve = 100
    else:
      for course in app.courses:
        course.achieve -= 0.05 / app.clockDelay
        if (course.achieve < 0): course.achieve = 0
    app.hero.perfor = int(sum([course.achieve for course in app.courses]) / len(app.courses))

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
                           app.NSH: app.GHC.getDistance(app.NSH),
                           app.TQ:  app.GHC.getDistance(app.TQ)},
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
                           app.HIL: app.SF.getDistance(app.HIL),
                           app.DON: app.SF.getDistance(app.DON)},
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
                           app.BH:  app.MAL.getDistance(app.BH),
                           app.PH:  app.MAL.getDistance(app.PH)},
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
    app.UC = Building("UC", "Cohon University Center", 
                      (app.width*760/1125, app.height*510/825))
    app.Gallo = DiningPlace("Gallo", "El Gallo de Oro", 
                            (app.width*760/1125, app.height*510/825),
                            "Dining", 1, app.UC, [((10, 0), (22, 0))], 0)
    app.ABP = DiningPlace("ABP", "Au Bon Pain at Skibo Cafe", 
                          (app.width*760/1125, app.height*510/825),
                          "Dining", 2, app.UC, [((8, 0), (2, 0))], 2)
    app.GymUC = InnerPlace("Fitness Center", "Fitness Center", 
                           (app.width*760/1125, app.height*510/825),
                           "Fitness", 2, app.UC, [((9, 0), (22, 0))])
    app.ActRoomUC = InnerPlace("Activity Room", "Activity Room", 
                               (app.width*760/1125, app.height*510/825),
                               "Social", 2, app.UC, [((8, 0), (24, 0))])

    app.DH = Building("Doherty", "Doherty Hall", 
                      (app.width*562/1125, app.height*598/825))
    app.DH2210 = Classroom("DH2210", "DH2210", 
                           (app.width*562/1125, app.height*598/825),  
                           "Classroom", 2, app.DH, [((0, 0), (24, 0))], 
                           "15112 Lecture")

    app.GHC = Building("Gates", "Gates & Hillman Centers", 
                       (app.width*561/1125, app.height*523/825))
    app.CLR = Classroom("Clusters", "Clusters", 
                        (app.width*561/1125, app.height*523/825),
                        "Classroom", 5, app.GHC, [((0, 0), (24, 0))], 
                        "15112 Lab")
    app.Rour = DiningPlace("Rour Cafe", "Rour Cafe - Tazza D'Oro",
                           (app.width*561/1125, app.height*523/825), "Dining",
                           3, app.GHC, [((8, 0), (22, 0))], 2)

    app.PCA = Building("Purnell Center", "Purnell Center for the Arts",
                       (app.width*641/1125, app.height*532/825))

    app.DON = Building("Donner", "Donner House", 
                       (app.width*892/1125, app.height*655/825))
    app.MyRoom = InnerPlace("My Room", "My Room", 
                            (app.width*892/1125, app.height*655/825),
                            "Dorm", 2, app.DON, [((0, 0), (24, 0))])

    app.CUT = Building("The Cut", "The Cut", 
                       (app.width*667/1125, app.height*588/825))

    app.TC = Building("Tennis Court", "Tennis Court",
                      (app.width*753/1125, app.height*610/825))
    app.TennisCourt = InnerPlace("Tennis Court", "Tennis Court",
                                 (app.width*753/1125, app.height*610/825),
                                 "Fitness", 1, app.TC, [((0, 0), (24, 0))])

    app.BH = Building("Baker", "Baker Hall", 
                      (app.width*533/1125, app.height*696/825))
    app.BH255A = Classroom("PH100", "PH100", 
                          (app.width*533/1125, app.height*696/825),
                          "Classroom", 2, app.BH, [((0, 0), (24, 0))], 
                          "Global Recitation")
    
    app.PH = Building("Potter", "Potter Hall",
                      (app.width*443/1125, app.height*672/825))
    app.PH100 = Classroom("PH100", "PH100", 
                          (app.width*443/1125, app.height*672/825),
                          "Classroom", 1, app.PH, [((0, 0), (24, 0))], 
                          "Global Lecture")
                            
    app.HL = Building("Hunt", "Hunt Library",
                       (app.width*631/1125, app.height*732/825))
    app.Maggie = DiningPlace("Maggie Murph", "Maggie Murph Café",
                             (app.width*631/1125, app.height*732/825), 
                             "Dining", 1, app.HL, [((8, 0), (22, 0))], 2)                   
    
    app.NSH = Building("Newell-Simon", "Newell-Simon Hall",
                       (app.width*494/1125, app.height*511/825))
    app.iNoodle = DiningPlace("iNoodle", "iNoodle",
                              (app.width*494/1125, app.height*511/825), "Dining",
                              3, app.NSH, [((10, 0), (20, 0))], 2)

    app.WEH = Building("Wean", "Wean Hall",
                       (app.width*478/1125, app.height*580/825))
    app.LaPrima = DiningPlace("La Prima", "La Prima Espresso",
                              (app.width*491/1125, app.height*580/825), "Dining",
                              5, app.WEH, [((8, 0), (18, 0))], 1)
    app.WEH5320 = Classroom("WEH5320", "WEH5320", 
                            (app.width*491/1125, app.height*580/825),  
                            "Classroom", 5, app.WEH, [((0, 0), (24, 0))], 
                            "112 Recitation")

    app.WWG = Building("West Wing", "West Wing",
                       (app.width*832/1125, app.height*570/825))
    app.MindRoom = InnerPlace("Mindfulness Room", "Mindfulness Room",
                              (app.width*832/1125, app.height*570/825), "Social",
                              1, app.WWG, [((8, 0), (22, 0))])
    
    app.RES = Building("Resnik", "Resnik House",
                       (app.width*904/1125, app.height*596/825))
    app.CMUCafe = DiningPlace("CMU Cafe", "CMU Cafe",
                              (app.width*904/1125, app.height*596/825), 
                              "Dining", 1, app.RES, 
                              [((0, 0), (2, 0)), ((8, 0), (24, 0))], 1)
    app.Serve = DiningPlace("Resnik Servery", "Resnik Servery",
                             (app.width*904/1125, app.height*596/825),
                            "Dining", 1, app.RES,
                            [((10, 30), (14, 0)), ((17, 0), (22, 0))], 2)
    
    app.MM = Building("Margaret Morrison", "Margaret Morison Carnegie Hall",
                      (app.width*797/1125, app.height*646/825))
    
    app.GS = Building("Gesling Stadium", "Gesling Stadium",
                      (app.width*887/1125, app.height*530/825))
    app.Stadium = InnerPlace("Gesling Stadium", "Gesling Stadium",
                             (app.width*887/1125, app.height*530/825), "Fitness",
                             1, app.GS, [((0, 0), (24, 0))])
    
    app.SF = Building("Soccer Field", "Intramural Soccer Field",
                      (app.width*1004/1125, app.height*579/825))
    app.SField = InnerPlace("Soccer Field", "Intramural Soccer Field",
                            (app.width*1004/1125, app.height*579/825), "Fitness",
                            1, app.SF, [((0, 0), (24, 0))])
    
    app.HIL = Building("The Hill", "The Hill",
                       (app.width*1000/1125, app.height*674/825))

    app.GYM = Building("Skibo Gymnasium", "Skibo Gymnasium",
                       (app.width*813/1125, app.height*736/825))
    app.ActRoomSki = InnerPlace("Activity Room", "Activity Room",
                                (app.width*813/1125, app.height*736/825), "Fitness",
                                2, app.GYM, [((8, 0), (24, 0))])

    app.POS = Building("Posner", "Posner Hall",
                       (app.width*752/1125, app.height*712/825))
    app.Exchange = DiningPlace("The Exchange", "The Exchange",
                               (app.width*752/1125, app.height*712/825), "Dining",
                               1, app.POS, [((10, 0), (14, 0)), ((16, 0), (20, 0))], 2)
    
    app.CFA = Building("CFA", "College of Fine Arts",
                       (app.width*692/1125, app.height*689/825))
    
    app.FE = Building("The Fence", "The Fence",
                      (app.width*652/1125, app.height*634/825))
    app.Fence = InnerPlace("The Fence", "The Fence",
                           (app.width*652/1125, app.height*634/825), 
                           "Social", 1, app.FE, [((0, 0), (24, 0))])
    
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
    app.RourCom = DiningPlace("Rour Commons", "Rour Commons",
                              (app.width*533/1125, app.height*321/825), "Dining",
                              1, app.TEP, [((10, 0), (14, 0)), ((16, 0), (20, 0))], 2)

    app.MOR = Building("Morewood", "Morewood Gardens",
                       (app.width*674/1125, app.height*319/825))
    app.UG = DiningPlace("The Underground", "The Underground",
                         (app.width*674/1125, app.height*319/825), "Dining",
                         0, app.MOR, [((0, 0), (2, 0)), ((8, 0), (24, 0))], 1)

    app.MUD = Building("Mudge", "Mudge House",
                       (app.width*699/1125, app.height*168/825))

    app.STE = Building("Stever", "Stever House",
                       (app.width*710/1125, app.height*228/825))

    app.ROF = Building("Rez", "Residence on the Fifth",
                       (app.width*409/1125, app.height*172/825))

  def createEvents(app):
    app.createCourses()

    HW112WED = Event("112 Homework", (1, 15), (20, 0), (22, 0), "Homework")
    app.addEvent(HW112WED)
    HW101MON = Event("Interp Homework", (1, 13), (20, 0), (21, 30), "Homework")
    app.addEvent(HW101MON)
    DinMon = Event("Dinner", (1, 13), (18, 0), (18, 30), "Dining")
    app.addEvent(DinMon)
    DinTue = Event("Dinner", (1, 14), (18, 0), (18, 30), "Dining")
    app.addEvent(DinTue)
    DinWed = Event("Dinner", (1, 15), (18, 0), (18, 30), "Dining")
    app.addEvent(DinWed)

  def createCourses(app):
    # 112:
    app.Lec112Tue = repeatingEvent("112 Lecture", (1, 14), (4, 28), 7,
                                   (10, 30), (11, 50), "Class", app.DH2210)
    app.Lec112Thu = repeatingEvent("112 Lecture", (1, 16), (4, 30), 7,
                                   (10, 30), (11, 50), "Class", app.DH2210)
    app.Rec112Wed = repeatingEvent("112 Recitation", (1, 15), (4, 1), 7,
                                   (15, 30), (16, 20), "Class", app.WEH5320)
    app.Lab112Fri = repeatingEvent("112 Lab", (1, 17), (3, 27), 7,
                                   (15, 30), (16, 20), "Class", app.CLR)
    app.addRepeatingEvent(app.Lec112Tue)
    app.addRepeatingEvent(app.Rec112Wed)
    app.addRepeatingEvent(app.Lec112Thu)
    app.addRepeatingEvent(app.Lab112Fri)
    app.one12 = Course("15112", "Fundamentals of Programming and Computer Science", 
                       [(2, 20), (3, 2)], "Exam", 
                       {app.Lec112Tue, app.Lec112Thu, app.Rec112Wed, app.Lab112Fri})    
    # FYW:
    app.LecGloMon = repeatingEvent("Global Lecture", (1, 13), (4, 27), 7,
                                   (12, 30), (13, 20), "Class", app.PH100)
    app.LecGloWed = repeatingEvent("Global Lecture", (1, 15), (4, 29), 7,
                                   (12, 30), (13, 20), "Class", app.PH100)
    app.RecGloFri = repeatingEvent("Global Recitation", (1, 17), (5, 1), 7,
                                   (12, 30), (13, 20), "Class", app.BH255A)
    app.addRepeatingEvent(app.LecGloMon)
    app.addRepeatingEvent(app.LecGloWed)
    app.addRepeatingEvent(app.RecGloFri)
    app.glob = Course("79104", "Global History",
                      [], "Paper",
                      {app.LecGloMon, app.LecGloWed, app.RecGloFri})
    # whole course list:
    app.courses = [app.one12, app.glob]

  def addRepeatingEvent(app, event):
    currEvent = Event(event.name, event.startDate, event.startTime, 
                      event.endTime, event.function, event.location)
    while (currEvent.date <= event.endDate):
      app.addEvent(currEvent)
      nextDate = app.wrapAroundMonth(currEvent.date[0], currEvent.date[1] + event.cycle)
      currEvent = Event(event.name, nextDate, event.startTime, 
                        event.endTime, event.function, event.location)

  def addEvent(app, event):
    if event.date in app.events:
      eventList = app.events[event.date]
      if event not in eventList:
        index = len(eventList)
        for i in range(len(eventList)):
          if (event.startTime < eventList[i].startTime):
            index = i
            break
          elif (event.startTime == eventList[i].startTime):
            if (event.endTime <= eventList[i].endTime): index = i
            else: index = i+1
            break
        app.events[event.date].insert(index, event)
    else: app.events[event.date] = [event]

  def isClassTime(app, time, classroom):
    for course in app.courses:
      for clas in course.classes:
        if (clas.location == classroom) and (clas.startTime <= time <= clas.endTime):
          return True
    return False

  def stopActivity(app):
    app.hero.inActivity = False
    app.hero.sleeping = False
    app.hero.studying = False
    app.hero.eating = False
    app.hero.inClass = False
    app.hero.exercising = False
    app.hero.socializing = False

  def drawActivityWindow(app, activity, stats, canvas):
    # draw the window:
    (borderX, borderY) = (app.windowBorderX, app.windowBorderY)
    canvas.create_rectangle(borderX, borderY, app.width-borderX, app.height-borderY,
                            fill = "white", width = 0)
    # will be replaced by import corresponding icon:
    canvas.create_text(app.width/2, app.height/2, text = f"{activity}...",
                       font = "Arial 32 bold")
    # draw empty status bar:
    (barLength, barWidth) = (app.statusBarLength, app.statusBarWidth)
    canvas.create_rectangle(app.width/2 - barLength/2, app.height/4,
                            app.width/2 + barLength/2, app.height/4 + barWidth)
    # fill status bar:
    filledBarLength = barLength * (stats/100)
    canvas.create_rectangle(app.width/2 - barLength/2, app.height/4,
                            app.width/2 - barLength/2 + filledBarLength, 
                            app.height/4 + barWidth, fill = "cyan")
    # draw exit button:
    (butLength, butWidth) = (app.buttonLength, app.buttonWidth)
    canvas.create_rectangle(app.width/2 - butLength/2, app.height*(3/4) - butWidth,
                            app.width/2 + butLength/2, app.height*(3/4),
                            fill = "cyan")
    canvas.create_text(app.width/2, app.height*(3/4) - butWidth/2,
                       text = "Finish", font = "Arial 20 bold")

  def mousePressedOnExitButton(app, event):
    (butLength, butWidth) = (app.buttonLength, app.buttonWidth)
    return ((app.width/2 - butLength/2 < event.x < app.width/2 + butLength/2) and
            (app.height*(3/4) - butWidth < event.y < app.height*(3/4)))

MyModalApp(width=1125, height=825)
