# Classes and functions to get the Dorm mode to work:
  # the Hero class
  # functions to get the hero do activities

from cmu_112_graphics import *

class Hero(object):
  def __init__(self, intelligence, energy, social, health, mood,
               location, coordinates, refSpeed):
    self.intel = intelligence
    self.energy = energy
    self.social = social

    self.health = health
    self.perfor = 75

    self.location = location
    self.coordinates = coordinates
    self.speed = (self.energy/75) * refSpeed
    self.moving = False
    self.rushCapacity = self.health

    self.inActivity = False
    self.sleepy = 80
    self.sleeping = False
    self.hunger = 50
    self.eating = False
    self.stress = 20
    self.studying = False
    self.inClass = False
    self.socializing = False
    self.exercising = False
  
  def getStatsLabels(self):
    return "intelligence:\nenergy:\nsociability:\n\nhealth:\nperformance:"
  
  def getStatsNums(self):
    return f"""{self.intel}\n{self.energy}\n{self.social}\n
{int(self.health)}\n{int(self.perfor)}"""

class Course(object):
  homework = dict()

  def __init__(self, code, name, midterms, final, classes):
    self.code = code
    self.name = name
    self.achieve = 60
    self.midterms = midterms # list of tuples of months, date, and day
    self.final = final # "exam" or "paper"
    self.classes = classes # set of class meeting Events
  
  def __repr__(self):
    return self.code
  
  def __eq__(self, other):
    return (isinstance(other, Course) and (self.code == other.code))
  
  def __hash__(self):
    return hash(self.code)

