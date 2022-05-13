from random import uniform

WIDTH = 600
HEIGHT = 400
SPACING = 125

class Pipe:

    def __init__(self):
        
        centery = uniform(SPACING, HEIGHT - SPACING)

        self.x = WIDTH
        self.top = centery - SPACING / 2
        self.bottom = HEIGHT - (centery + SPACING / 2)
        self.w = 80
        self.speed = 6

    def hits(self, bird):
        if (bird.y - bird.r) < self.top or (bird.y + bird.r) > (HEIGHT - self.bottom):
            if bird.x > self.x and bird.x < (self.x + self.w):
                return True

        return False

    def update(self):
        self.x -= self.speed

    def passed(self):
        if self.x < -self.w:
            return True
        else:
            return False