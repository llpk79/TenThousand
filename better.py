import random
import collections

msg = (
    '\n\n        	Welcome to 10,000\n'
	'		     The Game!\n'
	'\n'
	'Game object:\n'
	'	The object of the game is to have the highest score.\n'
	'	Actually, it\'s to have fun!\n'
	'	It might take a minute to get used to playing, just relax,\n'
	'	take a few practice runs, and challenge some friends!\n'
	'\n'
	'To score:\n'
	'	Pick 1\'s and 5\'s from the dice you\'ve thrown.\n'
	'	1\'s are worth 100 points. 5\'s are worth 50 points.\n'
	'	You may also select any three or four of a kind.\n'
	'	Three of a kind scores the number on the die x 100.\n'
	'	Four of a kind scores double a three of a kind of the same number.\n'
	'	Three ones are worth 1000 points, four ones are worth 2000 points.\n'
	'	Choose any combination of the above. We\'ll call \'em \'keepers\'.\n'
	'	Look carefully on your first roll! The following are worth a lot of\n'
	'	points!:\n'	
	'		A Straight 1-6 (chosen in any order) is worth 1500 points.\n'
	'		A Full House (three pairs) is worth 1500 points.\n'
	'		[I\'m really proud of the code for these^^ check it out!!]\n'
	'		Six of a kind scores 5000 points!!!\n'
	'		And you get to roll all six dice again!\n'
	'\n'
	'To play:\n'
	'	For each turn you will start with six dice.\n'
	'	Your dice will appear in [brackets].\n'
	'	It\'s just old school. You\'ll be fine. Hang in there.\n'
	'	You must choose at least one keeper from each throw to continue your\n'
	'	turn.\n'
	'	To choose a keeper, use the reference number (0-5) located\n'
	'	above it.\n'
	'	WTF? Yeah, I know. You\'ll get used to it and it\'ll be fun.\n'
	'	Trust me.\n'
	'	Enter the reference number and hit Enter.\n'
	'	Repeat until you have all the keepers you want selected.\n'
	'	Then, hit Enter again to submit your selections to scoring.\n'
	'	If all six dice are kept, in one or more turns, all six may be\n'
	'	thrown again.\n'
	'	To get on the board you must have a turn worth 500 or more points.\n'	
	'	If you would like to stop rolling and keep your score for the\n'
	'	turn, press k and Enter.\n'
	'	If you wish, press Enter and the remaining die will now be\n'
	'	trown again.\n'
	'	You will choose your keepers and whether to throw again in the\n'
	'	same way until...\n'
	'	Your turn ends because you keep your score or your roll has\n'
	'	no keepers.\n'
	'	The game continues until one player\'s score is over 10,000.\n'
	'	The other players will then have one turn to better that \n'
	'	player\'s score.*\n'
	'	The winner is the player with the highest total score!*\n'
	'	*[Not currently functional. I\'m working on making sure the winner\n'
	'	actually does have the high score, any advice there, or on anything,\n'
	'	would be greatly appreciated!]\n\n'
	'			THANK YOU FOR PLAYING !!\n'
	'			Created by:\n'
	'				Paul Kutrich\n'
	)

class Game:
	def __init__(self, round_score = 0):
		self.round_score = round_score

	#sets number of players and player names.
	def set_player(self):
		players = int(input("Enter number of players:",))
		player_list = []
		x = 0 
		while x < players:
			name = input("Enter your name:",)
			self.name = name
			self.name = Player(name)
			player_list.append(self.name)
			x += 1
		return player_list

	#checks for full house and returns score.				
	def full_house(self, choice):
		pair_count = 0
		score = 0
		for i in range(0,3):
			try:
				if choice[0] == choice[1]:
					pair_count += 1
					del(choice[1], choice[0])
					continue
				if choice[0] == choice[2]:
					pair_count += 1
					del(choice[2], choice[0])
					continue				
				if choice[0] == choice[3]:
					pair_count += 1
					del(choice[3], choice[0])
					continue
				if choice[0] == choice[4]:
					pair_count += 1
					del(choice[4], choice[0])
					continue
				if choice[0] == choice[5]:
					pair_count += 1
					del(choice[5], choice[0])
			except IndexError:
				pass
		if pair_count == 3:
			score += 1500
			print("You got a Full House!!")
		return score

	#checks for straight and returns score. 
	def straight(self, choice):
		score = 0
		if len([(x,y) for x in choice for y in choice if x == y]) == 6:
			score += 1500
			print("You got a Straight!!")
		return score

	#scores choices from Player.pick().
	def keep_score(self, choice):
		score = 0
		if len(choice) == 6:
			score += self.full_house(choice)
			score += self.straight(choice)
			return score
		else:
			valuedict = {1: {
						1: 100, 
						2: 200, 
						3: 1000, 
						4: 2000, 
						6: 5000
						}, 
					2: {
						3: 200, 
						4: 400, 
						6: 5000
						}, 
					3: {
						3: 300,
						4: 600, 
						6: 5000
						}, 
					4: {
						3: 400, 
						4: 800, 
						6: 5000
						}, 
					5: {
						1: 50, 
						2: 100, 
						3: 500, 
						4: 1000,
						6: 5000
						}, 
					6: {
						3: 600, 
						4: 1200, 
						6: 5000
						}
						}
			try:
				counts = collections.Counter(choice)
				score = sum(valuedict[die][count] for die,count in counts.items())
				if score == 0:
					print("No keepers")
					return 0
			except KeyError:
				print("One of your choices was not a keeper.")
				print("Try not cheating next time.\n\n")
		return score

	#sets winning score, updates total scores, 
	#switches between players until winning score met.
	#this is essentially the game script.
	def take_turns(self):
		player_list = Game.set_player(Game)
		scores_list = [self.name.total_score for self.name in player_list
		if self.name.total_score >= 10000]
		while len(scores_list) == 0:
			for x in range(0,len(player_list)):
				player_list[x].turn(player_list[x].name)
				scores_list = [self.name.total_score for self.name
				in player_list if self.name.total_score >= 10000]
				for x in range(0,len(player_list)):
					print("\n",player_list[x].name,"'s total score is",player_list[x].total_score,"\n")
		winner_list = [self.name for self.name in player_list
		if	self.name.total_score >=10000]
		if len(winner_list) > 0:
			winner_list.sort(key=lambda Player: self.name.total_score)
			print("The winner is",winner_list[-1].name,"!! With a score of:"
			,winner_list[-1].total_score,"\n")
		else:
			print("The winner is",winner_list[0].name,"wins!! With a score of:",winner_list[0].total_score,"\n")
		return False
		
