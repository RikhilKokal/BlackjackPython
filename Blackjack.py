from random import shuffle
from time import sleep
from os import system

system("clear")
chips = 1000

cardNames = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

while chips > 0:
	# Creates a list of 52 lists, each of the nested lists has three elements: the card value, the card name, and what is printed to the user, respectively
	cards = []
	for cardName in cardNames:
		for suit in suits:
			if type(cardName) == int:
				cards.append([cardName, cardName, f"{cardName}{suit}"])
			elif cardName == "Ace":
				cards.append([11, cardName, f"{cardName}{suit}"])
			else:
				cards.append([10, cardName, f"{cardName}{suit}"])

	shuffle(cards)

	# Asks how many chips the user wants to bet
	while True:
		bet = input(f"You have {int(chips)} chips. How many would you like to bet?\n")
		try:
			bet = int(bet)
		except ValueError:
			print("That is not an amount of chips that you can bet.")
			continue
		if bet <= 0:
			print("You must bet at least one chip.")
		elif bet > chips:
			print("You don't have that many chips.")
		elif bet <= chips:
			print()
			break

	playerCards = [cards[2], cards[3]]
	playerCardsShow = [cards[2][2], cards[3][2]]
	dealerCards = ["Hidden Card", cards[1][2]]
	playerTotal = playerCards[0][0] + playerCards[1][0]
	dealerTotal = cards[1][0]
	insurance = False
	playerSplit = False
	splitTurn = False
	playerCardsSplit = []
	double1 = False
	double2 = False
	
	if playerTotal == 22:
		playerTotal = 12
		cards[3][0] = 1
	
	def showPlayerHand(show, total):
			print(f"Player's cards: {', '.join(show)}")
			print(f"Player's total: {total}")
			print()

	def showHands(pCards, pTotal):
		print(f"Dealer's cards: {', '.join(dealerCards)}")
		print(f"Dealer's total: {dealerTotal}")
		print()
		showPlayerHand(pCards, pTotal)
	
	showHands(playerCardsShow, playerTotal)
	
	# If the player is dealt a blackjack, prints blackjack and deals a new hand
	if playerTotal == 21:
		bet = int(bet * 1.5)
		sleep(1)
		print("Blackjack!")
	
		if dealerTotal + cards[0][0] != 21:
			chips += bet
			print("You win!")
			print()
			sleep(1)
	
		else:
			print()
			print()
			sleep(1)
			dealerTotal = cards[0][0] + cards[1][0]
			dealerCards[0] = cards[0][2]
			showHands(playerCardsShow, playerTotal)
			print("Dealer stays.")
			sleep(1)
			print("It's a push.")
			print()
		continue

	# If the dealers face up card is an Ace, asks if the player wants insurance
	if cards[1][1] == "Ace" and bet * 1.5 <= chips and bet != 1:
		while True:
			insurance = input("Would you like insurance? (Y/N)\n")
			if insurance.lower() == "y":
				print()
				print("Insurance taken!")
				print()
				print()
				sleep(1)
				if cards[0][1] == 10:
					chips += int(bet / 2)
					dealerCards[0] = cards[0][2]
					showHands(playerCardsShow, playerTotal)
					print("Dealer has a blackjack.")
					print("Insurance paid.")
					insurance = True
					break
				else:
					print("Nobody's home.")
					print()
					chips -= int(bet / 2)
					break
			elif insurance.lower() == "n":
				break
			else:
				print("Unknown command entered. Please try again.")

	if insurance is True:
		print()
		continue

	cardCount = 4
	turn = 1
	split = False

	# Asks the player wants to hit or stay until the player chooses stay or busts
	while True:
		if split == True:
			turn = 1
			splitTurn = True
			playerTotalSplit = playerTotal
			playerCardsSplit = playerCardsShow
			playerCards = [cards[3], cards[5]]
			playerCardsShow = [playerCards[0][2], playerCards[1][2]]
			playerTotal = playerCards[0][0] + playerCards[1][0]
			if playerTotal == 22:
				playerTotal = 12
				cards[5][0] = 1
			sleep(1)
			print()
			print()
			print()
			showHands(playerCardsShow, playerTotal)
			split = False
			continue
		double = False
		if playerTotal > 21:
			print("You bust.")

			if playerSplit is True and splitTurn == False:
				split = True
				continue
			else:
				print()
				break

		elif playerTotal == 21:
			if playerSplit is True and splitTurn == False:
				split = True
				continue
			else:
				print()
				break

		elif turn == 1 and (bet * 2) <= chips:
			if playerCards[0][1] == playerCards[1][1] and playerSplit == False:
				hitOrStay = input("Would you like to [H]it, [S]tay, [D]ouble Down, or [Sp]lit?\n")
				if hitOrStay.lower() == "sp":
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
			else:
				hitOrStay = input("Would you like to [H]it, [S]tay, or [D]ouble Down?\n")
			if hitOrStay.lower() == "d":
				double = True
		else:
			hitOrStay = input("Would you like to [H]it or [S]tay?\n")

		if hitOrStay.lower() == "h" or double is True:
			print()
			print(f"Your new card is: {cards[cardCount][2]}.")
			playerTotal = playerTotal + cards[cardCount][0]
			playerCardsShow.append(cards[cardCount][2])
			playerCards.append(cards[cardCount])

			for card in range(len(playerCards)):
				if playerCards[card][0] == 11 and playerTotal > 21:
					playerCards[card][0] = 1
					playerTotal -= 10
			
			print(f"Your new total is: {playerTotal}.")
			cardCount += 1

			if double is True:
				if playerTotal > 21:
					print("You bust.")
				if playerSplit is True and splitTurn == False:
					double1 = True
					split = True
					continue
				elif playerSplit is True:
					double2 = True
					break
				else:
					bet *= 2
					break

		elif hitOrStay.lower() == "s":
			if playerSplit is True and splitTurn == False:
				split = True
				continue
			else:
				print()
				break
		else:
			print("Unknown command entered. Please try again.")
			turn -= 1
		turn += 1

	dealerTotal = cards[0][0] + cards[1][0]
	dealerCards[0] = cards[0][2]
	if dealerTotal == 22:
		dealerTotal = 12
		cards[1][0] = 1

	sleep(1)
	print()
	print()
	if playerSplit is True:
		showHands(playerCardsSplit, playerTotalSplit)
		showPlayerHand(playerCardsShow, playerTotal)
	else:
		showHands(playerCardsShow, playerTotal)
	sleep(1)

	# Does the dealers turn. Hits on everything 16 and under, stays on 17 and over, unless soft 17
	while True:
		if dealerTotal == 17:
			for card in range(len(dealerCards) + len(playerCards)):
				if cards[card][2] not in playerCardsShow:
					if cards[card][0] == 11:
						print("Dealer hits.")
						print(f"Dealer's new card is: {cards[cardCount][2]}.")
						dealerTotal += cards[cardCount][0]
						dealerCards.append(cards[card][2])

						for card in range(len(dealerCards) + len(playerCards) + len(playerCardsSplit)):
							if cards[card][2] not in playerCardsShow and cards[card][2] not in playerCardsSplit:
								if cards[card][0] == 11 and dealerTotal > 21:
									cards[card][0] = 1
									dealerTotal -= 10
						
						print(f"Dealer's new total is {dealerTotal}.")
						cardCount += 1
						sleep(2)
						continue
		
		if dealerTotal > 16 and dealerTotal <= 21:
			print("Dealer stays.")
			break
	
		elif dealerTotal <= 16:
			print("Dealer hits.")
			print(f"Dealer's new card is: {cards[cardCount][2]}")
			dealerTotal += cards[cardCount][0]
			dealerCards.append(cards[cardCount][2])
	
			for card in range(len(dealerCards) + len(playerCards)):
				if cards[card][2] not in playerCardsShow:
					if cards[card][0] == 11 and dealerTotal > 21:
						cards[card][0] = 1
						dealerTotal -= 10
	
			print(f"Dealer's new total is: {dealerTotal}")
			cardCount += 1
			sleep(2)
	
		else:
			print("Dealer busts.")
			break

	sleep(1)
	
	# Checks who wins
	def whoWins(compare, double):
		global chips, bet
		if double:
			bet *= 2

		if compare > 21:
			print("You lose.")
			chips -= bet
		elif dealerTotal > 21:
			print("You win!")
			chips += bet
		elif compare == dealerTotal:
			print("It's a push.")
		elif compare > dealerTotal:
			print("You win!")
			chips += bet
		else:
			print("You lose.")
			chips -= bet
		
		if double1 is True:
			bet /= 2

	if playerSplit is True:
		print()
		print()
		print()
		print("HAND 1")
		print()
		showHands(playerCardsSplit, playerTotalSplit)
		if double1 is True:
			whoWins(playerTotalSplit, double1)
		else:
			whoWins(playerTotalSplit, None)
		sleep(2)
		print()
		print()
		print()
		print("HAND 2")
		print()
	else:
		print()
		print()
		print()
		
	showHands(playerCardsShow, playerTotal)
	if double2 is True:
		whoWins(playerTotal, double2)
	else:
		whoWins(playerTotal, None)
	print()
	sleep(1)

print()
print("You have no more chips.")