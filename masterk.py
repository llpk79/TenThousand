import random
import collections
import numpy as np

valuedict = {1: {
                0: 0,
                1: 100,
                2: 200,
                3: 1000,
                4: 2000,
                5: 0,
                6: 5000
                },
            2: {
                0: 0,
                1: 0,
                2: 0,
                3: 200,
                4: 400,
                5: 0,
                6: 5000
                },
            3: {
                0: 0,
                1: 0,
                2: 0,
                3: 300,
                4: 600,
                5: 0,
                6: 5000
                },
            4: {
                0: 0,
                1: 0,
                2: 0,
                3: 400,
                4: 800,
                5: 0,
                6: 5000
                },
            5: {
                0: 0,
                1: 50,
                2: 100,
                3: 500,
                4: 1000,
                5: 0,
                6: 5000
                },
            6: {
                0: 0,
                1: 0,
                2: 0,
                3: 600,
                4: 1200,
                5: 0,
                6: 5000
                }
                }


def is_full_house(choice):
    if len(choice) == 6 and\
                all(a == b for a, b in zip(*[iter(sorted(choice))]*2)):
        return 1500
    else:
        return 0


def is_straight(choice):
    if sorted(choice) == list(range(1, 7)):
        return 1500
    else:
        return 0


def keep_score(choice):
    '''Scores choices from Player.pick().'''
    score = 0
    score += is_straight(choice)
    score += is_full_house(choice)
    if score == 0:
        counts = collections.Counter(choice)
        try:
            score = sum(valuedict[die][count] for die, count
                        in counts.items())
        except KeyError:
            pass
    if score == 0:
        print('\nNo keepers. What a bummer.\nYour score for this round is: 0')
        return 0
    return score


class Game:
    def __init__(self, player_list):
        self.player_list = player_list

    def set_player(self, player_list=[]):
        '''Sets number of players and player names.'''
        players = int(input('How many humans are playing?''\n', ))
        digi_player = input('Do you want to play against Digital Overlord? y/n''\n')
        if digi_player == r'y':
            name = 'Digital Overlord'
            self.name = ComPlayer(name)
            player_list.append(self.name)
        x = 0
        while x < players:
            name = input('Enter your name:''\n', )
            self.name = name
            self.name = Player(name)
            player_list.append(self.name)
            x += 1
        return player_list



class Player:
    def __init__(self, name, total_score=0):
        self.total_score = total_score
        self.name = name

    def pick(self, roll):
        '''Takes user input to choose dice by index. Returns choices.'''
        choice_list = []
        try:
            while True:
                choose = int(input('''
Choose which die to keep by position 1-6
Type choice, then enter, repeat for all choices.
Press enter when finished
''',
                            ))-1
                if choose >= len(roll):
                    print('\nChoice not available\nGo ahead and try again.')
                    pass
                else:
                    choice_list.append(choose)
        except ValueError:
            choice = [roll[x] for x in choice_list]
            False
        if choice is None:
            choice = []
        return choice


class ComPlayer:
    def __init__(self, name, total_score=0):
        self.total_score = total_score
        self.name = name

    def pick(self, roll):
        '''Allows computer to choose dice. Boop beep.'''
        counts = collections.Counter(roll)
        keepers = np.zeros(6, dtype=int)
        if is_full_house(roll) == 1500:
            keepers = list(roll)
        elif is_straight(roll) == 1500:
            keepers = list(roll)
        else:
            for _ in counts.items():
                if valuedict[_[0]][_[1]] > 0:
                    for x in range(len(roll)):
                        if roll[x] == _[0]:
                            keepers = np.insert(keepers, x, _[0])
                            keepers = np.delete(keepers, x + 1)
            while 0 in keepers:
                try:
                    for y in range(len(keepers)):
                        if keepers[y] == 0:
                            keepers = np.delete(keepers, y)
                except IndexError:
                    pass
        choice = list(keepers)
        if choice == []:
            return []
        return choice

def throw(throw_list):
    '''Rolls dice and returns rolls in a list.'''
    roll = [random.randint(1, 6) for _ in range(6-len(throw_list))]
    return roll

def turn(player):
    '''One player turn.'''
    round_score = 0
    keepers_list = []
    throw_list = []
    throw_count = 0
    while True:
        roll = throw(keepers_list)
        print(f'\n{player.name}, your dice in []\n 1  2  3  4  5  6\n{roll}\n')
        throw_list.append(roll)
        choice = player.pick(throw_list[throw_count])
        print(f'\nHere are your choices: {choice}')
        score = keep_score(choice)
        if score == 0:
            False
            return round_score
        print(f'\nScore for this throw is: {score}')
        round_score += score
        print(f'\nTotal score for this turn is: {round_score}')
        keepers_list += choice
        if len(keepers_list) ==6:
            print('\nSix keepers! Roll \'em again!')
            keepers_list = []
            throw_list = []
            throw_count = -1
        if player.name != 'Digital Overlord':
            again = (input(
'''Roll again or keep?
Enter = roll K = keep''',
                    ))
            if again == r'k':
                player.total_score += round_score
                if player.total_score < 500:
                    print('\nMust score 500 to get on the board.')
                    False
                    player.total_score = 0
                    round_score = 0
                    return round_score
                else:
                    print(f'\n{player.name}\'s score this turn: {round_score}')
                    False
                    return round_score
            else:
                throw_count += 1
        else:
            if round_score >= 500 and len(keepers_list) is not 6:
                player.total_score += round_score
                if player.total_score > 500:
                    print(f'\nYour score this turn: {round_score}')
                    False
                    return round_score
                else:
                    player.total_score = 0
            else:
                throw_count += 1
    False
    return round_score

def take_turns(self, player_list):
    '''Sets winning score, switches between players'''
    while not any(player.total_score >= 10000 for player
                  in player_list):
        for player in player_list:
            turn(player)
            for x in range(0, len(player_list)):
                print(f'\n{player_list[x].name}\'s total score is: '
                      f'{player_list[x].total_score}')
        if any(player.total_score >= 10000 for player in player_list):
            winner_dict = {}
            for x in range(len(player_list)):
                winner_dict.update({player_list[x].total_score: player_list[x]})
            winner = winner_dict[max(winner_dict.keys())]

        False
    print(f'\nThe winner is {winner.name},'
          f'with a score of: {winner.total_score}!!')
    return False

def main():
    while True:
        player_list = Game.set_player(Game, [])
        take_turns(Game, player_list)
        replay = input('Would you like to play again? y/n')
        if replay == r'y':
            True
        else:
            False
# print(msg)
if __name__=="__main__":
    main()
