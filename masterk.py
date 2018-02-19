#Copyright 2018 Paul Kutrich. All rights reserved.

import random
import collections
from scoring_rules import scoring_rules

msg = '''
                    Welcome to Ten Thousand
                           The Game!
Objective:
    Score 10,000 points.
    Any turn in which a player ends with more than 10,000 points will be the 
    final turn.
    If multiple players finish with more than 10,000 points, the winner is the
    player with the most points.
    
To score:
    1's and 5's are worth 100 and 50 points respectively.
    Three-of-a-kind is worth the die number x 100. (Three 1's is 1000 points)
    Four-of-a-kind is worth double the same Three-of-a-kind.
    Five-of-a-kind is double Four-of-a-kind.
    Six of any number is worth 5000 points.
    A six dice straight is worth 1500 points.
    Three pairs are also worth 1500 points.
    
To play:
    Your dice will appear in [brackets].
    Choose your dice by the reference number located above your dice.
    You must choose at least one scoring die per throw. If no scoring die are
    thrown your turn is over and your score for the turn will be zero.
    You must score 500 points in one turn to get on the board.
    If you get six keepers in a turn, you may choose to roll all dice again.
    You'll press Enter a lot. Sorry about that. There will be graphics soon.
    Have fun and thanks for helping me develop my first app!!
'''


class Game:
    '''Methods for instantiates players in player_list, game rules, scoring,
    taking turns, choosing a winner, and ending the game.'''
    def __init__(self, player_list):
        self.player_list = self.set_player()

    def set_player(self):
        '''Sets number of players and player names. Adds computer player if 
        desired.'''
        player_list = []
        while True:
            try:
                players = int(input('How many humans are playing?''\n', ))
                break
            except ValueError:
                print('Please enter a number')
        digi_player = input('Do you want to play against Digital Overlord? y/n''\n')
        if r'y' in digi_player.lower():
            player_list.append(ComPlayer('Digital Overlord', 0))
        for x in range(1, players + 1):
            name = input(f'Player {x}, Enter your name:''\n', )
            player_list.append(HumanPlayer(name, 0))
        return player_list

    def is_three_pair(self, choice):
        choice = sorted(choice)
        return len(choice) == 6 and choice[0] == choice[1] and\
            choice[2] == choice[3] and choice[4] == choice[5]

    def is_straight(self, choice):
        return sorted(choice) == list(range(1, 7))

    def keep_score(self, choice):
        '''Scores choices from choose_dice() according to scoring_rules. Ensures
        highest legal score is used.'''
        score = 0
        counts = collections.Counter(choice)
        score = sum(scoring_rules[die - 1][count - 1]
                    for die, count in counts.items())
        if score < 1500:
            if self.is_straight(choice) or self.is_three_pair(choice):
                score = 1500
        if score == 0:
            print('\nSorry, no keepers. That ends your turn.'
                  '\nYour score for this round is: 0')
            return 0
        return score

    def turn(self, player):
        '''One player turn. Updates total scores. Sets thresholds for ComPlayer
        ending its turns.'''
        round_score = 0
        keepers_list = []
        throw_count = 0
        while True:
            roll = [random.randint(1, 6) for _ in range(6 - len(keepers_list))]
            print(f'\n{player.name}, your dice in []'
                  f'\n 1  2  3  4  5  6'
                  f'\n{roll}')
            choice = player.choose_dice(roll)
            print(f'\nHere are your choices: {choice}')
            score = self.keep_score(choice)
            if score == 0:
                return False
            print(f'\nScore for this throw is: {score}')
            round_score += score
            print(f'\nTotal score for this turn is: {round_score}')
            keepers_list += choice
            if len(keepers_list) == 6:
                print('\nSix keepers! Roll \'em again!')
                keepers_list = []
                throw_count = -1
            if player.name != 'Digital Overlord':
                again = input('''
Roll again or keep current score?
Enter = Roll, K = Keep'''
                              )
                if r'k' in again.lower():
                    player.total_score += round_score
                    if player.total_score < 500:
                        print('\nScore at least 500 to get on the board.')
                        player.total_score = 0
                        round_score = 0
                        return False
                    else:
                        print(f'\n{player.name}\'s score this turn: {round_score}')
                        return False
                else:
                    throw_count += 1
            else:
                if round_score >= 500 and len(keepers_list) > 2:
                    player.total_score += round_score
                    print(f'\n{player.name}\'s score this turn: {round_score}')
                    return False
                else:
                    throw_count += 1
        return False

    def take_turns(self, player_list):
        '''Sets winning score, switches between players, prints winner name
        and score.'''
        while not any(player.total_score >= 10000 for player in player_list):
            for player in player_list:
                self.turn(player)
                for x in range(len(player_list)):
                    print(f'\n{player_list[x].name}\'s total score is: '
                          f'{player_list[x].total_score}')
        winner_dict = {}
        for x in range(len(player_list)):
            winner_dict.update({player_list[x].total_score: player_list[x]})
        winner = winner_dict[max(winner_dict.keys())]
        print(f'\nThe winner is {winner.name}, '
              f'with a score of: {winner.total_score}!!')


