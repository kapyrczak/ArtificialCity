import random
import pedestrian
import config


class Path:
    def __init__(self, number, length=24, pedestrians=[], spawnProbability=config.pedestrian_spawn_prob,
                 speedLimit=1.7, ticksPerSecond=config.tps):
        self.number = number
        self.length = length
        self.pedestrians = pedestrians
        self.spawnProbability = spawnProbability
        self.speedLimit = speedLimit
        self.ticksPerSecond = ticksPerSecond
        self.vMax = 1.7
        self.startingVelocity = speedLimit
        self.numberOfPedestrians = 0

    def addPedestrian(self, length=1, width=1, vChange=0.1, velocity=0.05, travelled=0):

        index = self.find_index(travelled)

        if len(self.pedestrians) != 0 and \
                self.pedestrians[index - 1].travelled - self.pedestrians[index - 1].length <= \
                -self.pedestrians[index - 1].length:
            return

        newPedestrian = pedestrian.Pedestrian(
            length, width,
            self.speedLimit / self.ticksPerSecond,
            vChange / self.ticksPerSecond,
            velocity,
            travelled)

        self.pedestrians.insert(index, newPedestrian)

    def removePedestrians(self):
        for pedestrian in self.pedestrians:

            if pedestrian.travelled > self.length:  # + self.pedestrians[index].length:
                print(self.number, self.length)
                print(pedestrian.travelled)
                self.pedestrians.remove(pedestrian)
                self.numberOfPedestrians += 1

    def find_index(self, distance):

        index = 0
        while index < len(self.pedestrians) and self.pedestrians[index].travelled < distance:
            index += 1
        return index

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
        self.movePedestrians()
        self.removePedestrians()
        if random.random() < self.spawnProbability:
            self.addPedestrian()
        self.pedestrians.sort(key=lambda pedestrian: pedestrian.travelled)

        v_m = 0
        for pedestrian in self.pedestrians:
            self.vMax = max(v_m, pedestrian.velocity)
