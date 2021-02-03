# IMPORT LIBRARIES
from random import shuffle
from time import sleep
from os import system
import platform
import pickle
# end: IMPORT LIBRARIES


# ================================================================================
# def clearScreen
# Clears the shell console
#
# Arguments - None
#
# Returns - None
#
def clearScreen():
	if platform.system() == 'Windows':
		system("cls")
	else:
		system("clear")
# end: def clearScreen


# ================================================================================
# def printWithEllipses
# Prints a message with an ellipses animation
# Arguments -
# message: The message to add the ellipses animation to
#
# Returns - None
#
def printWithEllipses(message):
	for numOfDots in range(0,8):
		print("\r" + message + "." * (numOfDots % 4), end="   \b\b\b", flush = True)
		sleep(0.5)
# end: def printWithEllipses


# +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# GLOBAL VARIABLES
# +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

chips = 1000 # The number of chips the player starts with
decks = 0 # The number of decks the player is playing with
save = None # If True, saves score
saveInput = None # At the end of the game, asks the player if they would like to save the amount of chips they have
load = None # Asks the player if they want to load a save file
loadedUsername = False # The username that the player loads
username = "" # The username to save
enterUsername = None # The username that the player enters, not necessarily saved though
exit = False # Should the program get exited out of
cardNames = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"] # The names of cards
suits = ["Clubs", "Diamonds", "Hearts", "Spades"] # The names of the suits in a card deck


# Create or find user's save file
try:
	# Attempt to load the save file
	loadFile = open('BlackjackScores.dat', 'rb')
	scores = pickle.load(loadFile)
	loadFile.close()

except EOFError:
	# If file is empty, create a blank dictionary called scores
	scores = {}

except FileNotFoundError:
	# Create a new file if none exists
	loadFile = open('BlackjackScores.dat', 'x')
	scores = {}
	loadFile.close()

# Clear the screen to begin the game
clearScreen()


# Ask the user if they want to load a save file
if len(scores) != 0:

	# Wait until the user enters a valid input
	while load not in ["y", "n", "Y", "N"]:

		# Ask the user if they want to open an exisiting file
		load = input(f"You have {len(scores)} saved game(s). Would you like to load a save file? (Y/N)\n")

		if load.lower() == "y": # The user wants to open a file
		
			while enterUsername not in scores:
				# Get information from the user
				enterUsername = input("What is your username?\n")
				scores.get(enterUsername)
				
				# Confirm the information from the user
				if enterUsername not in scores:
					print("That username has not been saved.")
			
			# Load the number of chips from the save file
			chips = scores[enterUsername]
			loadedUsername = True
			printWithEllipses("Loading save file")
		
		elif load.lower() == "n": # The user does not want to open a file
			pass
		
		else: # If the user entered an invalid input somehow
			print("Unknown command entered. Please try again.")


# Clear the screen
clearScreen()

# Ask the user for the number of card decks they want to use
while decks not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
	decks = input("How many decks of cards would you like to play with? (1-8)\n")

	# Make sure the number is valid
	if decks not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
		print("That is not an number of decks you can play with.")
		

decks = int(decks) # Number of card decks to play with

# Confirmation messages
if decks == 1:
	printWithEllipses("Shuffling a deck of cards")
else:
	printWithEllipses(f"Shuffling {decks} decks of cards")
	
# Clear the screen
clearScreen()


