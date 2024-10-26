from dataclasses import dataclass, field


@dataclass
class Route:
    vertex: list[int] = field(default_factory=list)
    time: list[int] = field(default_factory=list)
    leaveTime: list[int] = field(default_factory=list)


    def startAt(self, vertex: int):
        self.vertex.append(vertex)
        self.time.append(0)
        self.leaveTime.append(0)


    def sleep_for(self, time):
        self.time[-1] += time
        self.leaveTime[-1] += time
        
        
    # TODO: Use standard formatting such as JSON
    def __str__(self):
        return f'Route: {self.vertex}\nTiempos: {self.time}\nLeaveTime: {self.leaveTime}'
    
    def __len__(self):
        return len(self.vertex)
    
    # TODO: Use standard formatting such as JSON
    def writeToFile(self) :
        return ' '.join(map(str, self.vertex)) + '\n' + \
               ' '.join(map(str, self.time)) + '\n' + \
               ' '.join(map(str, self.leaveTime)) + '\n'
    
    # TODO: Use standard formatting such as JSON
    def readFromFile(self, file):
        self.vertex = [int(x) for x in file.readline().split()]
        self.time = [int(x) for x in file.readline().split()]
        self.leaveTime = [int(x) for x in file.readline().split()]






def createStaticRoute(vertex: int, time: int):
    route = Route()
    route.startAt(vertex)
    route.sleep_for(time)
    return route
    