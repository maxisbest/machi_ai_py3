# tf.__version__ = 1.13.1; np.__version__ = 1.16.3

from game import Game
from player import Player
from player_ai import PlayerAI
from copy import deepcopy
#from rnd_player import RndPlayer
from constants import *

import numpy as np
import sys

#BUILDING ORDER
# BUILDING_ORDER_ = BUILDING_ORDER + ['DO NOT BUY']

#when in training, you need to set 📌 load=False; 📌 use_max_probability=True; 📌 g_shuffle=True
# the following setting is for battle.
kwargs = {'load':True,
          'name':'',
          'verbose':True,
          'use_max_probability':True,
          'shared_ai':True,
          'game_record_filename':'battle_log.log',  #这个值设为''就不会记录战斗过程了, battle_log.log
          'prob_mod':0.0,
          'g_shuffle':False
         }
print(kwargs)

game = Game(0,name='t001',options=kwargs)
players = game.players

print("player1 and player3 has the same AI.dice_ai?")
print(players[1].AI.dice_ai == players[3].AI.dice_ai) #No

players[1].load_ai(True)

#player1_3 = []
for i in range(2,4):
    players[i].AI.dice_ai = players[1].AI.dice_ai
    players[i].AI.reroll_ai = players[1].AI.reroll_ai
    players[i].AI.steal_ai = players[1].AI.steal_ai
    players[i].AI.swap_ai = players[1].AI.swap_ai
    players[i].AI.buy_ai = players[1].AI.buy_ai

print(players[1].AI.dice_ai == players[3].AI.dice_ai) #Yes
print(players[0].AI.dice_ai == players[1].AI.dice_ai) #No

#players[0].AI = PlayerAI(players[0])  #这个操作会改变
players[0].AI.initialize_ai()

print("player0 and player1 has the same AI.buy_ai?")
print(players[0].AI.buy_ai == players[1].AI.buy_ai)
print(players[0].order)

for player in players:
    player.win=0
# i = np.random.randint(1, 10000, 1)[0]
# game = Game(i, name=name, options=kwargs)

game.players=players
game.run()

kwargs = {'load': False,
          'name': '',
          'verbose': False,
          'use_max_probability': True,
          'shared_ai': False,  # 这里要设为False, 否则上面的4个AI又会用同样的神经网络了。不过player在初始化的时候, 这个属性默认是False的。
          'game_record_filename': '',  # 这个值设为''就不会记录战斗过程了, battle_log.log
          'prob_mod': 0.0,
          'g_shuffle': False
          }
print(kwargs)

who_won = []
for i in range(1000):
    game = Game(i, name=str(i), options=kwargs)
    # reset_game
    game.players = players
    for j in range(4):
        players[j].game = game
        players[j].buildings = deepcopy(starting_buildings)
        players[j].coins = 3
        players[j].order = j
        players[j].win = 0

    game.run(silent=True)
    print(f"game{i} finished with {game.turn} turns.", end=' ')

    for k in range(4):
        if players[k].win:
            who_won.append(players[k].order)
            print(f'player{k} won.')

    game.flush_player_history()
