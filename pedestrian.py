import random

class Pedestrian:
    """
    average speed of a pedestrian -> 6 km/h ~= 1,7 m/s
    let's round it to 2 m/s

    """
    slowDownProbability = 0.2
    def __init__(self, length = 1, width = 1, vMax = 200, vChange = 0.01, velocity = 0,
                  travelled = 0, safeDistance=1):
        self.length = length
        self.width = width
        self.vMax = vMax
        self.velocity = velocity
        self.vChange = vChange
        self.travelled = travelled
        self.safeDistance = safeDistance


    def accelerate(self):
        if self.velocity < self.vMax:
            self.velocity += self.vChange
        if self.velocity > self.vMax:
            self.velocity = self.vMax

    def distance(self, prevPedestrian):
        return prevPedestrian.travelled - self.travelled


    def keepSafeVelocity(self, prevPedestrian):
        dist = self.distance(prevPedestrian)

        if dist < self.safeDistance + self.velocity:
            self.velocity = dist


    def slowDown(self):
        temp = self.velocity - self.vChange
        if temp < 0:
            self.velocity = 0
        else:
            self.velocity = temp


    def randomize(self):
        if random.random() <= self.slowDownProbability:
            self.slowDown()



    def move(self):
        self.travelled += self.velocity


