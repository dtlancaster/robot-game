import rgkit.rg as rg


class Robot:
    def act(self, game):
        adj_enemies = 0                 # 1 square away
        adj_enemy_locs = []             # loc of adj enemies.
        close_enemies = 0               # 2 squares away
        close_enemy_locs = []           # loc of close enemies.
        close_enemy_target_locs = []    # loc of places close enemies could move into which are attackable.

        # calculate number of adj_enemies and close_enemies
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.wdist(loc, self.location) == 1:  # dist or wdist?
                    adj_enemies += 1
                    adj_enemy_locs.append(loc)
                if rg.wdist(loc, self.location) == 2:  # dist or wdist?
                    close_enemies += 1
                    close_enemy_locs.append(loc)
                    for possAtk in rg.locs_around(self.location, filter_out=('invalid', 'obstacle')):
                        for possMove in rg.locs_around(loc, filter_out=('invalid', 'obstacle')):
                            if possMove == possAtk:
                                close_enemy_target_locs.append(possAtk)

        # commits suicide if the unit may die from attacks in the turn anyway
        # else if enemy is nearby is attacks them
        if self.hp <= 9 * adj_enemies:
            return ['suicide']
        elif adj_enemies > 0:
            for loc in adj_enemy_locs:
                return ['attack', loc]
        elif close_enemies > 0:
            for loc in close_enemy_locs:
                toCenter = rg.toward(loc, rg.CENTER_POINT)
                for possMove in close_enemy_target_locs:
                    if possMove == toCenter:
                        return ['attack', possMove]
            for possMove in close_enemy_target_locs:
                return ['attack', possMove]

        '''
        if at center and likely to die this turn commit suicide
        else if enemy near attack
        else guard
        '''
        if self.location == rg.CENTER_POINT:
            if adj_enemies > 0 and self.hp <= 9 * adj_enemies:
                return ['suicide']
            elif adj_enemies > 0:
                for loc in adj_enemy_locs:
                    return ['attack', loc]
            else:
                return ['guard']

        # move to center
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]