"""
GAME RULES:

Game is played on a 19x19 grid.
100 turns total. Goal is to end with more bots than opponent.
Cannot walk out of bounds.
Every 10 turns, 5 robots spawn at random spawn points for each player.
Any robot standing on one of the random spawn points will die.
Each robot begins with 50 HP.
Robots may act on its adjacent squares--not diagonally.
No friendly damage.

Code the AI for a single robot that ALL robots will use.

ACTIONS:

MOVE into an adjacent square. 5 HP collision damage to both robots.

ATTACK an adjacent square. Attacked robot will lose 8 to 10 HP.

SUICIDE at the end of the turn, dealing 15 damage to any adjacent robots.

GUARD to stay put, take half damage from attacks and suicides, avoid all collision damage.
"""

# Example starting bot looks for any enemies around and attacks them. Otherwise, it tries to move to the center.

from rgkit import rg


class Robot:
    def act(self, game):
        # if we're in the center, stay put.
        if self.location == rg.CENTER_POINT:
            return ['guard']

        # if there are enemies around, attack them
        for loc, bot in game.robots.items():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        # move toward the center
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
