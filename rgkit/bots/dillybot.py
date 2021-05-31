from rgkit import rg

# Current issue: Robots sometimes attempt to move to an invalid location. 

class Robot:
    def act(self, game):
        # if we're in the center, stay put.
        if self.location == rg.CENTER_POINT:
            return ['guard']
        

        # find nearest enemy
        nearest_enemy = (18, 18)
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.wdist(loc, self.location) <= rg.wdist(nearest_enemy, self.location):
                    nearest_enemy = loc
        
        # if our robot is surrounded and health is low, suicide. Otherwise, attack.
        adjacent_enemies = []
        low_health = 11
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    adjacent_enemies.append(loc)
                    if len(adjacent_enemies) > 2:
                        if bot.hp <= low_health:
                            return ['suicide']
                        return ['attack', loc]
                    else:
                        return ['move', rg.toward(self.location, nearest_enemy)]

        # if there are enemies around, determine whether to attack or suicide.
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    # if robot health is low but it isn't surrounded, move to the center.
                    if bot.hp <= low_health:
                        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
                    else:
                        return ['attack', loc]
                

        # move toward the nearest enemy
        return ['move', rg.toward(self.location, nearest_enemy)]
