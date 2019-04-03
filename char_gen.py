#!/usr/bin/env python

import random
import json
import requests

standard_array = [15, 14, 13, 12, 10, 8]


def pad_score(score):
	if len(str(score)) == 1:
		return ' ' + str(score)
	else:
		return str(score)

def pad_mod(mod):
	if mod >= 0:
		return '+' + str(mod)
	else:
		return str(mod)


def generate_char(class_id=0, race_id=0, verbose=False):
	''' generate a character
		0 means random selection
	'''
	assert class_id in [0, 3, 5, 9, 12], 'invalid pc_class'
	assert race_id in [0, 1, 2, 3, 4]
	if class_id == 0:
		class_id = random.choice([3, 5, 9, 12])

	class_url = 'http://dnd5eapi.co/api/classes/' + str(class_id)
	c = requests.get(class_url)
	assert c.status_code == 200, 'error retrieving class info'
	char_class = c.json()['name']
	hit_die = c.json()['hit_die']
	base_proficiencies = [x['name'] for x in c.json()['proficiencies']]

	
	# ability scores
	abilities = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
	std_array = [15, 14, 13, 12, 10, 8]
	proficiency_bonus = 2


	''' populate ability scores based on class
	'''
	# cleric
	if class_id == 3:
		stat_priority_lists = {
			1: ['WIS','CON','CHA','STR','DEX','INT'],
			2: ['WIS','STR','CHA','CON','DEX','INT'],
			3: ['WIS','CHA','CON','STR','INT','DEX'],
		}
		my_stat_priority = random.randint(1,len(stat_priority_lists))
		my_stat_priority_list = stat_priority_lists[my_stat_priority]
		prime_req = 'WIS'
		saves = ['WIS', 'INT']

	# fighter
	if class_id == 5:
		stat_priority_lists = {
			1: ['STR','CON','DEX','WIS','CHA','INT'],
			2: ['STR','CON','CHA','DEX','WIS','INT'],
			3: ['STR','DEX','CON','WIS','INT','CHA'],
		}
		my_stat_priority = random.randint(1,len(stat_priority_lists))
		my_stat_priority_list = stat_priority_lists[my_stat_priority]
		prime_req = 'STR'
		saves = ['STR', 'CON']

	# rogue
	if class_id == 9:
		stat_priority_lists = {
			1: ['DEX','CON','CHA','INT','WIS','STR'],
			2: ['DEX','INT','CHA','CON','WIS','STR'],
			3: ['DEX','CHA','INT','CON','WIS','STR'],
		}
		my_stat_priority = random.randint(1,len(stat_priority_lists))
		my_stat_priority_list = stat_priority_lists[my_stat_priority]
		prime_req = 'DEX'
		saves = ['DEX', 'CHA']

	# wizard
	if class_id == 12:
		stat_priority_lists = {
			1: ['INT','DEX','CON','WIS','CHA','STR'],
			2: ['INT','CON','CHA','DEX','WIS','STR'],
			3: ['INT','DEX','CON','CHA','WIS','STR'],
		}
		my_stat_priority = random.randint(1,len(stat_priority_lists))
		my_stat_priority_list = stat_priority_lists[my_stat_priority]
		prime_req = 'INT'
		saves = ['INT', 'WIS']
		

	ability_scores = {
		'STR': std_array[my_stat_priority_list.index('STR')],
		'DEX': std_array[my_stat_priority_list.index('DEX')],
		'CON': std_array[my_stat_priority_list.index('CON')],
		'INT': std_array[my_stat_priority_list.index('INT')],
		'WIS': std_array[my_stat_priority_list.index('WIS')],
		'CHA': std_array[my_stat_priority_list.index('CHA')],
	}

	



	# race selection
	''' 1 = Dwarf
		2 = Elf
		3 = Halfling
		4 = Human
	'''
	if race_id == 0:
		if class_id == 3: # cleric
			race_id = random.choice([4, 4, 4, 1, 1, 3, 2])
		if class_id == 5: # fighter
			race_id = random.choice([4, 4, 4, 1, 1, 2, 2, 3])
		if class_id == 9: # rogue
			race_id = random.choice([4, 4, 4, 3, 3, 3, 2, 2, 1])
		if class_id == 12: # wizard
			race_id = random.choice([4, 4, 4, 2, 2, 3, 1])

	race_url = 'http://dnd5eapi.co/api/races/' + str(race_id)
	r = requests.get(race_url)
	assert r.status_code == 200, 'error retrieving race info'
	char_race = r.json()['name']
	#race_traits = r.json()['traits']

	if verbose:
		print('ability_scores before mod: ' + str(ability_scores))

	# ability modifiers
	if race_id == 1:
		ability_scores['CON'] += 2
		ability_scores['CHA'] += -1
	if race_id == 2:
		ability_scores['DEX'] += 2
		ability_scores['CON'] += -1
	if race_id == 3:
		ability_scores['DEX'] += 2
		ability_scores['STR'] += -1
	if race_id == 4:
		ability_scores[prime_req] += 2
		for ability in ability_scores.keys():
			if ability != prime_req:
				ability_scores[ability] += 1 


	modifier_lookup = {
		1: -5,
        2: -4,
        3: -4,
        4: -3,
        5: -3,
        6: -2,
        7: -2,
        8: -1,
        9: -1,
        10: 0,
        11: 0,
        12: 1,
        13: 1,
        14: 2,
        15: 2,
        16: 3,
        17: 3,
        18: 4,
        19: 4,
        20: 5,
	}

	modifiers = {
		'STR': modifier_lookup[ability_scores['STR']],
		'DEX': modifier_lookup[ability_scores['DEX']],
		'CON': modifier_lookup[ability_scores['CON']],
		'INT': modifier_lookup[ability_scores['INT']],
		'WIS': modifier_lookup[ability_scores['WIS']],
		'CHA': modifier_lookup[ability_scores['CHA']],
	}

	saving_throws = {
		'STR': modifier_lookup[ability_scores['STR']],
		'DEX': modifier_lookup[ability_scores['DEX']],
		'CON': modifier_lookup[ability_scores['CON']],
		'INT': modifier_lookup[ability_scores['INT']],
		'WIS': modifier_lookup[ability_scores['WIS']],
		'CHA': modifier_lookup[ability_scores['CHA']],
	}

	# apply class saves
	for ability in abilities:
		if ability in saves:
			saving_throws[ability] += proficiency_bonus



	
	if verbose:
		print('Class: ' + char_class)
		print('Race: ' + char_race)
		print('Hit Die: 1d' + str(hit_die))
		print('ABILITY SCORES')
		print('STR: ' + str(ability_scores['STR']))
		print(ability_scores)
		print(base_proficiencies)
		#print('Traits: ' + str(race_traits))
		print('     score    mod    save')
		for ability in abilities:
			print(f"{ability}:  {pad_score(ability_scores[ability])}      {pad_mod(modifiers[ability])}      {pad_mod(saving_throws[ability])}")
	
	