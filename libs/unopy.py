import random

cards = {
	"common":
		['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'RS','R+',
 		'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BS', 'B+',
 		'Y0', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'YS', 'Y+',
 		'G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'GS', 'G+'],
	"uncommon": ["W0","W4"]
}

def generate_card():
	if random.random() < (8/112):
		return random.choice(cards["uncommon"])
	else:
		return random.choice(cards["common"])

def discord_format_cards(card):
	color = card[0]
	number = card[1]
	formatted_card = ""
	if card == "W0":
		formatted_card = ":ox:"
	elif card == "W4":
		formatted_card = ":broken_heart:"
	if formatted_card != "":
		return formatted_card
	else:
		pass