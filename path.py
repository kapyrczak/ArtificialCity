import random
import pedestrian

class Path:
    def __init__(self, number = 1, length = 20, pedestrians = [], increaseProbability = 0.2,
        speedLimit = 2, ticksPerSecond=30):
        self.number = number
        self.length = length
        self.pedestrians = pedestrians
        self.increaseProbability = increaseProbability
        self.speedLimit = speedLimit
        self.ticksPerSecond = ticksPerSecond
        self.vMax = 2
        self.startingVelocity = speedLimit


    def newPedestrian(self, length = 1, width = 1, vChange = 0.1, velocity = 0, travelled = 0):

        newPedestrian = pedestrian.Pedestrian(length, width,  self.speedLimit/self.ticksPerSecond,
                                               vChange/self.ticksPerSecond, velocity, travelled)

        self.pedestrians.insert(0, newPedestrian)

    def addPedestrian(self):
        if random.random() < self.increaseProbability:
            self.newPedestrian()

    def removePedestrians(self):
        end = len(self.pedestrians)
        index = 0
        while index < end:
            if self.pedestrians[index].travelled > self.length:
                self.pedestrians.pop(index)
                index = index - 1
            index = index + 1

    def movePedestrians(self):
       for pedestrian in self.pedestrians:
           pedestrian.accelerate()
       for pedestrian in self.pedestrians:
           pedestrian.randomize()
       for pedestrian in self.pedestrians:
           pedestrian.move()


    def update(self):
        self.movePedestrians()
        #self.removePedestrians()
        self.addPedestrian()









