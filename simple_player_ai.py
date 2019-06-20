import keras
from keras.models import Sequential
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.models import load_model

import numpy as np 

from copy import deepcopy
from random import randint
from random import random
from random import shuffle

from numpy.random import choice as rchoice

from constants import * 

class SimpPlayerAI(object):
	def __init__(self, player):
		self.player = player 
		self.game = self.player.game
		self.n_epochs = 5
		self.dice_ai = None
		self.reroll_ai = None
		self.steal_ai = None
		self.swap_ai = None
		self.buy_ai = None

	def initialize_ai(self):
		self.construct_input()
		self.input_dim = len(self.current_input)

		self.construct_dice_ai()
		self.construct_buy_ai()
		self.construct_swap_ai()
		self.construct_steal_ai()
		self.construct_reroll_ai()

	def load_h5(self):
		self.dice_ai = load_model('_dice_ai.h5')
		self.reroll_ai = load_model('_reroll_ai.h5')
		self.steal_ai = load_model('_steal_ai.h5')
		self.swap_ai = load_model('_swap_ai.h5')
		self.buy_ai = load_model('_buy_ai.h5')

	def merge_input(self, extra_input):
		self.construct_input()
		extra_input_height = extra_input.shape[0]
		return np.column_stack((np.repeat([self.current_input], extra_input_height, 0), extra_input))

	def merge_right(self, original_input, right_input):
		input_height = original_input.shape[0]
		return np.column_stack((original_input, np.repeat([right_input], input_height, 0)))

	def record_dice(self):
		pass

	def record_reroll(self):
		pass

	def record_buy(self):
		pass

	def record_swap(self):
		pass

	def record_steal(self):
		pass

	def eval_dice(self):
		#0 = double, 1 = single
		extra_input = np.identity(1)
		extra_input = np.concatenate((extra_input, np.zeros( (1,1) )))
		input = self.merge_input(extra_input)
		preds = self.dice_ai.predict(input)
		return preds[:,1]

	def eval_buy(self):
		#0-18 = buy, 19=no buy
		extra_input = np.identity(19)
		extra_input = np.concatenate((extra_input, np.zeros( (1,19) ), ))
		input = self.merge_input(extra_input)
		preds = self.buy_ai.predict(input)
		return preds[:,1]

	def eval_swap(self):
		#self_building_id + 12*opponent_building_id + 144*opponent_offset
		extra_input = np.identity(12*36)
		input = self.merge_input(extra_input)
		preds = self.swap_ai.predict(input)
		return preds[:,1]

	def eval_steal(self):
		# index = steal_offset - 1
		extra_input = np.identity(3)
		input = self.merge_input(extra_input)
		preds = self.steal_ai.predict(input)
		return preds[:,1]

	def eval_reroll(self):
		#0 = reroll, 1 = no reroll
		extra_input = np.identity(1)
		extra_input = np.concatenate((extra_input, np.zeros( (1,1) )) )
		#this considers the value of the dice roll and the number of dice rolled
		right_input = [1*(self.player.roll==2)] + [0] * 12
		right_input[self.player.roll_value] = 1
		input = self.merge_right(self.merge_input(extra_input), right_input)
		preds = self.reroll_ai.predict(input)
		return preds[:,1]

	def construct_dice_ai(self):
		"""
		there is only one extra input: whether to roll one or two dice
		"""
		additional_inputs = 1
		self.dice_ai = self.generic_ai(additional_inputs)

	def construct_buy_ai(self):
		"""
		there are 19 buildings to buy from, all zeros = no buy
		"""
		additional_inputs = 19
		self.buy_ai = self.generic_ai(additional_inputs)

	def construct_swap_ai(self):
		"""
		there are 12 swappable building types

		so extra inputs = 12 * (12 + 12 + 12)
		index = index_opponent_swap + 12*index_self_swap + 144*index_opponenent
		"""
		additional_inputs = 12*36
		self.swap_ai = self.generic_ai(additional_inputs)

	def construct_steal_ai(self):
		"""there are 3 targets, so 3 extra inputs"""
		additional_inputs = 3
		self.steal_ai = self.generic_ai(additional_inputs)

	def construct_reroll_ai(self):
		"""
		relevant input 0 - 1 (0) or 2(1) dice
		relevant input 1-12 - value of first dice roll 
		then one input to decide to reroll or not
		"""
		additional_inputs = 1 + 1 + 12
		self.reroll_ai = self.generic_ai(additional_inputs)

	def generic_ai(self, additional_inputs):
		ai = Sequential()
		ai.add(Dense(512, input_shape = (self.input_dim + additional_inputs,) ) )
		ai.add(Dropout(0.1))
		ai.add(Activation('relu'))
		ai.add(Dense(256))
		ai.add(Dropout(0.05))
		ai.add(Activation('relu'))
		ai.add(Dense(128))
		ai.add(Dropout(0.05))
		ai.add(Activation('relu'))
		ai.add(Dense(2))
		ai.add(Activation('softmax'))
		opt = keras.optimizers.SGD(nesterov=True,momentum=0.1)
		ai.compile(loss='categorical_crossentropy',
				  optimizer=opt,
				  metrics=['accuracy'])
		return ai 

	def construct_input(self):
		#construct input for each player state 
		self.current_input = self.player.complete_serialize()
