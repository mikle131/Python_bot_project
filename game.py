from typing import List, Dict
from random import shuffle
import datetime


class Game:
    user_1: int
    user_2: int
    turn_id: int
    not_turn_id : int
    bet: int
    is_first_action: bool
    stay_counter : int
    is_correct : bool
    prices = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    is_bj : bool
    last_action_time : int

    def __init__(self, user_1, user_2, bet):
        self._deck = [(i, mast) for i in range(2, 11) for mast in ['♥️', '♠️', '♦️', '♣️']]  # циферки
        self._deck += [(val, mast) for mast in ['♥️', '♠️', '♦️', '♣️'] for val in ['J', 'Q', 'K']]  # картинки
        self._deck += [('A', mast) for mast in ['♥️', '♠️', '♦️', '♣️']]  # тузы
        self.user_1 = user_1
        self.user_2 = user_2
        self.bet = bet
        self.players = {user_1: {'hand': [], 'raw_points' : 0, 'points': 0, 'wins': 0, 'a': 0}, user_2: {'hand': [], 'raw_points' : 0, 'points': 0, 'wins': 0, 'a': 0}}
        self.turn_id = user_1
        self.not_turn_id = user_2
        self.stay_counter = 1
        self.is_first_action = True
        self.is_correct = True
        self.a_counter = 0
        self.is_bj = False

    def start_newround(self, turn_id):
        shuffle(self._deck)
        self.hit(turn_id)
        self.hit(turn_id)
        self.hit(self.not_turn_id)
        self.is_first_action = True
        self.last_action_time = (datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds()
        return self._deck

    def hit(self, turn_id):
        """Имитация взятия карты из колоды"""
        self.is_first_action = False
        card = self._deck.pop()
        self.players[turn_id]['raw_points'] += self.prices[card[0]]
        self.players[turn_id]['points'] += self.prices[card[0]]
        if card[0] == 'A':
            self.players[turn_id]['a'] += 1
        if self.players[turn_id]['raw_points'] > 21:
            self.players[turn_id]['points'] = self.players[turn_id]['raw_points'] - self.players[turn_id]['a'] * 10
        self.players[turn_id]['hand'].append(card)
        self.is_correct_checker(turn_id)
        self.last_action_time = (datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds()
        return 0

    def is_correct_checker(self, turn_id):
        """Проверка, не превысила ли сумма 21"""
        if self.players[turn_id]['points']  > 21:
            self.is_correct = False
        elif self.players[turn_id]['points'] == 21:
            self.is_bj = True
        return 1

    def stay(self):
        self.turn_id, self.not_turn_id = self.not_turn_id, self.turn_id
        self.stay_counter += 1
        self.last_action_time = (datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds()
        return 1

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