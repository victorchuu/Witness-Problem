from .route import Route


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


    def advance_to_end(self, route, copy_to = None):    
        while(self.next(route, copy_to)) :
            continue


# This method is not use, only that it can be helpful for thebugging
# TODO: Possibly move to a testUtils module and add unit tests
def is_route_valid(route: Route, instance):
    u = route.vertex[0]
    total_time = route.time[0]
    assert route.leaveTime[0] == total_time
    for i in range(len(route.vertex)):
        total_time += instance.graph.directDist(u, route.vertex[i])
        total_time += route.time[i]
        u = route.vertex[i]
        assert route.leaveTime[i] == total_time
    assert total_time == instance.maxTime