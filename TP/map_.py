# Classes and functions to get the Map mode to work:
  # the Location class
  # functions to find paths and move around
  # functions to do activities in different places

from cmu_112_graphics import *

# slightly adapted from https://www.cs.cmu.edu/~112/notes/notes-data-and-operations.html#FloatingPointApprox
def almostEqual(d1, d2, epsilon = 10**-10):
    return (abs(d2 - d1) < epsilon)

class Location(object):
  def __init__(self, shortName, longName, coordinates):
    self.shortName = shortName
    self.longName = longName
    self.coordinates = coordinates # tuple of xy coordinates
  
  def __repr__(self):
    return self.shortName
  
  def __eq__(self, other):
    return (isinstance(other, Location) and 
            (self.longName == other.longName) and
            (self.coordinates == other.coordinates))
  
  def __hash__(self):
    return hash((self.shortName, self.coordinates))

  # gets the distance between two Locations:
  def getDistance(self, other):
    (startX, startY) = (self.coordinates[0], self.coordinates[1])
    (endX, endY) = (other.coordinates[0], other.coordinates[1])
    return ((startX - endX)**2 + (startY - endY)**2)**0.5

# where the player can click on when interacting with map:
class Building(Location):
  locationTypes = ["Dining", "Classroom", "Fitness", "Social", "Dorm"]
  activityTypes = ["Eat", "Attend Class", "Exercise", "Socialize", "Sleep/Study"]

  def __init__(self, shortName, longName, coordinates):
    super().__init__(shortName, longName, coordinates)
    self.places = set() # set of Place objects inside
  # might distinguish indoor/outdoor later

  # returns the name of the building plus info about any places in it:
  def getInfo(self):
    infoStr = f"{str(self.longName)}\n\nPlaces to go:"
    if (self.places == []):
      infoStr += "None"
    else:
      for place in self.places:
        infoStr += "\n\n" + place.getPlaceInfo()
    return infoStr

