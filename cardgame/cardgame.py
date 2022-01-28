import shuffle
import random

class Engine(object):
    
    #initializes engine
    def __init__(self, deck):
        self.deck = deck


    #main loop of the game. Takes the starting point given and sets the end point
    def play(self):
        current_street = self.deck.starting_point
        last_street = self.deck.current_step('Game End')

        #loops through the game beginning at given starting point
        while current_street != last_street:
            self.deck, next_street = current_street.enter(self.deck)
            current_street = self.deck.current_step(next_street)
        
        current_street.enter(next_street)

class Flop(object):
    
    def enter(self, deck):
        deck = deck

        hand1_score = 0
        hand2_score = 0

        deck.draw_a_card()

        #for loops to sum the top 3 cards of each hand
        for i in deck.hand1[0:3]:
            hand1_score += i

        for i in deck.hand2[0:3]:
            hand2_score += i

        print(f"Here is your current hand: {deck.hand1}")

        player_bet = ""

        while player_bet.lower() not in ("y", "n"):
            player_bet = input(f"Do you think your top three cards are better than the opponents? (Y/N)>  ")

        if player_bet.lower() == "y" and hand1_score > hand2_score:
            deck.score += 1
        elif player_bet.lower() == "n" and hand1_score < hand2_score:
            deck.score += 1
        else:
            deck.score -= 1
        
        return deck, 'Turn'

class Turn(object):

    def enter(self, deck):
        deck = deck

        hand1_score = 0
        hand2_score = 0

        deck.draw_a_card()

        #for loops to sum the bottom 3 cards of each hand
        for i in deck.hand1[-3:-1]:
            hand1_score += i

        for i in deck.hand2[-3:-1]:
            hand2_score += i

        print(f"Here is your current hand: {deck.hand1}")

        player_bet = ""

        while player_bet.lower() not in ("y", "n"):
            player_bet = input(f"Do you think your bottom three cards are worse than the opponents? (Y/N)>  ")

        if player_bet.lower() == "y" and hand1_score < hand2_score:
            deck.score += 1
        elif player_bet.lower() == "n" and hand1_score > hand2_score:
            deck.score += 1
        else:
            deck.score -= 1
        
        return deck, 'River'

class River(object):
        
    def enter(self, deck):
        deck = deck

        hand1_score = 0
        hand2_score = 0

        deck.draw_a_card()

        #for loops to sum the bottom 3 cards of each hand
        for i in deck.hand1:
            hand1_score += i

        for i in deck.hand2:
            hand2_score += i

        hand1_score = hand1_score / len(deck.hand1)

        hand2_score = hand2_score / len(deck.hand2)

        print(f"Here is your current hand: {deck.hand1}")
    
        player_bet = ""

        while player_bet.lower() not in ("y", "n"):
            player_bet = input(f"Do you think your average card is better than the opponents? (Y/N)>  ")

        if player_bet.lower() == "y" and hand1_score >= hand2_score:
            deck.score += 1
        elif player_bet.lower() == "n" and hand1_score <= hand2_score:
            deck.score += 1
        else:
            deck.score -= 1
        
        return deck, 'Showdown'

class Showdown(object):

    def enter(self, deck):
        deck = deck

        hand1_score = 0
        hand2_score = 0

        deck.draw_a_card()

        number_to_guess = random.randint(1, 9)

        hand1_score = deck.hand1.count(number_to_guess)
        hand2_score = deck.hand1.count(number_to_guess)

        print(hand1_score, hand2_score)

        print(f"Here is your current hand: {deck.hand1}")
    
        player_bet = ""

        while player_bet.lower() not in ("y", "n"):
            player_bet = input(f"Do you think you have more {number_to_guess}'s in your hand than your opponent? (Y/N)>  ")

        if player_bet.lower() == "y" and hand1_score > hand2_score:
            deck.score += 1
        elif player_bet.lower() == "n" and hand1_score < hand2_score:
            deck.score += 1
        else:
            deck.score -= 1
        
        return deck, 'Results'

class Results(object):
    
    def enter(self, deck):

        print(f"Here was your hand: {deck.hand1}")
        print(f"And here was your opponenets: {deck.hand2}\n\n\n")

        print(f"You ended up with a score of {deck.score}!")

        if deck.score < 0:
            print(f"Not a very good result for you!")
        elif deck.score == 0:
            print(f"You essentially broke even.")
        elif deck.score > 0 and deck.score < 3:
            print(f"Not the worst I've seen.")
        else:
            print("Great job! Were you cheating?")
        
        return deck, 'Game End'


class GameEnd(object):

    def enter(self, deck):
        print("\n\nThanks for playing.")

class Deck(object):

    steps = {
        'Flop': Flop(),
        'Turn': Turn(),
        'River': River(),
        'Showdown': Showdown(),
        'Results': Results(),
        'Game End': GameEnd()
    }
    
    ##initializes the deck by setting the cards within and shuffling them, creates two hands, dealing five cards to each
    def __init__(self, cards, starting_point):
        
        self.cards = shuffle.deck_setup(cards)
        shuffle.card_shuffle(self.cards)

        self.hand1 = []
        self.hand2 = []

        self.communitycards = []

        self.score = 0

        self.starting_point = self.current_step(starting_point)

        i = 0

        while i < 5:
            self.hand1.append(self.cards.pop())
            self.hand2.append(self.cards.pop())
            i += 1
    
    ##deals one card to each player
    def draw_a_card(self):
        self.hand1.append(self.cards.pop())
        self.hand2.append(self.cards.pop())
        self.hand1.sort(reverse = 1)
        self.hand2.sort(reverse = 1)

    ##community card
    def community_card(self):
        self.communitycards.append(self.cards.pop())

    #function to retrieve corresponding Class from passed step name
    def current_step(self, step_name):
        step = self.steps.get(step_name)
        return step

deck = Deck([], 'Flop')
a_game = Engine(deck)
a_game.play()
