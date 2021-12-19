from zoo import *
import json
import csv


class Simulator:
    def __init__(self):
        self.round = 0
        self.wolf = Wolf()
        self.sheeps = []
        self.target_sheep = [0, True]  # [id, status Dead/Alive ]
        self.data = {}  # Zbior informacji dla zapisu w plik .json
        self.data_csv = []  # Zbior informacji dla zapisu w plik .csv
        self.alive_sheep = 0 # Liczba żywych owiec, potrzebne dla niektorych metod
        for i in range(15):
            self.sheeps.append(Sheep(i))

    def make_turn(self):
        if all(sheep.location[0] is None for sheep in self.sheeps):
            print("All sheeps are dead")
        else:
            for i in range(len(self.sheeps)):
                self.sheeps[i].move()

            self.sheeps, self.target_sheep[0], self.target_sheep[1] = self.wolf.move(self.sheeps)
        self.round += 1

        self.print_log()
        self.write_json()
        self.write_csv()

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
        print('\n')

    def start(self):
        for i in range(50):
            self.make_turn()

        with open('pos.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=3)

        self.write_csv(True)

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

    def write_csv(self, w=False):
        header = ['Numer tury', 'Liczba żywych owiec']
        self.data_csv.append([self.round, self.alive_sheep])

        if w:
            with open('alive.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(self.data_csv)



