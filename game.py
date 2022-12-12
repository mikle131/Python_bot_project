from typing import List
from random import shuffle


class Game:
    _deck = [(i, mast) for i in range(2, 11) for mast in ['H', 'S', 'D', 'C']]  # циферки
    _deck += [(10, mast) for mast in ['H', 'S', 'D', 'C']]  # картинки
    _deck += [(11, mast) for mast in ['H', 'S', 'D', 'C']]  # тузы
    user_1 : int
    user_2 : int
    turn : int
    deck : List[int]
    points_1 = 0
    points_2 = 0
    bet : int

    def __init__(self, user_1, user_2, bet):
        self.user_1 = user_1
        self.user_2 = user_2
        self.bet = bet

    def start_newround(self, turn):
        shuffle(self._deck)
        self.hit(turn)
        self.hit(turn)
        return self._deck

    def hit(self, turn):
        if turn == 1:
            card = self._deck.pop()
            if card[0] == 11:
                if self.points_1 + card[0] <= 21:
                    self.points_1 += card[0]
                else:
                    self.points_1 += 1
            else:
                self.points_1 += card[0]
            return self.points_1
        else:
            card = self._deck.pop()
            if card[0] == 11:
                if self.points_2 + card[0] <= 21:
                    self.points_2 += card[0]
                else:
                    self.points_2 += 1
            else:
                self.points_2 += card[0]
            return self.points_2

    def stay(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        self.hit(self.turn)
        self.hit(self.turn)
        return self.turn
