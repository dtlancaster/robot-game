from rgkit import rg

class Robot:
    def act(self, game):
        if rg.dist(self.location, rg.CENTER_POINT) <= 2:
            return ['suicide']
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]