from player import Player 
from constants import * 

from copy import deepcopy
from random import randint
from random import random
from random import shuffle

from numpy.random import choice

class Game(object):
	def __init__(self, id, pre_existing_players = None):
		if not pre_existing_players:
			self.players = [Player(self, i) for i in range(4)]
			self.initialize_player_ai()
		else:
			shuffle(pre_existing_players)
			self.players = [player.reset_game(self, i) for i, player in enumerate(pre_existing_players)]

		self.building_supply = deepcopy(supply_buildings)
		self.id = id 
		
		#may be used for weighting
		self.turn = 0

	def run(self):
		print 'Beginning game #%s' % self.id 
		current_player = self.players[0]
		while True:
			self.turn += 1
			current_player.take_turn()
			if current_player.win:
				break 
			elif current_player.extra_turn:
				current_player.extra_turn = False 
			else:
				current_player = self.get_next_player(current_player)
			if self.turn % 200 == 0:
				print 'turn %s' % self.turn
				for player in self.players:
					print player.coins

		print 'Player %d, order %d won in %d turns' % (current_player.id, current_player.order, self.turn) 
		for player in self.players:
			player.update_win_history()
		return self.players 

	def flush_player_history(self):
		for player in self.players:
			player.flush_history()

	def initialize_player_ai(self):
		for player in self.players:
			player.initialize_ai()

	def get_next_player(self, player, offset=1):
		return self.players[(player.order + offset) % 4]

	def activate_red(self, player):
		"""
		this is where players lose money to other players"""
		roll_value = player.roll_value 
		if roll_value not in [3,9,10]:
			return 0
		max_amount = player.coins 
		if max_amount == 0:
			return 0
		if roll_value==3:
			for i in range(1,4):
				target_player = self.get_next_player(player,i)
				biz_cost = target_player.buildings.cafe 
				if target_player.buildings.shopping_mall:
					biz_cost = biz_cost * 2
				final_cost = min(biz_cost, max_amount)
				max_amount -= final_cost
				player.coins = max_amount
				target_player.coins += final_cost
		else:
			for i in range(1,4):
				target_player = self.get_next_player(player,i)
				biz_cost = target_player.buildings.family_restaurant 
				if target_player.buildings.shopping_mall:
					biz_cost = biz_cost * 3
				else:
					biz_cost = biz_cost * 2
				final_cost = min(biz_cost, max_amount)
				max_amount -= final_cost
				player.coins = max_amount
				target_player.coins += final_cost
		return 0

	def activate_blue(self, player):
		"""
		each player can get money here
		"""
		roll_value = player.roll_value 
		if roll_value not in [1,2,5,9,10]:
			return 0 
		for target_player in self.players:
			if roll_value==1:
				target_player.coins += target_player.buildings.wheat_field 
			elif roll_value==2:
				target_player.coins += target_player.buildings.ranch
			elif roll_value==5:
				target_player.coins += target_player.buildings.forest
			elif roll_value==9:
				target_player.coins += target_player.buildings.mine * 5
			else:#10
				target_player.coins += target_player.buildings.apple_orchard * 3

		return 0 

	def train_players(self):
		for player in self.players:
			player.train_ai()

