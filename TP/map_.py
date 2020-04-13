# Classes and functions to get the Map mode to work:
  # the Location class
  # graph representing locations and paths
  # functions to find paths and move around

# Now it's just the Location class

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
    return f"'{self.shortName}' at {self.coordinates}"
  
  def __eq__(self, other):
    return (isinstance(other, Location) and 
            (self.shortName == other.shortName) and
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
  currFilters = ["Dining"]

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
class Place(Location):
  def __init__(self, shortName, longName, coordinates, function, floor,
               building, hours):
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
    hour = 12 if (12 <= timeNum < 13) else int(timeNum % 12)
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
class DiningPlace(Place):
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
class Classroom(Place):
  def __init__(self, shortName, longName, coordinates, function, floor,
               building, hours, className):
    super().__init__(shortName, longName, coordinates, function, floor,
                     building, hours)
    self.className = className

class MapMode(Mode):

  def appStarted(mode):
    # from https://www.cmu.edu/assets/pdfs/2020-campus-map.pdf:
    mode.background = mode.loadImage('images\mapPic.png')
    scale = min(mode.width/mode.background.size[0], mode.height/mode.background.size[1])
    mode.background = mode.scaleImage(mode.background, scale)
    
    mode.r = mode.width/100
    mode.iconWidth = mode.width/37.5
    (mode.dormIconX, mode.dormIconY) = (mode.width*4/75, mode.height*4/55)
    (mode.scheIconX, mode.scheIconY) = (mode.width*10/75, mode.height*4/55)
    (mode.filtIconX, mode.filtIconY) = (mode.width*71/75, mode.height*4/55)
    
    mode.target = None
    mode.displayPaths = False
    mode.nodesSelected = [mode.app.hero.location]
    mode.recommendedPath = []
    (mode.recPathX1, mode.recPathX2, mode.recPathY1, mode.recPathY2) = (-1, -1, -1, -1)
    (mode.cusPathX1, mode.cusPathX2, mode.cusPathY1, mode.cusPathY2) = (-1, -1, -1, -1)
    
    mode.path = []
    (mode.heroDx, mode.heroDy) = (0, 0)
    mode.heroMoving = False

  def mousePressed(mode, event):
    print(f"Mouse pressed at ({event.x}, {event.y}).")
    if ((mode.dormIconX-mode.iconWidth < event.x < mode.dormIconX+mode.iconWidth) and
        (mode.dormIconY-mode.iconWidth < event.y < mode.dormIconY+mode.iconWidth) and
        (mode.app.hero.location == mode.app.DON)):
      mode.app.setActiveMode(mode.app.dormMode)
    elif ((mode.scheIconX-mode.iconWidth < event.x < mode.scheIconX+mode.iconWidth) and
          (mode.scheIconY-mode.iconWidth < event.y < mode.scheIconY+mode.iconWidth)):
      mode.app.setActiveMode(mode.app.scheMode)
    elif ((mode.filtIconX-mode.iconWidth < event.x < mode.filtIconX+mode.iconWidth) and
          (mode.filtIconY-mode.iconWidth < event.y < mode.filtIconY+mode.iconWidth)):
      # a small drop-down window occurs for setting filters
      # would work like tiles
      pass
    elif (mode.mousePressedOnBuilding(event)): pass
    elif (mode.mousePressedOnPathIcons(event)):
      mode.recommendedPath = []
      mode.nodesSelected = []
      mode.heroMoving = True
  
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
          print(mode.nodesSelected)
        else:
          mode.target = building
          mode.displayPaths = True
          mode.findRecommendedPath()
        print()
        return True
    return False

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

  def getNearestNode(mode, nodes):
    nearDist = float("inf")
    nearNode = None
    for node in nodes:
      if (nodes[node] < nearDist): 
        nearDist = nodes[node]
        nearNode = node
    return nearNode

  def mousePressedOnPathIcons(mode, event):
    if ((mode.recPathX1 < event.x < mode.recPathX2) and
        (mode.recPathY1 < event.y < mode.recPathY2)):
      mode.path = mode.recommendedPath
      return True
    elif ((mode.cusPathX1 < event.x < mode.cusPathX2) and
          (mode.cusPathY1 < event.y < mode.cusPathY2)):
      if (mode.nodesSelected[-1] == mode.target):
        mode.path = mode.nodesSelected
        return True
      else: 
        mode.nodesSelected = [mode.app.hero.location]
    return False

  def getHeroMovement(mode):
    (node1, node2) = (mode.path[0], mode.path[1])
    x = node2.coordinates[0] - node1.coordinates[0]
    y = node2.coordinates[1] - node1.coordinates[1]
    h = (x**2 + y**2)**0.5
    (mode.heroDx, mode.heroDy) = (mode.app.hero.speed*x/h, mode.app.hero.speed*y/h)
  
  def timerFired(mode):
    if (len(mode.path) > 1):
      mode.getHeroMovement()
      newHeroX = mode.app.hero.coordinates[0] + mode.heroDx
      newHeroY = mode.app.hero.coordinates[1] + mode.heroDy
      mode.app.hero.coordinates = (newHeroX, newHeroY)
      if (almostEqual(mode.app.hero.coordinates[0], mode.path[1].coordinates[0], 0.8) and
          almostEqual(mode.app.hero.coordinates[1], mode.path[1].coordinates[1], 0.8)):
        mode.path.pop(0)
    elif (len(mode.path) == 1): 
      mode.path = []
      mode.heroMoving = False

  def redrawAll(mode, canvas):
    canvas.create_image(mode.width/2, mode.height/2, 
                        image = ImageTk.PhotoImage(mode.background))
    # will be replaced by icon images:
    canvas.create_rectangle(mode.dormIconX-mode.iconWidth, mode.dormIconY-mode.iconWidth,
                            mode.dormIconX+mode.iconWidth, mode.dormIconY+mode.iconWidth, 
                            fill = "pink")
    canvas.create_rectangle(mode.scheIconX-mode.iconWidth, mode.scheIconY-mode.iconWidth,
                            mode.scheIconX+mode.iconWidth, mode.scheIconY+mode.iconWidth, 
                            fill = "cyan")
    canvas.create_rectangle(mode.filtIconX-mode.iconWidth, mode.filtIconY-mode.iconWidth,
                            mode.filtIconX+mode.iconWidth, mode.filtIconY+mode.iconWidth, 
                            fill = "lime")
    if mode.displayPaths: mode.drawPaths(canvas)
    for building in mode.app.graph: mode.drawBuilding(building, canvas)
    mode.drawHero(canvas)
    mode.drawIcons(canvas)

  def drawPaths(mode, canvas):
    if not mode.heroMoving:
      for nodeA in mode.app.graph:
        (x1, y1) = nodeA.coordinates
        for nodeB in mode.app.graph[nodeA]:
          (x2, y2) = nodeB.coordinates
          canvas.create_line(x1, y1, x2, y2, width = 10, fill = "blue")
    # draw recommended path:
    for i in range(len(mode.recommendedPath)-1):
      (x1, y1) = mode.recommendedPath[i].coordinates
      (x2, y2) = mode.recommendedPath[i+1].coordinates
      canvas.create_line(x1, y1, x2, y2, width = 10, fill = "green")
    # draw user-selected path:
    for i in range(len(mode.nodesSelected)-1):
      (x1, y1) = mode.nodesSelected[i].coordinates
      (x2, y2) = mode.nodesSelected[i+1].coordinates
      canvas.create_line(x1, y1, x2, y2, width = 10, fill = "red")
    # draw the ongoing path:
    for i in range(len(mode.path)-1):
      (x1, y1) = mode.path[i].coordinates
      (x2, y2) = mode.path[i+1].coordinates
      canvas.create_line(x1, y1, x2, y2, width = 10, fill = "yellow")

  def drawBuilding(mode, building, canvas):
    (x, y) = building.coordinates
    color = "white"
    for place in building.places:
      if (place.function in Building.currFilters): color = "cyan"
    canvas.create_oval(x-mode.r, y-mode.r, x+mode.r, y+mode.r, fill = color)

  def drawHero(mode, canvas):
    (x, y) = mode.app.hero.coordinates
    canvas.create_oval(x-mode.r, y-mode.r, x+mode.r, y+mode.r, fill = "pink")
  
  def drawIcons(mode, canvas):
    if mode.displayPaths and (not mode.heroMoving):
      # draw path selection icons:
      (x, y) = (mode.app.hero.coordinates)
      (mode.recPathX1, mode.recPathY2) = (x + mode.width//50, y - mode.height//100) 
      (mode.recPathX2, mode.recPathY1) = (mode.recPathX1 + mode.width//10, 
                                          mode.recPathY2 - mode.height//20)
      canvas.create_rectangle(mode.recPathX1, mode.recPathY1, mode.recPathX2, 
                              mode.recPathY2, fill = "white")
      canvas.create_text((mode.recPathX1+mode.recPathX2)/2, 
                         (mode.recPathY1+mode.recPathY2)/2, 
                        text = "Recommended", fill = "green")
      (mode.cusPathX1, mode.cusPathY1) = (x + mode.width//50, y + mode.height//100)
      (mode.cusPathX2, mode.cusPathY2) = (mode.cusPathX1 + mode.width//10, 
                                          mode.cusPathY1 + mode.height//20)
      canvas.create_rectangle(mode.cusPathX1, mode.cusPathY1, mode.cusPathX2, 
                              mode.cusPathY2, fill = "white")
      canvas.create_text((mode.cusPathX1+mode.cusPathX2)/2, 
                         (mode.cusPathY1+mode.cusPathY2)/2, 
                         text = "Custom", fill = "red")

print("Loaded map_.")
