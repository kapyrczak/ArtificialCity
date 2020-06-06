import random
import pedestrian
import config

class Path:
    def __init__(self, number = 1, length = 20, pedestrians = [], spawnProbability = config.pedestrian_spawn_prob,
        speedLimit = 2, ticksPerSecond=config.tps):
        self.number = number
        self.length = length
        self.pedestrians = pedestrians
        self.spawnProbability = spawnProbability
        self.speedLimit = speedLimit
        self.ticksPerSecond = ticksPerSecond
        self.vMax = 2
        self.startingVelocity = speedLimit
        self.numberOfPedestrians = 0


    def newPedestrian(self, length = 1, width = 1, vChange = 0.1, velocity = 0, travelled = 0):

        newPedestrian = pedestrian.Pedestrian(length, width,  self.speedLimit/self.ticksPerSecond,
                                               vChange/self.ticksPerSecond, velocity, travelled)

        self.pedestrians.insert(0, newPedestrian)

    def addPedestrian(self):
        if random.random() < self.spawnProbability:
            self.newPedestrian()
        self.pedestrians.sort(key=lambda pedestrian: pedestrian.travelled)

    def removePedestrians(self):
        end = len(self.pedestrians)
        index = 0
        while index < end:
            if self.pedestrians[index].travelled > self.length:
                self.pedestrians.pop(index)
                index = index - 1
                self.numberOfPedestrians += 1
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
        self.removePedestrians()
        self.addPedestrian()

        v_m = 0
        for pedestrian in self.pedestrians:
            self.vMax = max(v_m, pedestrian.velocity)









