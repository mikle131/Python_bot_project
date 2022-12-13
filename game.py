from typing import List, Dict
from random import shuffle


class Game:
    # _deck = [(i, mast) for i in range(2, 11) for mast in ['H', 'S', 'D', 'C']]  # циферки
    # _deck += [(val, mast) for mast in ['H', 'S', 'D', 'C'] for val in ['J', 'Q', 'K']]  # картинки
    # _deck += [('A', mast) for mast in ['H', 'S', 'D', 'C']]  # тузы
    user_1: int
    user_2: int
    turn_id: int
    not_turn_id : int
    bet: int
    is_first_action: bool
    stay_counter : int
    prices = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self, user_1, user_2, bet):
        self._deck = [(i, mast) for i in range(2, 11) for mast in ['♥️', '♠️', '♦️', '♣️']]  # циферки
        self._deck += [(val, mast) for mast in ['♥️', '♠️', '♦️', '♣️'] for val in ['J', 'Q', 'K']]  # картинки
        self._deck += [('A', mast) for mast in ['♥️', '♠️', '♦️', '♣️']]  # тузы
        self.user_1 = user_1
        self.user_2 = user_2
        self.bet = bet
        self.players = {user_1: {'hand': [], 'points': 0, 'wins': 0}, user_2: {'hand': [], 'points': 0, 'wins': 0}}
        self.turn_id = user_1
        self.not_turn_id = user_2
        self.stay_counter = 1
        self.is_first_action = True

    def start_newround(self, turn_id):
        shuffle(self._deck)
        self.hit(turn_id)
        self.hit(turn_id)
        self.hit(self.not_turn_id)
        self.is_first_action = True
        return self._deck

    def hit(self, turn_id):
        """Имитация взятия карты из колоды"""
        self.is_first_action = False
        card = self._deck.pop()
        if card[0] == 'A':
            if self.players[turn_id]['points'] + self.prices[card[0]] <= 21:
                self.players[turn_id]['points'] += self.prices[card[0]]
            else:
                self.players[turn_id]['points'] += 1
        else:
            self.players[turn_id]['points'] += self.prices[card[0]]
        self.players[turn_id]['hand'].append(card)
        return self.players[turn_id]['points']

    def stay(self):
        self.is_first_action = True
        self.turn_id, self.not_turn_id = self.not_turn_id, self.turn_id
        self.hit(self.turn_id)
        self.hit(self.turn_id)
        self.stay_counter += 1
        return self.turn_id

    def get_current_hand(self, id):
        msg = f"Ваша рука: *{self.players[id]['points']}*\n\n"
        for card in self.players[id]['hand']:
            msg += card[1] + '*' + str(card[0]) + '*' + '  •  '
        msg = msg[:-4]
        if id == self.user_1:
            msg += f"\n\nРука противника: *{self.players[self.user_2]['points']}*\n\n"
            for card in self.players[self.user_2]['hand']:
              msg += card[1] + '*' + str(card[0]) + '*' + '  •  '
        else:
            msg += f"\n\nРука противника: *{self.players[self.user_1]['points']}*\n\n"
            for card in self.players[self.user_1]['hand']:
              msg += card[1] + '*' + str(card[0]) + '*' + '  •  '
        msg = msg[:-4]
        return msg