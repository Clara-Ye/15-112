# Classes and functions to get the Schedule mode to work:
  # the Event class
  # functions to allow the player do scheduling (not yet implemented)

from cmu_112_graphics import *

# slightly adapted from https://www.cs.cmu.edu/~112/notes/notes-data-and-operations.html#FloatingPointApprox
def almostEqual(d1, d2, epsilon = 10**-10):
    return (abs(d2 - d1) < epsilon)

class Event(object):
  def __init__(self, name, date, startTime, endTime, function, location="N/A"):
    self.name = name
    self.date = date
    self.startTime = startTime
    self.endTime = endTime
    self.function = function
    self.location = location
  
  def __repr__(self):
    return f"{self.name} on {self.date} from {self.startTime} to {self.endTime}"

  def __eq__(self, other):
    return (isinstance(other, Event) and 
            (self.name == other.name) and
            (self.date == other.date) and
            (self.startTime == other.startTime) and
            (self.endTime == other.endTime) and
            (self.location == other.location))
  
  def __hash__(self):
    return hash((self.name, self.date, self.startTime, self.endTime, self.location))

class repeatingEvent(Event):
  def __init__(self, name, startDate, endDate, cycle, 
               startTime, endTime, function, location="N/A"):
    super().__init__(name, startDate, startTime, endTime, function, location)
    self.startDate = startDate
    self.endDate = endDate
    self.cycle = cycle # event happens once every [cycle] days

  def __eq__(self, other):
    return (isinstance(other, Event) and 
            (self.name == other.name) and
            (self.startDate == other.startDate) and
            (self.startTime == other.startTime) and
            (self.endTime == other.endTime) and
            (self.location == other.location))
  
  def __hash__(self):
    return hash((self.name, self.startDate, self.startTime, self.endTime, self.location))

