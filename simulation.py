import zoo
import json
import csv
import main
from copy import deepcopy

# from decorators import log_debug_decorator
import decorators


class Simulator:
    def __init__(self, rounds_number : int, move : bool, sheeps : int, dir_to_write : str):
        self.directory_to_write = dir_to_write   # Punkt 2, dla argumentu --dir
        self.rounds_number = rounds_number  # Punkt 2, dla argumentu --round
        self.wait_after_move = move  # Punkt 2, dla argumentu --wait | wartosc True or False
        self.sheeps_number = sheeps  # Punkt 2, dla argumentu --sheep

        self.round = 0
        self.wolf = zoo.Wolf()
        self.sheeps = []
        self.target_sheep = [0, True]  # [id, status Dead/Alive ]
        self.data = {}                 # Zbior informacji dla zapisu w plik .json
        self.data_csv = []             # Zbior informacji dla zapisu w plik .csv
        self.alive_sheep = self.sheeps_number           # Liczba żywych owiec, potrzebne dla niektorych metod
        for i in range(self.sheeps_number):            # in range(liczba owiec)
            self.sheeps.append(zoo.Sheep(i))

    @decorators.log_debug_decorator
    def make_turn(self):
        if all(sheep.location[0] is None for sheep in self.sheeps):
            print("Wszystkie owce sa martwe")
        else:
            for i in range(len(self.sheeps)):
                log_old_loctation = deepcopy(self.sheeps[i].location)
                self.sheeps[i].move()
                main.logger.info(f'Sheep number {i} make a move. Old position = {log_old_loctation}, '
                                 f'new position = {self.sheeps[i].location}')

            log_old_loctation = deepcopy(self.wolf.location)
            self.sheeps, self.target_sheep[0], self.target_sheep[1] = self.wolf.move(self.sheeps)
            main.logger.info(f'Wolf make a move. Old position : {log_old_loctation}, '
                             f'new position = {self.wolf.location}')
            main.logger.info(f'Wolf chose target sheep. Sheep number is {self.target_sheep[0]}')
        self.round += 1

        self.print_log()
        self.write_json()
        self.write_csv()

        if self.wait_after_move:
            input('PRESS ENTER\n')

    @decorators.log_debug_decorator
    def print_log(self):
        self.alive_sheep = 0
        for i in self.sheeps:
            if i.location[0] is not None:
                self.alive_sheep += 1
        print(f'Numer tury : {self.round}')
        print(f'Pozycja wilka : {str(self.wolf.location)}')
        print(f'Liczba żywych owiec : {self.alive_sheep}')
        print(f'Wilk goni owce numer : {self.target_sheep[0]}')
        if self.target_sheep[1]:
            print(f'Wilk zjadł owce numer : {self.target_sheep[0]}')
            main.logger.info(f'Wolf kill sheep. Sheep number is {self.target_sheep[0]}')
        print('\n')

    @decorators.log_debug_decorator
    def start(self):
        for i in range(self.rounds_number):     # liczba tur
            main.logger.info(f'New round is started. Round number is {i+1}')
            main.logger.info(f'Number of alive sheeps : {self.alive_sheep}')
            self.make_turn()

        with open(self.directory_to_write + '/' + 'pos.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=3)

        self.write_csv(True)

    @decorators.log_debug_decorator
    def write_json(self):
        self.data[f'round_no {self.round}'] = []
        self.data[f'round_no {self.round}'].append({
            'wolf_pos': self.wolf.location,
            'sheep_pos': []
        })
        for i in range(len(self.sheeps)):
            self.data[f'round_no {self.round}'][0].get('sheep_pos').append({
                'nr': f'{i}',
                'position': self.sheeps[i].location
            })

    @decorators.log_debug_decorator
    def write_csv(self, w=False):
        header = ['Numer tury', 'Liczba żywych owiec']
        self.data_csv.append([self.round, self.alive_sheep])

        if w:
            with open(self.directory_to_write + '/' + 'alive.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(self.data_csv)



