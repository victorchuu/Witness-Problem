from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
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
        
        
    def __len__(self):
        return len(self.vertex)
    

    def __gt__(self, other):
        return True 
    
    def assert_correct(self, instance):

        if self.leaveTime[-1] != instance.maxTime:
            print(f"Route {self} is not correct. Leave time: {self.leaveTime[-1]} != {instance.maxTime}")
            assert False

        SUM = 0
        for i in range(len(self.vertex) - 1):
            SUM += self.time[i]
            SUM += instance.graph.directDist(self.vertex[i], self.vertex[i + 1])

        SUM += self.time[-1]

        if SUM != instance.maxTime:
            print(f"Route {self} is not correct. Sum: {SUM} != {instance.maxTime}")
            assert False



def createStaticRoute(vertex: int, time: int):
    route = Route()
    route.startAt(vertex)
    route.sleep_for(time)
    return route
    