class ScheMode(Mode):

  def appStarted(mode):
    mode.background = mode.loadImage('images\schePic.png')
    scale = min(mode.width/mode.background.size[0], mode.height/mode.background.size[1])
    mode.background = mode.scaleImage(mode.background, scale)
    # load icons for going to dorm mode / map mode
    mode.iconWidth = mode.width/37.5
    (mode.dormIconX, mode.dormIconY) = (mode.width*4/75, mode.height*4/55)
    (mode.mapIconX, mode.mapIconY) = (mode.width*10/75, mode.height*4/55)
    mode.displayedStartDate = (mode.app.month, mode.app.date)
    mode.displayedStartTime = mode.app.getTimeTuple(mode.app.getTimeFloat((mode.app.hours, mode.app.mins))-0.5)
    mode.defaultDisplay = True

  def mousePressed(mode, event):
    if ((mode.dormIconX-mode.iconWidth < event.x < mode.dormIconX+mode.iconWidth) and
        (mode.dormIconY-mode.iconWidth < event.y < mode.dormIconY+mode.iconWidth) and
        (mode.app.hero.location == mode.app.DON)):
      mode.app.setActiveMode(mode.app.dormMode)
    elif ((mode.mapIconX-mode.iconWidth < event.x < mode.mapIconX+mode.iconWidth) and
          (mode.mapIconY-mode.iconWidth < event.y < mode.mapIconY+mode.iconWidth)):
      mode.app.setActiveMode(mode.app.mapMode)
    print(mode.app.hero.sleepy, mode.app.hero.hunger, mode.app.hero.stress)
    print(f"Mouse pressed at ({event.x}, {event.y})")

  def timerFired(mode):
    mode.app.clockTicked()
    if mode.defaultDisplay: 
      mode.getDisplayedStartTime()
      mode.displayedStartDate = (mode.app.month, mode.app.date)
    mode.app.adjustHeroStats()

  def getDisplayedStartTime(mode):
    if (mode.app.hours < 19):
      mode.displayedStartTime = mode.app.getTimeTuple(mode.app.getTimeFloat((mode.app.hours, mode.app.mins))-0.5)
    else:
      mode.displayedStartTime = (18, 30)

  def redrawAll(mode, canvas):
    # draw background:
    canvas.create_image(mode.width/2, mode.height/2, 
                        image = ImageTk.PhotoImage(mode.background))
    mode.drawStats(canvas)
    mode.drawEvents(canvas)
    mode.drawTimeBar(canvas)
    mode.drawIcons(canvas)
  
  def drawStats(mode, canvas):
    statsLabels = mode.app.hero.getStatsLabels()
    statsNums = mode.app.hero.getStatsNums()
    canvas.create_text(mode.width/7.9, mode.height/2.3, text = statsLabels,
                       font = "Arial 12 bold")
    canvas.create_text(mode.width/5.3, mode.height/2.29, text = statsNums,
                       font = "Arial 12 bold")

  def drawEvents(mode, canvas):
    mode.getDisplayedEvents(mode.displayedStartDate, mode.displayedStartTime)
    for event in mode.displayedEvents:
      mode.drawEvent(event, canvas)

  def getDisplayedEvents(mode, startDate, startTime):
    mode.displayedEvents = []
    today = startDate
    tomorrow = mode.app.wrapAroundMonth(today[0], today[1]+1)
    dayAfterT = mode.app.wrapAroundMonth(tomorrow[0], tomorrow[1]+1)
    (hours, mins) = startTime
    for day in [today, tomorrow, dayAfterT]:
      if (day[0], day[1]) in mode.app.events:
        for event in mode.app.events[(day[0], day[1])]:
          if ((hours <= 19) and 
              (event.endTime >= (hours, mins)) and
              (event.startTime <= (hours+5.5, mins))):
            mode.displayedEvents.append(event)
          elif (hours > 19) and (event.endTime > (19, 0)):
            mode.displayedEvents.append(event)

  def drawEvent(mode, event, canvas):
    dateDiff = mode.getDateDifference(event.date, mode.displayedStartDate)
    x1 = mode.width/2.95 + (dateDiff)*(mode.width/5.6) + (dateDiff+1)*(mode.width/55)
    x2 = x1 + (mode.width/5.6)
    startTime = mode.app.getTimeFloat(mode.displayedStartTime)
    if (event.startTime >= mode.displayedStartTime):
      y1 = mode.height*(305/825) + (mode.app.getTimeFloat(event.startTime) - startTime)*(mode.width/15)
    else:
      y1 = mode.height*(305/825)
    y2 = mode.height*(305/825) + (mode.app.getTimeFloat(event.endTime) - startTime)*(mode.width/15)
    if (y2 > mode.height*(752/825)): y2 = mode.height*(752/825)
    canvas.create_rectangle(x1, y1, x2, y2, fill = "pink")
    displayedInfo = None
    if (y2 - y1 >= mode.height/30): displayedInfo = event.name
    if (y2 - y1 >= mode.height/10):
      startTime = mode.app.getDisplayedTime(event.startTime)
      endTime = mode.app.getDisplayedTime(event.endTime)
      displayedInfo += f"\n{startTime} - {endTime}"
    if (y2 - y1 >= mode.height/15): displayedInfo += f"\n{event.location}"
    canvas.create_text(x1 + 10, y1 + 10, anchor = "nw", font = "Arial 10 bold",
                       text = displayedInfo)

  def getDateDifference(mode, date1, date2):
    (month1, day1) = date1
    (month2, day2) = date2
    if (month1 == month2): return abs(day1 - day2)
    else: 
      endOfMonth1 = app.monthWrapArounds[month1]
      return (endOfMonth1 - day1) + day2

  def drawTimeBar(mode, canvas):
    time = (mode.app.hours, mode.app.mins)
    hours = mode.app.getTimeFloat(time)
    barY = mode.height*(345/825)
    if (hours > 19): barY += (hours - 19)*(mode.width/15)
    canvas.create_line(mode.width/3.05, barY, mode.width/1.05, barY, 
                       fill = "red", width = 2)
    canvas.create_text(mode.width/3.35, barY, 
                       text = mode.app.getDisplayedTime(time),
                       font = "Arial 12 bold", fill = "red")
    # draw other numbers:
    #for i in range(7):
    #  currNum = int(hours + i) % 24
    #  numX = mode.width/3.32
    #  numY = (mode.height/2.4) + (i - hours%1)*(mode.width/15)
    #  if ((not almostEqual(currNum, hours, 0.2)) and
    #      (barY < numY < (barY + 5.4*(mode.width/15)))):
    #    canvas.create_text(numX, numY, text = str(currNum), font = "Arial 12 bold")

  def drawIcons(mode, canvas):
    # will be replaced by icon images:
    canvas.create_rectangle(mode.dormIconX-mode.iconWidth, mode.dormIconY-mode.iconWidth,
                            mode.dormIconX+mode.iconWidth, mode.dormIconY+mode.iconWidth, 
                            fill = "pink")
    canvas.create_rectangle(mode.mapIconX-mode.iconWidth, mode.mapIconY-mode.iconWidth,
                            mode.mapIconX+mode.iconWidth, mode.mapIconY+mode.iconWidth, 
                            fill = "cyan")
    mode.app.drawDateAndTime(canvas)