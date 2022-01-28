from random import shuffle

class Cards:
    def __init__(self):
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suites = ['H', 'S', 'C', 'D']
        self.deck = [j + i for j in values for i in suites]

    def shuffle(self):
        shuffle(self.deck)

    def deal(self, n_players):
        self.hands = [self.deck[i::n_players] for i in range(0, n_players)]

c = Cards()
print(c.deck)
c.shuffle()
print(c.deck)
c.deal(4)
print(c.hands)