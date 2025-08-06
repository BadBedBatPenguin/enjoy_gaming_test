import random
from enum import Enum, auto
from abc import ABC, abstractmethod


# Define constants for symbols
class Symbols(Enum):
    SYMBOL_EMPTY = auto()
    SYMBOL_REGULAR = auto()
    SYMBOL_BONUS = auto()


class States(Enum):
    INIT = auto()
    SPIN = auto()
    BONUS_INIT = auto()
    BONUS = auto()


class Settings:
    starting_balance = 100
    bonus_trigger_chance = 20
    new_symbol_chance = 50


settings = Settings()


# Initial random source generation
def generate_initial_src(size=100000) -> list[int]:
    random.seed()
    return [random.randint(0, 100) for _ in range(size)]


class BaseModel:
    @classmethod
    def blank(cls):
        return {}


    @classmethod
    def spins(cls):
        return {'round_win': 0}


    @classmethod
    def bonus(cls):
        return {'round_win': 0, 'rounds_left': 3}
    

class BaseGame(ABC):
    @abstractmethod
    def run(self) -> None:
        pass


    @abstractmethod
    def setup_states(self) -> None:
        pass


    @abstractmethod
    def get_next_random(self) -> int:
        pass
    

class GameModel(BaseModel):
    pass


class Game(BaseGame):
    def __init__(self, random_integers: list[int]):
        self.round_initial_data = {}
        self.current_spin = {}
        self.random_integers_index = 0
        self.random_integers = random_integers
        self.current_state = States.INIT
        self.setup_states()
        self.round_data_model_cls = GameModel
    

    def setup_states(self) -> None:
        self.states = {
            States.INIT: self.handler_init,
            States.SPIN: self.handler_spin,
            States.BONUS_INIT: self.handler_bonus_init,
            States.BONUS: self.handler_bonus,
        }


    def get_next_random(self) -> int:
        value = self.random_integers[self.random_integers_index % len(self.random_integers)]
        self.random_integers_index += 1
        return value
    

    def handler_init(self) -> None:
        self.round_initial_data = self.round_data_model_cls.blank()
        self.round_initial_data['spins'] = self.round_data_model_cls.spins()
        self.round_initial_data['bonus'] = self.round_data_model_cls.bonus()
        self.current_spin['bet'] = 1
        self.current_spin['balance'] = settings.starting_balance
        self.current_spin['bonus_triggered'] = False
        self.current_spin['spin_win'] = 0
        self.current_spin['bonus_total_win'] = 0


    def handler_spin(self) -> None:
        # Reset spin win
        self.current_spin['spin_win'] = 0
        self.current_spin['board'] = [Symbols.SYMBOL_REGULAR for _ in range(5)]
        bonus_chance = self.get_next_random()
        if bonus_chance < settings.bonus_trigger_chance:
            self.current_spin['board'][2] = Symbols.SYMBOL_BONUS
            self.current_spin['bonus_triggered'] = True
        else:
            win = (self.get_next_random() % 5) 
            self.current_spin['balance'] += win
            self.current_spin['spin_win'] = win
            self.current_spin['bonus_triggered'] = False


    def handler_bonus_init(self) -> None:
        self.current_spin['rounds_left'] = self.round_initial_data['bonus']['rounds_left']
        self.current_spin['bonus_symbols'] = []
        self.current_spin['bonus_total_win'] = 0

        
    def handler_bonus(self) -> None:
        new_symbol_chance = self.get_next_random()
        if new_symbol_chance < settings.new_symbol_chance:
            new_value = self.get_next_random() % 10 + 1
            self.current_spin['bonus_symbols'].append(new_value)
            self.current_spin['rounds_left'] = self.round_initial_data['bonus']['rounds_left']
        else:
            self.current_spin['rounds_left'] -= 1
        if self.current_spin['rounds_left'] == 0:
            total_bonus_win = sum(self.current_spin['bonus_symbols']) 
            self.current_spin['balance'] += total_bonus_win
            self.current_spin['bonus_total_win'] = total_bonus_win


    def run(self, num_spins: int = 1000) -> None:
        total_spins = 0
        total_bonus_games = 0
        total_win = 0
        self.current_state = States.INIT
        self.handler_init()
        print(f"Game initialized with starting balance: {self.current_spin['balance']}")
        while total_spins < num_spins:
            self.current_state = States.SPIN
            self.handler_spin()
            total_spins += 1
            total_win += self.current_spin.get('spin_win', 0)
            if self.current_spin.get('bonus_triggered'):
                total_bonus_games += 1
                self.current_state = States.BONUS_INIT
                self.handler_bonus_init()
                self.current_state = States.BONUS
                while self.current_spin['rounds_left'] != 0:
                    self.handler_bonus()
                total_win += self.current_spin.get('bonus_total_win', 0)
        print(f"Simulation completed after {total_spins} spins.")
        print(f"Total bonus games triggered: {total_bonus_games}")
        print(f"Final balance: {self.current_spin['balance']}")
        print(f"Total win accumulated: {total_win}")


# Run the game simulation
if __name__ == "__main__":
    random_integers = generate_initial_src(size=1000)
    game = Game(random_integers)
    game.run(1)