class DormMode(Mode):
  def appStarted(mode):
    mode.background = mode.loadImage('images\dormPic.png')
    scale = min(mode.width/mode.background.size[0], mode.height/mode.background.size[1])
    mode.background = mode.scaleImage(mode.background, scale)
    mode.bedLocation = (mode.width*20/75, mode.height*32/55)
    mode.windowLocation = (mode.width*7/75, mode.height*9/55)
    mode.scheLocation = (mode.width*60/75, mode.height*12/55)
    mode.deskLocation = (mode.width*893/1125, mode.height*425/825)
    mode.r = mode.width/50
    mode.courseButtonLength = mode.width/4
    mode.courseButtonWidth = mode.app.buttonWidth
    mode.preStudy = False
    mode.courseStudied = None

  def mousePressed(mode, event):
    if (mode.preStudy):
      if mode.app.mousePressedOnExitButton(event): mode.preStudy = False
      elif mode.mousePressedOnCourseButtons(event):
        course = mode.getCourseSelected(event)
        mode.courseStudied = course
        mode.app.hero.inActivity = True
        mode.app.hero.studying = True
        mode.preStudy = False
    elif (mode.app.hero.sleeping) or (mode.preStudy) or (mode.app.hero.studying):
      if (mode.app.mousePressedOnExitButton(event)): mode.app.stopActivity()
    else:
      if mode.mousePressedOnWindow(event): mode.app.setActiveMode(mode.app.mapMode)
      elif mode.mousePressedOnSchedule(event): mode.app.setActiveMode(mode.app.scheMode)
      elif mode.mousePressedOnBed(event): mode.app.hero.sleeping = True
      elif mode.mousePressedOnDesk(event): mode.preStudy = True
    print(mode.app.hero.sleepy, mode.app.hero.hunger, mode.app.hero.stress)

  def mousePressedOnCourseButtons(mode, event):
    (butLength, butWidth) = (mode.courseButtonLength, mode.courseButtonWidth)
    blockWidth = (len(mode.app.courses) + 1.6)*butWidth
    return ((mode.width/2 - butLength/2 < event.x < mode.width/2 + butLength/2) and
            (mode.height/4 + 1.6*butWidth < event.y < mode.height/4 + blockWidth))

  def getCourseSelected(mode, event):
    butWidth = mode.courseButtonWidth
    blockMargin = (mode.height/4) + (1.6*butWidth)
    index = int((event.y - blockMargin) / butWidth)
    return mode.app.courses[index]

  def mousePressedOnWindow(mode, event):
    return ((mode.windowLocation[0] - mode.r < event.x < mode.windowLocation[0] + mode.r) and
            (mode.windowLocation[1] - mode.r < event.y < mode.windowLocation[1] + mode.r))

  def mousePressedOnSchedule(mode, event):
    return ((mode.scheLocation[0] - mode.r < event.x < mode.scheLocation[0] + mode.r) and
            (mode.scheLocation[1] - mode.r < event.y < mode.scheLocation[1] + mode.r))

  def mousePressedOnBed(mode, event):
    return ((mode.bedLocation[0] - mode.r < event.x < mode.bedLocation[0] + mode.r) and
            (mode.bedLocation[1] - mode.r < event.y < mode.bedLocation[1] + mode.r))
  
  def mousePressedOnDesk(mode, event):
    return ((mode.deskLocation[0] - mode.r < event.x < mode.deskLocation[0] + mode.r) and
            (mode.deskLocation[1] - mode.r < event.y < mode.deskLocation[1] + mode.r))

  def timerFired(mode):
    mode.app.clockTicked()
    mode.app.adjustHeroStats()
    mode.app.adjustCourseAchievement()

  def redrawAll(mode, canvas):
    # draw background:
    canvas.create_image(mode.width/2, mode.height/2, 
                        image = ImageTk.PhotoImage(mode.background))
    mode.drawInteractivePoints(canvas)
    if mode.app.hero.sleeping: 
      mode.app.drawActivityWindow("Sleeping", mode.app.hero.sleepy, canvas)
    elif mode.preStudy:
      mode.drawPreStudyWindow(canvas)
    elif mode.app.hero.studying:
      activity = f"Studying {mode.courseStudied}"
      mode.app.drawActivityWindow(activity, mode.app.hero.stress, canvas)
      mode.drawCourseAchievementBar(canvas)
    mode.app.drawDateAndTime(canvas)

  def drawInteractivePoints(mode, canvas):
    canvas.create_oval(mode.bedLocation[0] - mode.r, mode.bedLocation[1] - mode.r,
                       mode.bedLocation[0] + mode.r, mode.bedLocation[1] + mode.r,
                       fill = "pink")
    canvas.create_oval(mode.windowLocation[0] - mode.r, mode.windowLocation[1] - mode.r,
                       mode.windowLocation[0] + mode.r, mode.windowLocation[1] + mode.r,
                       fill = "pink")
    canvas.create_oval(mode.scheLocation[0] - mode.r, mode.scheLocation[1] - mode.r,
                       mode.scheLocation[0] + mode.r, mode.scheLocation[1] + mode.r,
                       fill = "pink")
    canvas.create_oval(mode.deskLocation[0] - mode.r, mode.deskLocation[1] - mode.r,
                       mode.deskLocation[0] + mode.r, mode.deskLocation[1] + mode.r,
                       fill = "pink")

  def drawPreStudyWindow(mode, canvas):
    # draw the window:
    (borderX, borderY) = (mode.app.windowBorderX, mode.app.windowBorderY)
    canvas.create_rectangle(borderX, borderY, mode.app.width-borderX, mode.app.height-borderY,
                            fill = "white", width = 0)
    # draw the course options:
    for i in range(len(mode.app.courses)): mode.drawCourseButton(i, canvas)
    # draw the prompt:
    (butLength, butWidth) = (mode.app.buttonLength, mode.app.buttonWidth)
    canvas.create_text(mode.app.width/2, mode.app.height/4 + butWidth/2,
                       text = f"What should I study...?",
                       font = "Arial 24 bold")
    # draw exit button:
    canvas.create_rectangle(mode.app.width/2 - butLength/2, mode.app.height*(3/4) - butWidth,
                            mode.app.width/2 + butLength/2, mode.app.height*(3/4),
                            fill = "cyan")
    canvas.create_text(mode.app.width/2, mode.app.height*(3/4) - butWidth/2,
                       text = "Exit", font = "Arial 20 bold")

  def drawCourseButton(mode, i, canvas):
    (butLength, butWidth) = (mode.courseButtonLength, mode.courseButtonWidth)
    distance = (i+1.6)*butWidth
    x1 = mode.width/2 - butLength/2
    x2 = mode.width/2 + butLength/2
    y1 = mode.height/4 + distance
    y2 = mode.height/4 + distance + butWidth
    canvas.create_rectangle(x1, y1, x2, y2, fill = "cyan")
    canvas.create_text(mode.width/2, (y1+y2)/2, text = mode.app.courses[i].code,
                       font = "Arial 18 bold")

  def drawCourseAchievementBar(mode, canvas):
    # draw empty status bar:
    (barLength, barWidth) = (mode.app.statusBarLength, mode.app.statusBarWidth)
    canvas.create_rectangle(mode.app.width/2 - barLength/2, mode.app.height/4 + 2*barWidth,
                            mode.app.width/2 + barLength/2, mode.app.height/4 + 3*barWidth)
    # fill status bar:
    filledBarLength = barLength * (mode.courseStudied.achieve/100)
    canvas.create_rectangle(mode.app.width/2 - barLength/2, 
                            mode.app.height/4 + 2*barWidth,
                            mode.app.width/2 - barLength/2 + filledBarLength, 
                            mode.app.height/4 + 3*barWidth, fill = "cyan")

print("Loaded dorm")
