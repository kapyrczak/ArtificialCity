import random
import pedestrian
import config

class Path:
    def __init__(self, number, length =24, pedestrians = [], spawnProbability = config.pedestrian_spawn_prob,
        speedLimit = 2, ticksPerSecond=config.pps):
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
        index = 0
        while index < len(self.pedestrians):
            if self.number == 1 or self.number == 2:
                if self.pedestrians[index].travelled + 6 > self.length:
                    self.pedestrians.pop(index)
                    index -= 1
                    self.numberOfPedestrians += 1
                index += 1

            elif self.pedestrians[index].travelled > self.length: #+ self.pedestrians[index].length:
                self.pedestrians.pop(index)
                index -= 1
                self.numberOfPedestrians += 1
            index += 1





    def find_index(self, distance):

        index = 0
        while index < len(self.pedestrians) and self.pedestrians[index].travelled < distance:
            index += 1
        return index


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
        self.pedestrians.sort(key=lambda pedestrian: pedestrian.travelled)


        v_m = 0
        for pedestrian in self.pedestrians:
            self.vMax = max(v_m, pedestrian.velocity)












