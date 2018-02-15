import random
import collections
import numpy as np

msg = ('''
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
    You must score 500 points to get on the board.
    You'll press Enter a lot. Sorry about that. There will be graphics soon.
    Try and break things! If you do, please tell my how you did it.
    Screen shots of the error message are especially helpful.
    Have fun and thanks for helping me develop my first app!!
''')

valuedict = {1:
                {
                0: 0,
                1: 100,
                2: 200,
                3: 1000,
                4: 2000,
                5: 4000,
                6: 5000
                },
            2: {
                0: 0,
                1: 0,
                2: 0,
                3: 200,
                4: 400,
                5: 800,
                6: 5000
                },
            3: {
                0: 0,
                1: 0,
                2: 0,
                3: 300,
                4: 600,
                5: 1200,
                6: 5000
                },
            4: {
                0: 0,
                1: 0,
                2: 0,
                3: 400,
                4: 800,
                5: 1600,
                6: 5000
                },
            5: {
                0: 0,
                1: 50,
                2: 100,
                3: 500,
                4: 1000,
                5: 2000,
                6: 5000
                },
            6: {
                0: 0,
                1: 0,
                2: 0,
                3: 600,
                4: 1200,
                5: 2400,
                6: 5000
                }
                }


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
            name = input(f'Player {x + 1}, Enter your name:''\n', )
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
                choose = int(input(
'''Choose which die to keep by position 1-6
Type position number, then enter. Repeat for all choices.
Press enter when finished
'''
                            ))-1
                if choose >= len(roll):
                    print(f'\n{choose} not available\n')
                    continue
                if choose in choice_list:
                    print('\nYou can only pick a die once.\nNo cheating!')
                    continue
                else:
                    choice_list.append(choose)
        except ValueError:
            choice = [roll[x] for x in choice_list]
            False
        if choice != None:
            counts = collections.Counter(choice)
            for _ in counts.items():
                if valuedict[_[0]][_[1]] == 0 and not is_full_house(choice)\
                        and not is_straight(choice):
                    print(f'\n{_[0]} is not a keeper.\nNo cheating!')
                    choice = []
        else:
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
        if is_full_house(roll) and sum(valuedict[die][count] for die, count
                    in counts.items()) < 1500:
            keepers = list(roll)
        elif is_straight(roll):
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

def is_full_house(choice):
    return len(choice) == 6 and\
                all(a == b for a, b in zip(*[iter(sorted(choice))]*2))

def is_straight(choice):
    return sorted(choice) == list(range(1, 7))


def keep_score(choice):
    '''Scores choices from self.pick().'''
    score = 0
    counts = collections.Counter(choice)
    score = sum(valuedict[die][count] for die, count in counts.items())
    if score < 1500:
         if is_straight(choice) or is_full_house(choice):
            score += 1500
    if score == 0:
        print('\nNo keepers. What a bummer.\nYour score for this round is: 0')
        return 0
    return score

def throw(keepers_list):
    '''Rolls dice and returns rolls in a list.'''
    roll = [random.randint(1, 6) for _ in range(6-len(keepers_list))]
    return roll

def turn(player):
    '''One player turn.'''
    round_score = 0
    keepers_list = []
    throw_count = 0
    while True:
        roll = throw(keepers_list)
        print(f'\n{player.name}, your dice in []\n 1  2  3  4  5  6\n{roll}\n')
        choice = player.pick(roll)
        print(f'\nHere are your choices: {choice}')
        score = keep_score(choice)
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
Roll again or keep?
Enter = roll K = keep'''
                    )
            if again == r'k':
                player.total_score += round_score
                if player.total_score < 500:
                    print('\nMust score at least 500 to get on the board.')
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

def take_turns(player_list):
    '''Sets winning score, switches between players'''
    winner_dict = {}
    while not any(player.total_score >= 10000 for player in player_list):
        for player in player_list:
            turn(player)
            for x in range(len(player_list)):
                print(f'\n{player_list[x].name}\'s total score is: '
                      f'{player_list[x].total_score}')
    for x in range(len(player_list)):
        winner_dict.update({player_list[x].total_score: player_list[x]})
    winner = winner_dict[max(winner_dict.keys())]
    False
    print(f'\nThe winner is {winner.name}, '
          f'with a score of: {winner.total_score}!!')
    return False

def main():
    player_list = Game.set_player(Game, [])
    take_turns(player_list)

print(msg)
if __name__=="__main__":
    main()
