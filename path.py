import random
import pedestrian
import config


class Path:
    def __init__(self, number=1, length=20, spawnProbability=config.pedestrian_spawn_prob,
                 speedLimit=3, ticksPerSecond=config.tps):
        self.number = number
        self.length = length
        self.pedestrians = []
        self.spawnProbability = spawnProbability
        self.speedLimit = speedLimit
        self.ticksPerSecond = ticksPerSecond
        self.vMax = 2
        self.numberOfPedestrians = 0
        self.red_lit = False

    def addPedestrian(self, length=1, width=1, vChange=0.1, velocity=0.05, travelled=0):

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
                self.numberOfPedestrians += 1

    def movePedestrians(self):
        for pedestrian in self.pedestrians:
            pedestrian.accelerate()
        for index in range(1, len(self.pedestrians)):
            curr = self.pedestrians[index - 1]
            next = self.pedestrians[index]
            curr.keepSafeVelocity(next)

        for pedestrian in self.pedestrians:
            pedestrian.randomize()
        for pedestrian in self.pedestrians:
            pedestrian.move()

    def update(self):
        if self.red_lit is not True:
            self.movePedestrians()

            self.removePedestrians()
            if random.random() < self.spawnProbability:
                self.addPedestrian()