# +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# MAIN GAME LOOP
# +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=++=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# If the user has chips, then play the game as normal
while chips > 0:
	# Creates a list of 52 lists, each of the nested lists has three elements: the card value, the card name, and what is printed to the user, respectively
	cards = []

	# Creates deck(s) of cards
	for i in range(decks):
		for cardName in cardNames:
			for suit in suits:
				if type(cardName) == int:
					cards.append([cardName, cardName, f"{cardName}{suit}"])
				elif cardName == "Ace":
					cards.append([11, cardName, f"{cardName}{suit}"])
				else:
					cards.append([10, cardName, f"{cardName}{suit}"])

	# Shuffles the deck of cards
	shuffle(cards)


	# Ask the user to enter a bet
	while (True):
		# Get a bet from the user
		bet = input(f"You have {chips} chips. Please enter the number of chips you want to bet or [E]xit.\n")

		# Make sure they entered a valid bet
		try:
			bet = int(bet)
		except ValueError:
			# Check if the user wants to exit or not
			if bet.lower() == "e":
				exit = True
				break
			else:
				# If the user does not want to exit, then give them an error
				print("That is not a number of chips that you can bet.")
				continue

		# Make sure the bet amount is valid
		if bet <= 0:
			print("You must bet at least one chip.")

		elif bet > chips:
			print("You don't have that many chips.")

		elif bet <= chips:
			print()
			break

	# Asks the user if they want to save their score if they haven't loaded a username
	if exit is True:
		# If they have loaded a username, automatically saves in order to avoid cheating
		if loadedUsername is True:
			save = True
		else:
			# Ask the user if they want to save a new score
			while saveInput not in ["y", "n", "Y", "N"]:

				saveInput = input("Would you like to save the number of chips you have? (Y/N)\n")
				
				if saveInput.lower() == "y":
					save = True
				elif saveInput.lower() == "n":
					save = False
				else:
					print("Unknown command entered. Please try again.")
		break # Exit MAIN GAME LOOP

	# Reinit variables
	playerCards = [cards[2], cards[3]] # A list of the player's cards
	playerCardsShow = [cards[2][2], cards[3][2]] # A list of what is printed in the console shell
	dealerCards = ["Hidden Card", cards[1][2]] # A list of the dealer's cards
	playerTotal = playerCards[0][0] + playerCards[1][0] # The sum value of the player's cards
	dealerTotal = cards[1][0] # The sum value of the dealer's cards
	insurance = False # Does the player want insurance
	playerSplit = False # Does the player want to split
	splitTurn = False # If the player split, is it their first hand or second
	playerCardsSplit = [] # A list of the cards in the player's second hand
	playerCardsSplitShow = [] # A list of what is printed in the console shell in the player's second hand
	double1 = False # If the player double downed on their first hand AND split
	double2 = False # If the player double downed on their second hand AND split
	cardCount = 4 # The next card that needs to be played
	turn = 1 # How many turns the player has taken
	split = False # Has the player split
	
	# If the user is dealt 2 aces, change the total from 22 to 12
	if playerTotal == 22:
		playerTotal = 12
		cards[3][0] = 1
	

	# ================================================================================
	# def showPlayerHand
	# Shows the players hand
	#
	# Arguments -
	# show: All of the cards that are in the players hand
	# total: The total sum value of all their cards
	#
	# Returns - None
	def showPlayerHand(show, total):
			print(f"Player's cards: {', '.join(show)}")
			print(f"Player's total: {total}\n")
	# end: def showPlayerHand


	# ================================================================================
	# def showHands
	# Shows the dealers and players hand
	#
	# Arguments -
	# pCards: The player's cards
	# pTotal: The player's total
	#
	# Returns - None
	def showHands(pCards, pTotal):
		# Print the dealers hand
		print(f"Dealer's cards: {', '.join(dealerCards)}")
		print(f"Dealer's total: {dealerTotal}\n")
		
		# Print the players hand
		showPlayerHand(pCards, pTotal)
	# end: def showHands


	# Show the hands of the player and dealer
	showHands(playerCardsShow, playerTotal)
	

	# If the player is dealt a blackjack and dealer does not have blackjack, prints blackjack and deals a new hand
	if playerTotal == 21:
		bet = int(bet * 1.5)
		sleep(1)
		print("Blackjack!")
	
		# If the dealer does not also get a blackjack, then the user wins the game
		if dealerTotal + cards[0][0] != 21:
			chips += bet
			print("You win!\n")
			sleep(1)
	
		# If the dealer is also dealt a blackjack, then it is a push
		else:
			print("\n")
			sleep(1)
			dealerTotal = cards[0][0] + cards[1][0]
			dealerCards[0] = cards[0][2]
			showHands(playerCardsShow, playerTotal)
			print("Dealer stays.")
			sleep(1)
			print("It's a push.\n")
		continue

	# If the dealers face up card is an Ace, asks if the player wants insurance
	if cards[1][1] == "Ace" and bet * 1.5 <= chips and bet != 1:
		
		while True:
			insurance = input("Would you like insurance? (Y/N)\n")

			# If the player takes insurance, then tell them insurance taken
			if insurance.lower() == "y":
				print("\nInsurance taken!\n\n")
				sleep(1)

				# Pay back insurance
				if cards[0][0] == 10:
					chips += int(bet / 2)
					dealerCards[0] = cards[0][2]
					showHands(playerCardsShow, playerTotal)
					print("Dealer has a blackjack.")
					print("Insurance paid.")
					insurance = True
					break

				# Don't pay back insurance
				else:
					print("Nobody's home.\n")
					chips -= int(bet / 2)
					break
			
			# The player did not want insurance
			elif insurance.lower() == "n":
				break
			else:
				print("Unknown command entered. Please try again.")

	if insurance is True:
		print()
		continue

	# Asks the player wants to hit or stay until the player chooses stay or busts
	while True:
		if split is True:
			turn = 1
			splitTurn = True
			playerTotalSplit = playerTotal
			playerCardsSplit = playerCards
			playerCardsSplitShow = playerCardsShow
			playerCards = [cards[3], cards[5]]
			playerCardsShow = [playerCards[0][2], playerCards[1][2]]
			playerTotal = playerCards[0][0] + playerCards[1][0]
			if playerTotal == 22:
				playerTotal = 12
				cards[5][0] = 1
			sleep(1)
			print("\n\n")
			showHands(playerCardsShow, playerTotal)
			split = False
			continue

		double = False

		# Bust the player for a losing total
		if playerTotal > 21:
			print("You bust.")

			if playerSplit is True and splitTurn is False:
				split = True
				continue
			else:
				print()
				break

		# Player gets exactly 21
		elif playerTotal == 21:
			if playerSplit is True and splitTurn is False:
				split = True
				continue
			else:
				print()
				break

		# Continue the game; ask the player for an action
		elif turn == 1 and (bet * 2) <= chips:

			if playerCards[0][1] == playerCards[1][1] and playerSplit is False:

				# Ask the user for their action
				hitOrStay = input("Would you like to [H]it, [S]tay, [D]ouble Down, or [Sp]lit?\n")

				# Split
				if hitOrStay.lower() == "sp":
					if cards[3][0] == 1:
						cards[3][0] = 11

					playerCards = [cards[2], cards[4]]
					playerCardsShow = [playerCards[0][2], playerCards[1][2]]
					playerTotal = playerCards[0][0] + playerCards[1][0]

					if playerTotal == 22:
						playerTotal = 12
						cards[4][0] = 1

					playerSplit = True	
					playerTotalSplit = 0
					cardCount = 6
					print()
					showHands(playerCardsShow, playerTotal)
					continue
					
			# If the user does not split, ask for another action
			else:
				hitOrStay = input("Would you like to [H]it, [S]tay, or [D]ouble Down?\n")

			# Double down
			if hitOrStay.lower() == "d":
				double = True
		
		# User does not split or DD
		else:
			hitOrStay = input("Would you like to [H]it or [S]tay?\n")

		# If the user hits
		if hitOrStay.lower() == "h" or double is True:
			# Show new card
			print(f"\nYour new card is: {cards[cardCount][2]}.")
			# Add to the total card count and player hand
			playerTotal = playerTotal + cards[cardCount][0]
			playerCardsShow.append(cards[cardCount][2])
			playerCards.append(cards[cardCount])

			# Split
			for card in range(len(playerCards)):
				if playerSplit is True and splitTurn is True:
					if playerCardsSplit[card][0] == 11 and playerTotal > 21:
						playerCardsSplit[card][0] = 1
						playerTotal -= 10
				else:
					if playerCards[card][0] == 11 and playerTotal > 21:
						playerCards[card][0] = 1
						playerTotal -= 10
			
			# Show the player their new total
			print(f"Your new total is: {playerTotal}.")
			cardCount += 1

			# Double down
			if double is True:
				if playerTotal > 21:
					print("You bust.")
				if playerSplit is True and splitTurn is False:
					double1 = True
					split = True
					continue
				elif playerSplit is True:
					double2 = True
					break
				else:
					bet *= 2
					break

		# Split
		elif hitOrStay.lower() == "s":
			if playerSplit is True and splitTurn is False:
				split = True
				continue
			else:
				print()
				break
		else:
			print("Unknown command entered. Please try again.")
			turn -= 1
		turn += 1

	# Dealer draws a card
	dealerTotal = cards[0][0] + cards[1][0]
	dealerCards[0] = cards[0][2]

	# Check if the dealer busts
	if dealerTotal == 22:
		dealerTotal = 12
		cards[1][0] = 1

	sleep(1)
	print("\n")

	# User split both hands
	if playerSplit is True:
		showHands(playerCardsSplitShow, playerTotalSplit)
		showPlayerHand(playerCardsShow, playerTotal)
	else:
		showHands(playerCardsShow, playerTotal)
	sleep(1)

	# Does the dealers turn. Hits on everything 16 and under, stays on 17 and over, unless soft 17
	while True:
		# Check if the dealer has 17+ card total. If they do and have no aces to lower, then stay. Otherwise hit
		if dealerTotal == 17:
			for card in range(len(dealerCards) + len(playerCards)):
				if cards[card][2] not in playerCardsShow:
					if cards[card][0] == 11:
						# Dealer hits
						print("Dealer hits.")
						print(f"Dealer's new card is: {cards[cardCount][2]}.")
						dealerTotal += cards[cardCount][0]
						dealerCards.append(cards[card][2])

						# Change any aces from 11 to 1 if the dealer has a total >21
						for card in range(len(dealerCards) + len(playerCards) + len(playerCardsSplitShow)):
							if cards[card][2] not in playerCardsShow and cards[card][2] not in playerCardsSplitShow:
								if cards[card][0] == 11 and dealerTotal > 21:
									cards[card][0] = 1
									dealerTotal -= 10
						
						# Show dealers new total
						print(f"Dealer's new total is {dealerTotal}.")
						cardCount += 1
						sleep(2)
						continue
		
		# Dealer stays
		if dealerTotal > 16 and dealerTotal <= 21:
			print("Dealer stays.")
			break
	
		# Dealer always hits if under 16 card total
		elif dealerTotal <= 16:
			# Dealer hits
			print("Dealer hits.")
			print(f"Dealer's new card is: {cards[cardCount][2]}")
			# Add to the dealers card total
			dealerTotal += cards[cardCount][0]
			dealerCards.append(cards[cardCount][2])
	
			# Account for aces
			for card in range(len(dealerCards) + len(playerCards)):
				if cards[card][2] not in playerCardsShow:
					if cards[card][0] == 11 and dealerTotal > 21:
						cards[card][0] = 1
						dealerTotal -= 10
	
			# Show dealers new total
			print(f"Dealer's new total is: {dealerTotal}")
			cardCount += 1
			sleep(2)
	
		# If the dealer hits and gets >21, the dealer busts
		else:
			print("Dealer busts.")
			break

	sleep(1)
	

	# ================================================================================
	# def whoWins
	# Determine who won the game
	#
	# Arguments -
	# compare: Current score to be checked
	# double: Doubles the chips earned for the winner if they double downed, split, and won
	#
	# Returns - None
	def whoWins(compare, double):
		global chips, bet
		if double:
			bet *= 2

		# Checks for a user loss
		if compare > 21:
			print("You lose.")
			chips -= bet
		# Checks for a dealer loss (user win)
		elif dealerTotal > 21:
			print("You win!")
			chips += bet
		# Checks for a tie (push)
		elif compare == dealerTotal:
			print("It's a push.")
		# Checks for greater player total (player win)
		elif compare > dealerTotal:
			print("You win!")
			chips += bet
		# Checks for greater dealer total (dealer win)
		else:
			print("You lose.")
			chips -= bet
		
		if double1 is True:
			bet /= 2
	# end: whoWins


	# Player split
	if playerSplit is True:
		print("\n\n\nHAND 1\n")
		showHands(playerCardsSplitShow, playerTotalSplit)
		if double1 is True:
			whoWins(playerTotalSplit, double1)
		else:
			whoWins(playerTotalSplit, None)
		sleep(2)
		print("\n\n\nHAND 2\n")
	else:
		print("\n")
		
	# Determine who won and show hands
	showHands(playerCardsShow, playerTotal)
	if double2 is True:
		whoWins(playerTotal, double2)
	else:
		whoWins(playerTotal, None)
	print()
	sleep(1)
