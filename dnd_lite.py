#!/usr/bin/env python

import random
import json
import requests

standard_array = [15, 14, 13, 12, 10, 8]

def roll_dice(qty, num_sides):
    total = 0
    for i in range(qty):
        total += random.randint(1,num_sides)
    return total


def roll_4d6():
    rolls = [random.randint(1,6), random.randint(1,6), random.randint(1,6), random.randint(1,6)]
    print(rolls)
    rolls.sort()
    return (sum(rolls[-3:]))


def pad_ability_score(score):
    if score < 10:
        return " " + str(score)
    else:
        return str(score)


def pad_modifier(modifier):
    if modifier < 0:
        return str(modifier)
    else:
        return "+" + str(modifier)


ability_modifiers = { 1: -5,
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
                      21: 5,
                      22: 6,
                      23: 6,
                      24: 7,
                      25: 7,
                      26: 8,
                      27: 8,
                      28: 9,
                      29: 9,
                      30: 10}


class PlayerCharacter5E(object):
    """D&D 5E Player Character"""

    def __init__(self, race_id, class_id):
        self.char_id = None
        self.char_name = None
        self.char_lvl = 1
        self.char_alignment = None
        self.char_prof_bonus = 2
        self.char_ability_scores = {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
        self.char_race_id = 0
        self.char_race_name = None
        self.char_race_features = []
        self.char_size = None
        self.char_speed = 0
        self.char_darkvision = 0
        self.char_bg_id = 0
        self.char_bg_name = None
        self.char_class_id = 0
        self.char_class_name = None
        self.char_skills = {
                            "Acrobatics": 0,
                            "Animal Handling": 0,
                            "Arcana": 0,
                            "Athletics": 0,
                            "Deception": 0,
                            "History": 0,
                            "Insight": 0,
                            "Intimidation": 0,
                            "Investigation": 0,
                            "Medicine": 0,
                            "Nature": 0,
                            "Perception": 0,
                            "Performance": 0,
                            "Persuasion": 0,
                            "Religion": 0,
                            "Sleight of Hand": 0,
                            "Stealth": 0,
                            "Survival": 0,
                            }
        self.char_skill_profs = []
        self.char_tool_profs = []
        self.char_languages = []
        self.char_weapons = []
        self.char_armor = []
        self.char_equip = []
        self.char_gp = 0.0
    
    def __repr__(self):
        """ define the representation of a character, which will be a dictionary of data points """
        return {'char_id': self.char_id, 
                'char_name': self.char_name, 
                'char_lvl': self.char_lvl,
                'char_alignment': self.char_alignment,
                'char_prof_bonus': self.char_prof_bonus,
                'char_ability_scores': self.char_ability_scores,
                'char_race_id': self.char_race_id,
                'char_race_name': self.char_race_name,
                'char_class_id': self.char_class_id,
                'char_class_name': self.char_class_name, 
                '': self.char_bg_name, 
                '': self.char_ability_scores,
                }
    def print_char(self):
        print('Race: ' + self.char_race_name)
        print('Class: ' + self.char_class_name)

    
    # # EASY STUFF LIKE NAME, ALIGNMENT, ETC.
    
    # def upd_name(self, char_name):
    #     self.char_name = char_name
    
    # def choose_align(self):
    #     ''' allow user to choose alignment '''
    #     alignments = {1: "Lawful Good",
    #                   2: "Neutral Good",
    #                   3: "Chaotic Good",
    #                   4: "Lawful Neutral",
    #                   5: "Neutral",
    #                   6: "Chaotic Neutral",
    #                   7: "Lawful Evil",
    #                   8: "Neutral Evil",
    #                   9: "Chaotic Evil"}
    #     for i in range(1,10):
    #         print(i + " " + alignments[i])
    #     align_id = int(raw_input("Enter the number of the alignment you'd like: "))
    #     self.char_alignment = alignments[align_id]
    

    # # ABILITY SCORES
    
    # def choose_abilities_4d6(self):
    #     abilities = { 1:"STR", 2:"DEX", 3:"CON", 4:"INT", 5:"WIS", 6:"CHA" }
    #     scores = []
    #     for i in range(6):
    #         scores.append(roll_4d6())
    #     scores.sort()
    #     print("here are your scores: " + str(scores))
    #     while len(scores) > 0:
    #         curr_score = scores.pop()
    #         if len(scores) == 5:
    #             print("your highest score is " + str(curr_score))
    #         else:
    #             print("your next highest score is " + str(curr_score))
    #         print(abilities)
    #         response = input("Enter the number of the ability you'd like to assign this score to: ")
    #         #while (abilities.has_key(int(response)) == False):
    #         while (int(response) in abilities) == False:
    #             response = input("Invalid entry. Please try again: ")
    #         self.char_ability_scores[abilities[int(response)]] = curr_score
    #         del abilities[int(response)]
    #         print("")
    #     print("")
    #     #print "Here are your final scores: ", self.char_ability_scores
    
    # def random_abilities_4d6(self):
    #     for ab in self.char_ability_scores.keys():
    #         self.char_ability_scores[ab] = (roll_4d6())
    #     #print "Here are your final scores: ", self.char_ability_scores

    # def create_character(char_class='random', char_race='random'):