class Player(Game):
	def __init__(self, name, total_score = 0):
		self.total_score = total_score
		self.name = name

	#rolls six dice and puts rolls into a list.	Returns list of dice.
	def throw(self, throw_count):
		dice = 5
		list = []
		i = 0
		while i <= dice - len(throw_count):
			i +=1
			list.append(random.randint(1,6))
		return list	

	#takes user input to choose dice by index. Returns list of choices.
	def pick(self, list):
		choice_list = []
		choose = []
		choice = []
		i = 0
		while i <= len(list):
			i += 1
			try:
				choose = (int(input('Choose which die to keep by position 0-5\n Type choice, then enter, repeat\n Press enter when finished:\n')))
				if choose >= len(list):
					print("Choice not available")
				else:
					choice_list.append(choose)
			except ValueError:
					Idx = choice_list
					choice = [list[i] for i in Idx]
					if choice == None:
						choice = []
					return choice

	#one player turn.
	def turn(self, player):
		round_score = 0
		list = self.throw([])
		print("\n",player,"Your dice in []\n  0  1  2  3  4  5\n",list,"\n")
		throw_list = []
		throw_list.append(list)
		choice = self.pick(throw_list[0])
		print("Here are your choices",choice,"\n")
		score = self.keep_score(choice)
		print("Your score for this throw is:",score,"\n")		
		if score == 0:
			round_score = 0
			return round_score
		else:
			round_score += score
		keepers_list = []
		keepers_list += choice
		if len(keepers_list) == 6:
			print("Six keepers! Roll 'em again!\n")
			keepers_list = []
			throw_list = []
			throw_count = -1
		else:
			throw_count = 0
		again = input("Roll again or keep?\nEnter = roll, K = keep\n",)
		if again is r"k":
			self.total_score += round_score
			if self.total_score < 500:
				round_score = 0
				print("Must score 500 to get on the board.\n")
				print("Your score this turn:",round_score,"\n")
				False
				self.total_score = 0
				return round_score
			else:
				print("Your score this turn:",round_score)
				print("Your total_score", self.total_score,"\n")
				False
				return round_score
		elif again != "q":
			while True:			
				for i in range(0,4):
					throw_count += 1
					list = self.throw(keepers_list)
					print("Your dice in []\n  0  1  2  3  4  5\n",list,"\n")
					throw_list.append(list)
					choice = self.pick(throw_list[throw_count])
					print("Here are your choices:",choice,"\n")
					score = self.keep_score(choice)
					print("Your score this throw is:",score,"\n")
					if score == 0:
						round_score = 0
						False
						return round_score
					else:
						round_score += score
					print("Turn score:",round_score,"\n")
					keepers_list += choice
					if len(keepers_list) ==6:
						print("Six keepers! Roll 'em again!\n")
						keepers_list = []
						throw_list = []
						throw_count = -1					
					again = input("Roll again or keep?\nEnter = roll, K = keep\n",)
					if again == r"k":
						self.total_score += round_score
						if self.total_score < 500:
							print("Must score 500 to get on the board.\n")
							print("Your score this turn:",round_score,"\n")
							False
							self.total_score = 0
							round_score = 0
							return round_score
						else:
							print("Your score this turn:",round_score,"\n")
							print("Your total_score", self.total_score,"\n")
							False
							return round_score
		False
		return round_score

def main():
	while True:
		Game.take_turns(Game)

print(msg)
main()