# end: MAIN GAME LOOP


# If the user wants to save their score
if save is True:

	# Load the users username
	while username in scores or len(username) < 2:
		if loadedUsername is True:
				username = enterUsername
				break

		# Ask the user for an username to save their score as
		else:
			username = input("Please enter a username and remember it in order to load this save file.\n")
		
		# Make sure the username is long enough and has not already been taken
		if len(username) < 2:
			print("Your username must be at least two characters.")
		elif len(username) >= 20:
			print("Your username must be less than 20 characters.")
		elif username in scores and username != enterUsername:
			print("That username is already taken.")

	# Save the users score
	scores[username] = chips

	# Create an entry in the save file
	saveFile = open('BlackjackScores.dat', 'wb')
	pickle.dump(scores, saveFile)
	saveFile.close()

	# Update an users score if they were working with an already loaded username
	if loadedUsername is True:
		printWithEllipses(f"Updating username '{username}' with {chips} chips")
	else:
		printWithEllipses(f"Saving username '{username}' and {chips} chips")
	
	print("\r" + ' ' * (35 + len(username) + len(str(chips))), end = "\r")
	print("Saved!")

# The user has no more chips and loses
elif exit is not True:
	print("\nYou have no more chips.")

	# Delete their score
	if loadedUsername is True:
		del scores[enterUsername]
	saveFile = open('BlackjackScores.dat', 'wb')
	pickle.dump(scores, saveFile)
	saveFile.close()

# End message
sleep(1)
print("Thank you for playing!")