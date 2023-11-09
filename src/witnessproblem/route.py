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