# locations inside buildings that the player can actually go to:
class InnerPlace(Location):
  def __init__(self, shortName, longName, coordinates, function, floor, building, hours):
    super().__init__(shortName, longName, coordinates)
    self.function = function # classroom, dining, fitness, social, dorm
    self.floor = floor
    self.building = building
    self.building.places.add(self)
    self.hours = hours # list of tuples of start time and end time
  
  # returns the name, function, and hours of a place as a string:
  def getPlaceInfo(self):
    return f"{self.longName}\n{self.function}\n{self.getHourStr()}"

  # returns a string of service time:
  def getHourStr(self):
    hourStr = ""
    for hour in self.hours:
      (startTimeNum, endTimeNum) = (hour[0], hour[1])
      startTimeDis = self.getDisplayTime(startTimeNum)
      endTimeDis = self.getDisplayTime(endTimeNum)
      hourStr += f"{startTimeDis} - {endTimeDis}; "
    return f"{hourStr[:-2]}."
  
  # takes a time as number and returns a time of format hh:mm am/pm:
  def getDisplayTime(self, timeNum):
    hour = app.hours
    period = "am" if (timeNum // 12 == 0) else "pm"
    minute = str(int((timeNum % 1) * 60))
    if (len(minute) == 1): minute = "0" + minute
    return f"{hour}:{minute}{period}"
  
  # returns whether a given time is within the hours of operation:
  def isOpen(self, time):
    for hour in self.hours:
      (startTime, endTime) = (hour[0], hour[1])
      if (startTime <= time <= endTime): return True
    return False

# where the player can eat:
class DiningPlace(InnerPlace):
  peakTimes = [9, 13, 18] # more people around 9am, 1pm and 6pm!

  def __init__(self, shortName, longName, coordinates, function, floor,
               building, hours, serviceType):
    super().__init__(shortName, longName, coordinates, function, floor,
                     building, hours)
    self.serviceType = serviceType # 0: grab-n-go, 1: orders, 2: mixed

  # returns an estimate of waiting time at a given time:
  def getWaitingTime(self, time):
    benchmark = 10 # in minutes
    timeMultiplier = 1
    if (self.serviceType == 1): timeMultiplier *= 2
    elif (self.serviceType == 2): timeMultiplier *= 1.5
    if (self.isPeakTime(time) == True): timeMultiplier *= 2
    benchmark *= timeMultiplier
    return benchmark # will return a random int around benchMark later
  
  # returns whether a given time is a peak time:
  def isPeakTime(self, time):
    for peakTime in DiningPlace.peakTimes:
      if (peakTime-0.5 <= time <= peakTime+0.5): return True
    return False

# where the player attends classes:
class Classroom(InnerPlace):
  def __init__(self, shortName, longName, coordinates, function, floor,
               building, hours, className):
    super().__init__(shortName, longName, coordinates, function, floor,
                     building, hours)
    self.className = className

class MapMode(Mode):

  def appStarted(mode):
    # load background and icons:
    # from https://www.cmu.edu/assets/pdfs/2020-campus-map.pdf:
    mode.background = mode.loadImage('images\mapPic.png')
    scale = min(mode.width/mode.background.size[0], mode.height/mode.background.size[1])
    mode.background = mode.scaleImage(mode.background, scale)
    mode.r = mode.width/100
    mode.iconWidth = mode.width/37.5
    (mode.dormIconX, mode.dormIconY) = (mode.width*4/75, mode.height*4/55)
    (mode.scheIconX, mode.scheIconY) = (mode.width*10/75, mode.height*4/55)
    (mode.filtIconX, mode.filtIconY) = (mode.width*71/75, mode.height*4/55)
    # filter-related:
    mode.displayFilters = False
    mode.currFilters = [ ]
    # path-selection-related:
    mode.target = None
    mode.displayPaths = False
    mode.nodesSelected = [mode.app.hero.location]
    mode.recommendedPath = []
    (mode.recPathX1, mode.recPathX2, mode.recPathY1, mode.recPathY2) = (-1, -1, -1, -1)
    (mode.cusPathX1, mode.cusPathX2, mode.cusPathY1, mode.cusPathY2) = (-1, -1, -1, -1)
    # hero movement related:
    mode.path = []
    (mode.heroDx, mode.heroDy) = (0, 0)
    mode.rushing = False
    mode.exausted = False
    # hero activity related:
    mode.preActivity = False
    mode.activities = [] # tuple of place, function, and displayedText
    mode.activityButtonLength = mode.width/3
    mode.activityButtonWidth = mode.app.buttonWidth
    mode.courseAttended = None

  def mousePressed(mode, event):
    # activity window related:
    if (mode.preActivity):
      if mode.app.mousePressedOnExitButton(event): mode.preActivity = False
      elif mode.mousePressedOnActivityButtons(event):
        if (mode.activities != [(None, None, "nothing")]):
          activity = mode.getActivitySelected(event)
          (place, time) = (activity[0], (mode.app.hours, mode.app.mins))
          if (place != None):
            if (place.function != "Classroom"):
              if (place.isOpen(time)): mode.setActivity(activity)
            elif (mode.app.isClassTime(time, place)): mode.setActivity(activity)
    elif (mode.app.hero.inActivity):
      if (mode.app.mousePressedOnExitButton(event)): mode.app.stopActivity()
    # icon-related:
    elif mode.mousePressedOnDormIcon(event):
      mode.app.setActiveMode(mode.app.dormMode)
    elif mode.mousePressedOnScheIcon(event):
      mode.app.setActiveMode(mode.app.scheMode)
    # filter-related:
    elif mode.mousePressedOnFiltIcon(event): 
      mode.displayFilters = not mode.displayFilters
    elif (mode.displayFilters == True) and (mode.mousePressedOnFilters(event)):
      mode.mousePressedOnFilter(event)
    # path-realted:
    elif (mode.mousePressedOnPathIcons(event)):
      mode.app.hero.moving = True
      mode.app.hero.location = mode.target
      mode.recommendedPath = [mode.app.hero.location]
      mode.nodesSelected = [mode.app.hero.location]
    elif (mode.mousePressedOnBuilding(event)): pass
    print(mode.app.hero.sleepy, mode.app.hero.hunger, mode.app.hero.stress)

  def mousePressedOnDormIcon(mode, event):
    return ((mode.dormIconX-mode.iconWidth < event.x < mode.dormIconX+mode.iconWidth) and
            (mode.dormIconY-mode.iconWidth < event.y < mode.dormIconY+mode.iconWidth) and
            (mode.app.hero.location == mode.app.DON))

  def mousePressedOnScheIcon(mode, event):
    return ((mode.scheIconX-mode.iconWidth < event.x < mode.scheIconX+mode.iconWidth) and
            (mode.scheIconY-mode.iconWidth < event.y < mode.scheIconY+mode.iconWidth))

  def mousePressedOnFiltIcon(mode, event):
    return ((mode.filtIconX-mode.iconWidth < event.x < mode.filtIconX+mode.iconWidth) and
            (mode.filtIconY-mode.iconWidth < event.y < mode.filtIconY+mode.iconWidth))

  def mousePressedOnFilters(mode, event):
    (left, right) = (mode.filtRight - mode.filtWidth, mode.filtRight)
    (top, bottom) = (mode.filtTop, mode.filtTop + mode.filtHeight*len(Building.locationTypes))
    return (left < event.x < right) and (top < event.y < bottom)

  def mousePressedOnFilter(mode, event):
    filtIndex = int((event.y - mode.filtTop) / mode.filtHeight)
    filt = Building.locationTypes[filtIndex]
    if (filt in mode.currFilters): mode.currFilters.remove(filt)
    else: mode.currFilters.append(filt)

  def mousePressedOnBuilding(mode, event):
    for building in mode.app.graph:
      (x, y) = (building.coordinates[0], building.coordinates[1])
      if (x - mode.r < event.x < x + mode.r) and (y - mode.r < event.y < y + mode.r): 
        if mode.displayPaths:
          if ((mode.nodesSelected[-1] in mode.app.graph[building]) and
              (building not in mode.nodesSelected)):
            mode.nodesSelected.append(building)
          elif building in mode.nodesSelected:
            print("Already selected")
          else:
            print("Cannot go there")
        else:
          mode.target = building
          mode.displayPaths = True
          mode.findRecommendedPath()
        return True
    return False

  # finds the shortest path from the current node to a target:
  # algorithm from https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=33e635bd-b3a4-4686-b3a6-ab850003d7c6:
  def findRecommendedPath(mode):
    toVisit = dict()
    visited = dict()
    currNode = mode.app.hero.location
    shortestPaths = {currNode: [currNode]}
    for node in mode.app.graph:
      if (node == currNode): toVisit[node] = 0
      else: toVisit[node] = float("inf")
    while (mode.target in toVisit):
      for neighbor in mode.app.graph[currNode]:
        if (neighbor in toVisit):
          distance = mode.app.graph[currNode][neighbor] + toVisit[currNode]
          if (distance < toVisit[neighbor]):
            toVisit[neighbor] = distance
            shortestPaths[neighbor] = shortestPaths[currNode] + [neighbor]
      visited[currNode] = toVisit[currNode]
      del toVisit[currNode]
      currNode = mode.getNearestNode(toVisit)
    mode.recommendedPath = shortestPaths[mode.target]

  # gets the nearest node of a given node:
  def getNearestNode(mode, nodes):
    nearDist = float("inf")
    nearNode = None
    for node in nodes:
      if (nodes[node] < nearDist): 
        nearDist = nodes[node]
        nearNode = node
    return nearNode

  def mousePressedOnActivityButtons(mode, event):
    (butLength, butWidth) = (mode.activityButtonLength, mode.activityButtonWidth)
    blockWidth = (len(mode.activities) + 1.6)*butWidth
    return ((mode.width/2 - butLength/2 < event.x < mode.width/2 + butLength/2) and
            (mode.height/4 + 1.6*butWidth < event.y < mode.height/4 + blockWidth))

  def getActivitySelected(mode, event):
    butWidth = mode.activityButtonWidth
    blockMargin = (mode.height/4) + (1.6*butWidth)
    index = int((event.y - blockMargin) / butWidth)
    print("Activity selected:", mode.activities[index])
    return mode.activities[index]

  def setActivity(mode, activity):
    (location, locationType, activityName) = (activity[0], activity[1], activity[2])
    i = Building.locationTypes.index(locationType)
    activityType = Building.activityTypes[i]
    if (activityType == "Eat"): mode.app.hero.eating = True
    elif (activityType == "Attend Class"):
      mode.courseAttendedName = location.className
      for course in mode.app.courses:
        for clas in course.classes:
          if (clas.name == mode.courseAttendedName): 
            mode.courseAttended = course
            mode.app.hero.inClass = True
    elif (activityType == "Exercise"): mode.app.hero.exercising = True
    elif (activityType == "Socialize"): mode.app.hero.socializing = True
    elif (activityType == "Sleep/Study"): mode.app.setActiveMode(mode.app.dormMode)
    mode.app.hero.inActivity = True

  def mousePressedOnPathIcons(mode, event):
    if ((mode.recPathX1 < event.x < mode.recPathX2) and
        (mode.recPathY1 < event.y < mode.recPathY2)):
      mode.path = mode.recommendedPath
      mode.activities = []
      return True
    elif ((mode.cusPathX1 < event.x < mode.cusPathX2) and
          (mode.cusPathY1 < event.y < mode.cusPathY2)):
      if (mode.nodesSelected[-1] == mode.target):
        mode.path = mode.nodesSelected
        mode.activities = []
        return True
      else: 
        mode.nodesSelected = [mode.app.hero.location]
    return False
  
  def timerFired(mode):
    mode.app.clockTicked()
    mode.app.adjustHeroStats()
    mode.app.adjustCourseAchievement()
    mode.moveHero()
    mode.adjustRushCapacity()
    
  def moveHero(mode):
    if (len(mode.path) > 1):
      mode.getHeroMovement()
      newHeroX = mode.app.hero.coordinates[0] + mode.heroDx
      newHeroY = mode.app.hero.coordinates[1] + mode.heroDy
      mode.app.hero.coordinates = (newHeroX, newHeroY)
      if (almostEqual(mode.app.hero.coordinates[0], mode.path[1].coordinates[0], 1) and
          almostEqual(mode.app.hero.coordinates[1], mode.path[1].coordinates[1], 1)):
        mode.path.pop(0)
        mode.app.hero.location = mode.path[0]
        print(f"Hero is now at {mode.app.hero.location}.")
    # stops hero movement:
    elif (len(mode.path) == 1): 
      mode.path = []
      mode.displayPaths = False
      mode.app.hero.moving = False
    elif ((len(mode.path) == 0) and (mode.displayPaths == False)):
      if (mode.activities == []): 
        mode.getActivities(mode.app.hero.location)
        mode.preActivity = True

  # gets the current, incremental hero movement:
  def getHeroMovement(mode):
    (node1, node2) = (mode.path[0], mode.path[1])
    x = node2.coordinates[0] - node1.coordinates[0]
    y = node2.coordinates[1] - node1.coordinates[1]
    h = (x**2 + y**2)**0.5
    speed = mode.app.hero.speed*1.5 if mode.rushing else mode.app.hero.speed
    (mode.heroDx, mode.heroDy) = (speed*x/h, speed*y/h)

  def getActivities(mode, building):
    for place in mode.app.hero.location.places:
      i = Building.locationTypes.index(place.function)
      activityName = Building.activityTypes[i]
      activityInfo = f"{activityName} in {place.shortName}"
      mode.activities.append((place, place.function, activityInfo))
    if (mode.activities == []): mode.activities = [(None, None, "Nothing")]

  def adjustRushCapacity(mode):
    if mode.rushing: 
      mode.app.hero.rushCapacity -= 1
      if (mode.app.hero.rushCapacity <= 0): 
        mode.rushing = False
        mode.exausted = True
        print("Exausted!")
    elif (mode.app.hero.rushCapacity < mode.app.hero.health):
      mode.app.hero.rushCapacity += 0.5
      mode.exausted = False

  def keyPressed(mode, event):
    if (event.key == "r"): mode.rushing = not mode.rushing

  def redrawAll(mode, canvas):
    canvas.create_image(mode.width/2, mode.height/2, 
                        image = ImageTk.PhotoImage(mode.background))
    # will be replaced by icon images:
    mode.drawIcons(canvas)
    # draw map:
    if mode.displayFilters: mode.drawFilters(canvas)
    if mode.displayPaths: mode.drawPaths(canvas)
    for building in mode.app.graph: mode.drawBuilding(building, canvas)
    if mode.displayPaths and (not mode.app.hero.moving): mode.drawPathIcons(canvas)
    mode.drawHero(canvas)
    # draw activity-selection window:
    if mode.preActivity: mode.drawPreActivityWindow(canvas)
    # draw activity window:
    if mode.app.hero.eating:
      mode.app.drawActivityWindow("Eating", mode.app.hero.hunger, canvas)
    elif mode.app.hero.socializing:
      mode.app.drawActivityWindow("Socializing", mode.app.hero.stress, canvas)
    elif mode.app.hero.exercising:
      mode.app.drawActivityWindow("Exercising", mode.app.hero.stress, canvas)
    elif mode.app.hero.inClass:
      activity = f"Taking {mode.courseAttendedName}"
      mode.app.drawActivityWindow(activity, mode.courseAttended.achieve, canvas)
    mode.app.drawDateAndTime(canvas)

  def drawIcons(mode, canvas):
    canvas.create_rectangle(mode.dormIconX-mode.iconWidth, mode.dormIconY-mode.iconWidth,
                            mode.dormIconX+mode.iconWidth, mode.dormIconY+mode.iconWidth, 
                            fill = "pink" if (mode.app.hero.location == mode.app.DON) else "gray")
    canvas.create_rectangle(mode.scheIconX-mode.iconWidth, mode.scheIconY-mode.iconWidth,
                            mode.scheIconX+mode.iconWidth, mode.scheIconY+mode.iconWidth, 
                            fill = "cyan")
    canvas.create_rectangle(mode.filtIconX-mode.iconWidth, mode.filtIconY-mode.iconWidth,
                            mode.filtIconX+mode.iconWidth, mode.filtIconY+mode.iconWidth, 
                            fill = "lime")

  def drawFilters(mode, canvas):
    mode.filtRight = mode.filtIconX + mode.iconWidth
    mode.filtTop = mode.filtIconY + mode.iconWidth
    mode.filtWidth = mode.width//9.5
    mode.filtHeight = mode.height//20
    for i in range(len(Building.locationTypes)):
      filt = Building.locationTypes[i]
      color = "cyan" if (filt in mode.currFilters) else "white"
      canvas.create_rectangle(mode.filtRight - mode.filtWidth, mode.filtTop + i*mode.filtHeight,
                              mode.filtRight, mode.filtTop + (i+1)*mode.filtHeight, 
                              fill = color)
      canvas.create_text(mode.filtRight - mode.filtWidth/2, mode.filtTop + (i+1/2)*mode.filtHeight,
                         text = filt, font = "Arial 16 bold")

  def drawPaths(mode, canvas):
    if not mode.app.hero.moving:
      for nodeA in mode.app.graph:
        (x1, y1) = nodeA.coordinates
        for nodeB in mode.app.graph[nodeA]:
          (x2, y2) = nodeB.coordinates
          canvas.create_line(x1, y1, x2, y2, width = 8, fill = "gray")
    # draw recommended path:
    for i in range(len(mode.recommendedPath)-1):
      (x1, y1) = mode.recommendedPath[i].coordinates
      (x2, y2) = mode.recommendedPath[i+1].coordinates
      canvas.create_line(x1, y1, x2, y2, width = 8, fill = "green")
    # draw user-selected path:
    for i in range(len(mode.nodesSelected)-1):
      (x1, y1) = mode.nodesSelected[i].coordinates
      (x2, y2) = mode.nodesSelected[i+1].coordinates
      canvas.create_line(x1, y1, x2, y2, width = 8, fill = "yellow")
    # draw the ongoing path:
    for i in range(len(mode.path)-1):
      (x1, y1) = mode.path[i].coordinates
      (x2, y2) = mode.path[i+1].coordinates
      canvas.create_line(x1, y1, x2, y2, width = 8, fill = "red")

  def drawBuilding(mode, building, canvas):
    (x, y) = building.coordinates
    color = "white"
    for place in building.places:
      if (place.function in mode.currFilters): color = "cyan"
    canvas.create_oval(x-mode.r, y-mode.r, x+mode.r, y+mode.r, fill = color)

  def drawHero(mode, canvas):
    (x, y) = mode.app.hero.coordinates
    canvas.create_oval(x-mode.r, y-mode.r, x+mode.r, y+mode.r, fill = "pink")
  
  def drawPathIcons(mode, canvas):
    (x, y) = (mode.app.hero.coordinates)
    if (mode.target.coordinates[0] <= mode.app.hero.coordinates[0]):
      (mode.recPathX1, mode.cusPathX1) = (x + mode.width // 50, x + mode.width // 50)
      (mode.recPathX2, mode.cusPathX2) = (mode.recPathX1 + mode.width//10, 
                                          mode.cusPathX1 + mode.width//10)
    else:
      (mode.recPathX2, mode.cusPathX2) = (x - mode.width // 50, x - mode.width // 50)
      (mode.recPathX1, mode.cusPathX1) = (mode.recPathX2 - mode.width//10, 
                                          mode.cusPathX2 - mode.width//10)
    # draw recommended icon:
    (mode.recPathY2, mode.recPathY1) = (y - mode.height//100, 
                                        mode.recPathY2 - mode.height//20) 
    canvas.create_rectangle(mode.recPathX1, mode.recPathY1, mode.recPathX2, 
                            mode.recPathY2, fill = "white")
    canvas.create_text((mode.recPathX1+mode.recPathX2)/2, 
                        (mode.recPathY1+mode.recPathY2)/2, 
                      text = "Recommended", fill = "green")
    # draw custom icon:
    (mode.cusPathY1, mode.cusPathY2) = (y + mode.height//100, 
                                        mode.cusPathY1 + mode.height//20)
    canvas.create_rectangle(mode.cusPathX1, mode.cusPathY1, mode.cusPathX2, 
                            mode.cusPathY2, fill = "white")
    canvas.create_text((mode.cusPathX1+mode.cusPathX2)/2, 
                        (mode.cusPathY1+mode.cusPathY2)/2, 
                        text = "Custom", fill = "red")

  def drawPreActivityWindow(mode, canvas):
    # draw the window:
    (borderX, borderY) = (mode.app.windowBorderX, mode.app.windowBorderY)
    canvas.create_rectangle(borderX, borderY, mode.app.width-borderX, mode.app.height-borderY,
                            fill = "white", width = 0)
    # draw the activities:
    for i in range(len(mode.activities)): mode.drawActivityButton(i, canvas)
    # draw the prompt:
    (butLength, butWidth) = (mode.app.buttonLength, mode.app.buttonWidth)
    canvas.create_text(mode.app.width/2, mode.app.height/4 + butWidth/2,
                       text = f"Things to do in {mode.app.hero.location.shortName}:",
                       font = "Arial 24 bold")
    # draw exit button:
    canvas.create_rectangle(mode.app.width/2 - butLength/2, mode.app.height*(3/4) - butWidth,
                            mode.app.width/2 + butLength/2, mode.app.height*(3/4),
                            fill = "cyan")
    canvas.create_text(mode.app.width/2, mode.app.height*(3/4) - butWidth/2,
                       text = "Exit", font = "Arial 20 bold")

  def drawActivityButton(mode, i, canvas):
    (butLength, butWidth) = (mode.activityButtonLength, mode.activityButtonWidth)
    distance = (i+1.6)*butWidth
    x1 = mode.width/2 - butLength/2
    x2 = mode.width/2 + butLength/2
    y1 = mode.height/4 + distance
    y2 = mode.height/4 + distance + butWidth
    time = (mode.app.hours, mode.app.mins)
    activityPlace = mode.activities[i][0]
    color = "gray"
    if (activityPlace != None):
      if (activityPlace.function != "Classroom"):
        if (activityPlace.isOpen(time)): color = "cyan"
      elif (mode.app.isClassTime(time, activityPlace)): color = "cyan"
    canvas.create_rectangle(x1, y1, x2, y2, fill = color)
    canvas.create_text(mode.width/2, (y1+y2)/2, text = mode.activities[i][2],
                       font = "Arial 18 bold")

print("Loaded _map")