class Player:
    def __init__(self, name, total_score):
        self.total_score = 0
        self.name = name


class HumanPlayer(Player):
    '''Contains methods for user input and input validation according to
    scoring rules.'''

    def get_user_choice(self):
        '''Adjusts user input for indexing. Returns input if valid. '''
        try:
            choose = int(input('''
Choose which die to keep by position 1-6
Type position number, then enter. Repeat for all choices.
Press enter when finished
'''
                               ))
        except ValueError:
            return None
        return choose - 1

    def validate_choice(self, choice):
        '''Removes errant choices and informs user of error(s) if present.
        Returns user choices sans errors. '''
        counts = collections.Counter(choice)
        if Game.is_three_pair(Game, choice) and \
                sum(scoring_rules[die - 1][count - 1]
                    for die, count in counts.items()) < 1500:
            return choice
        else:
            error = [die for die, count in counts.items()
                     if scoring_rules[die - 1][count - 1] == 0
                     and not Game.is_straight(Game, choice)
                     and sum(scoring_rules[die - 1][count - 1]
                                for die, count in counts.items()) >
                                Game.is_three_pair(Game, choice)]
        for x in range(len(error)):
            print(f'\nYou must have three {error[x]}\'s to score. '
                  f'Let\'s put that back.')
        choice = [die for die, count in counts.items()
                  for x in range(count)
                  if scoring_rules[die - 1][count - 1] > 0]
        return choice

    def choose_dice(self, roll):
        '''Takes get_user_choice() to choose dice from roll.
        Returns validated choices from validate_choice().'''
        choice_list = []
        while True:
            choose = self.get_user_choice()
            if choose is None:
                break
            if choose >= len(roll):
                print(f'\n{choose + 1} not available\n')
                continue
            if choose in choice_list:
                print('\nYou may choose a die only once.\n')
                continue
            choice_list.append(choose)
        choice = [roll[x] for x in choice_list]
        choice = self.validate_choice(choice)
        return choice


class ComPlayer(Player):
    '''Computer player with method for choosing scoring dice from roll.'''

    def choose_dice(self, roll):
        '''Choose dice according to scoring rules.
        Boop Beep. '''
        counts = collections.Counter(roll)
        if Game.is_three_pair(Game, roll) and \
                sum(scoring_rules[die - 1][count - 1]
                    for die, count in counts.items()) < 1500:
            choice = roll
        elif Game.is_straight(Game, roll):
            choice = roll
        else:
            choice = [die for die, count in counts.items() for x in range(count)
                      if scoring_rules[die - 1][count - 1] > 0]
        return choice


def main():
    while True:
        game = Game([])
        game.take_turns(game.player_list)
        replay = input('\nWould you like to play again? y/n')
        if r'n' in replay.lower():
            return False

print(msg)
if __name__=="__main__":
    main()
