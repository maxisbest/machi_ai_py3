"""
this file contains a random_player class
constants: starting_buildings, building_cost, supply_buildings, player_limit, BUILDING_ORDER, BUILDING_INDEX, SWAPPABLE_BUILDING_ORDER, SWAPPABLE_BUILDING_INDEX
"""

from constants import starting_buildings, building_cost, player_limit, \
    BUILDING_ORDER, SWAPPABLE_BUILDING_ORDER, BUILDING_VECTOR_TEMPLATE
import numpy as np
from copy import deepcopy
from random import randint
from random import choice
from functools import reduce
from player import Player
from player_ai import PlayerAI  #need this class to record data.

class RndPlayer(Player):
    def __init__(self, game, order=3, coins=3, name='rp'):
        Player.__init__(self, game, order, name)
        #self.AI = None
        #self.shared_ai = False
        self.coins = coins

    def roll_dice(self):
        ''' get the vale of dice(s), self.roll_value '''
        dice = [randint(1, 6) for _ in range(self.roll)]
        if self.roll == 2 and dice[0] == dice[1]:
            self.double = True
        else:
            # for rerolls
            self.double = False
        self.roll_value = sum(dice)
        if self.game.record_game:
            msg = f'roll dice: p{self.order} rolled {self.roll_value} with {self.dice} dice\n'
            self.game.game_record_file.write(msg)
            print(msg, end='')

           self.AI.shared.dice_history = []
            self.AI.shared.dice_history_turn = []
            self.AI.shared.buy_history = []
            self.AI.shared.buy_history_turn = []
            self.AI.shared.steal_history = []
            self.AI.shared.steal_history_turn = []
            self.AI.shared.swap_history = []
            self.AI.shared.swap_history_turn = []
            self.AI.shared.reroll_history = []
            self.AI.shared.reroll_history_turn = []
            self.AI.shared.dice_history_win = []
            self.AI.shared.buy_history_win = []
            self.AI.shared.steal_history_win = []
            self.AI.shared.swap_history_win = []
            self.AI.shared.reroll_history_win = []

    def decide_dice(self):
        '''randomly decides using 1 dice, or 2 dices. self.roll=1 or 2 '''
        if self.buildings['station'] == 0:
            self.roll = 1
            return 0
        self.roll = choice([1, 2])  # from random import choice
        return 0

    def decide_reroll(self):
        '''if self.reroll==0, then no rerolling; if self.reroll==1, game will go to roll_dice() again. '''
        if self.buildings['radio_tower'] == 0:
            self.reroll = 0
            return 0

        self.reroll = choice([0, 1])

        if self.reroll == 1 and self.game.record_game:
            msg = f"reroll: p{self.order} is rerolling.\n"
            self.game.game_record_file.write(msg)
            print(msg, end='')
        return 0

    def decide_steal(self):
        """
        decide from whom to steal. offset can be 1, 2, or 3.
        随机决定对哪个玩家下手。
        """
        self.victim = self.get_next_player(offset=choice([1, 2, 3]))

    def decide_swap(self):
        self.create_swap_mask()  # get a mask.
        ax0, ax1, ax2 = np.nonzero(self.swap_mask) # (ax0[i], ax1[i], ax2[i]) is a nonzero and valid choice.
        ychoice = randint(0, len(ax0)-1) # get an valid index. my family name is YI, so i use ychoice instead of choice to avoid keywords duplication. :)
        self.swap_self_building = ax0[ychoice]
        self.swap_opponent_offset=ax1[ychoice]+1 #you will only get 0/1/2, so you need +1.
        self.swap_opponent_building=ax2[ychoice]

    def create_swap_mask(self):
        mask = np.zeros((12, 3, 12)) #self has 12 swappable cards, there are 3 opponents, and every oppnent has 12 cards.
        for i in range(12):  #iterate self's cards
            for j in range(3):  #iterate 3 players
                for k in range(12):  #iterate other players' cards
                    if self.buildings[SWAPPABLE_BUILDING_ORDER[i]]!=0 and \
                            self.get_next_player(offset=(j+1)).buildings[
                                SWAPPABLE_BUILDING_ORDER[k]]!=0:
                        mask[i, j, k]=1
        self.swap_mask = mask

    def decide_buy(self):
        self.create_buy_mask()
        ylist = self.buy_mask #取出buy_mask--是个list变量
        ylist_np = np.array(ylist) #转换为np.array()类型
        yvalid = np.nonzero(ylist_np) #得到一个元组, 放的是有效值的下标
        ychoice = np.random.choice(yvalid[0].tolist()) #随机选择一个下标, 这个下标对应的是可以买的牌
        self.buy_choice = ychoice #

        """this returns the complete and sufficient game state based on the player whose turn it is"""
        return reduce(list.__add__, [self.get_next_player(offset).serialize_data() for offset in range(4)])


