import random
import pedestrian
import config

class Path:
    def __init__(self, number, length, pedestrians = [], spawnProbability = config.pedestrian_spawn_prob,
        speedLimit = 1.5, ticksPerSecond=config.tps):
        self.number = number
        self.length = length
        self.pedestrians = pedestrians
        self.spawnProbability = spawnProbability
        self.speedLimit = speedLimit
        self.ticksPerSecond = ticksPerSecond
        self.vMax = 1.5
        self.startingVelocity = speedLimit
        self.numberOfPedestrians = 0




    def addPedestrian(self, length = 1, width = 1, vChange = 0.1, velocity = 0.05, travelled = -1):


        newPedestrian = pedestrian.Pedestrian(
            length, width,
            self.speedLimit / self.ticksPerSecond,
            vChange / self.ticksPerSecond,
            velocity,
            travelled)

        self.pedestrians.insert(0, newPedestrian)

    def removePedestrians(self):

        for pedestrian in self.pedestrians:
            if pedestrian.travelled > self.length:
                var = self.pedestrians.index(pedestrian)
                self.pedestrians.pop(var)

    def movePedestrians(self):
       for pedestrian in self.pedestrians:
           pedestrian.accelerate()
       for index in range(1, len(self.pedestrians)):
           curr = self.pedestrians[index-1]
           next = self.pedestrians[index]
           curr.keepSafeVelocity(next)

       for pedestrian in self.pedestrians:
           pedestrian.randomize()
       for pedestrian in self.pedestrians:
           pedestrian.move()


    def update(self):
        self.movePedestrians()

        self.removePedestrians()
        if random.random() < self.spawnProbability:
            self.addPedestrian()











