
class Route :
    
    def __init__(self):
        self.vertex: [int] = []
        self.time: [int] = []  
        self.leaveTime: [int] = []


    def startAt(self, vertex: int):
        self.vertex.append(vertex)
        self.time.append(0)
        self.leaveTime.append(0)


    def sleep_for(self, time):
        self.time[-1] += time
        self.leaveTime[-1] += time
        
        
    def __str__(self):
        return f'Route: {self.vertex}\nTiempos: {self.time}\nLeaveTime: {self.leaveTime}'
    
    def __len__(self):
        return len(self.vertex)
    
    def is_valid(self, instance):
        graph = instance.graph
        it = RouteIterator(self)
        u = self.vertex[0]
        total_time = self.time[0]
        assert self.leaveTime[0] == total_time
        for i in range(len(self.vertex)):
            total_time += instance.graph.directDist(u, self.vertex[i])
            total_time += self.time[i]
            u = self.vertex[i]
            assert self.leaveTime[i] == total_time
        assert total_time == instance.maxTime

    def writeToFile(self) :
        return ' '.join(map(str, self.vertex)) + '\n' + \
               ' '.join(map(str, self.time)) + '\n' + \
               ' '.join(map(str, self.leaveTime)) + '\n'
    
    def readFromFile(self, file):
        self.vertex = [int(x) for x in file.readline().split()]
        self.time = [int(x) for x in file.readline().split()]
        self.leaveTime = [int(x) for x in file.readline().split()]



def createStaticRoute(vertex: int, time: int):
    route = Route()
    route.startAt(vertex)
    route.sleep_for(time)
    return route
    

class RouteIterator :
    

    def __init__(self, route, copy_to = None, start_at = 0) :
        self.index = start_at
        self.vertex = route.vertex[start_at]
        self.a = start_at
        self.b = route.time[start_at]
        
        if not (copy_to == None) :
            copy_to.vertex.append(self.vertex)
            copy_to.time.append(route.leaveTime[0])
            copy_to.leaveTime.append(route.leaveTime[0])
        
    def isFinished(self, route):
        return self.index+1 < len(route.vertex)

    def next(self, route, copy_to = None) :
        if self.index+1 >= len(route.vertex) :
            if not (copy_to == None) :
                copy_to.time[-1] += route.leaveTime[-1] - copy_to.leaveTime[-1]
                copy_to.leaveTime[-1] = route.leaveTime[-1]
            return False
        self.index += 1
        self.b = route.leaveTime[self.index]
        self.a = self.b - route.time[self.index]
        self.vertex = route.vertex[self.index]
        
        if not (copy_to == None) :
            copy_to.vertex.append(self.vertex)
            copy_to.time.append(route.time[self.index])
            copy_to.leaveTime.append(route.leaveTime[self.index])
        
        return True
    

    def advance(self, route, steps, copy_to = None):
        while(self.index < steps) :
            self.next(route, copy_to)


    def advace_to_end(self, route, copy_to = None):    
        while(self.next(route, copy_to)) :
            continue