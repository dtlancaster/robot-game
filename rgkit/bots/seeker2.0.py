from rgkit import rg

pre_attack_count = 0

class Robot:
    def act(self, game):
        global pre_attack_count
        valid_adj = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))

        if self.hp <= 5:
            return['suicide']

        # if there are enemies around, attack them
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    if self.hp < 20:
                        flee = self.best_flee(game)

                        if flee != ():
                            pre_attack_count=0
                            return ['move', flee]

                    return ['attack', loc]

        # If enemy is two distances away, pre attack in that direction. Only do this
        # for certain number of turns and then move closer
        for loc, bot in game.robots.items():
            if (bot.player_id != self.player_id and pre_attack_count <=1) or (bot.player_id != self.player_id and self.hp <= 20):
                if rg.wdist(loc, self.location) == 2:
                    pre_attack_count += 1
                    return ['attack', rg.toward(self.location, loc)]

        # See if we have an ally near
        #If not, move to closer to an ally
        adj_allies = self.ally_near(game)
        for loc, bot in game.robots.items():
            distance = 10

            if bot.player_id == self.player_id and bot.robot_id != self.robot_id:
                if rg.dist(loc, self.location) < distance and not adj_allies:
                    move_to = rg.toward(self.location, loc)

                    if move_to in game.robots:
                        continue

                    if move_to in valid_adj:
                        return ['move', move_to]



        # Move toward nearest enemy with hp less than or equal to mine
        nearest_enemy = self.nearest_enemy(game)
        if nearest_enemy != ():
            move_to = rg.toward(self.location, nearest_enemy)
            if move_to in valid_adj:
                return ['move', move_to]

        if pre_attack_count > 1:
            pre_attack_count = 0

        return['guard']

    # Find nearest enemy with less than or equal health
    def nearest_enemy(self, game):
        smallest_distance = 30
        closest = ()
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                distance = rg.wdist(self.location, loc)

                if (distance < smallest_distance and bot.hp <= self.hp):
                    closest = loc

        return closest

    # Checks adjacent squares, if square is empty, checks adjacent squares of the empty
    # square. If there are no enemies around it, move there
    def best_flee(self, game):
        loc_around1 = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))
        loc_around_updated = []
        loc_around2 = ()

        for loc1 in loc_around1:
            if loc1 in game.robots:
                continue
            loc_around_updated.append(loc1)

        for loc2 in loc_around_updated:
            loc_around2 = rg.locs_around(loc2, filter_out=('invalid', 'obstacle'))
            valid = True
            for loc3 in loc_around2:

                for loc, bot in game.robots.items():
                    if bot.player_id != self.player_id and loc == loc3:
                        valid = False
            if valid:
                return loc2

        return ()



    # Determine if an ally is nearby
    def ally_near(self, game):
        for loc, bot in game.robots.items():
            if bot.player_id == self.player_id and bot.robot_id != self.robot_id:
                dist = rg.wdist(loc, self.location)
                if dist <= 3:
                    return True
        return False

    def valid_move(self, loc):
        locations = rg.loc_types(loc)
        if 'invalid' in locations or 'obstacle' in locations:
            return False
        return True