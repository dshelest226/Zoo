import sys
import argparse
import configparser
import logging

import zoo
from exceptions import TooSmallNumber
from simulation import Simulator

logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help=" Określa plik konfiguracyjny, w którym zapisane są wartości "
                                               "dla init_pos_limit, sheep_move_dist i wolf_move_dist.")

    parser.add_argument('--dir', '-d', help="Określa podkatalog katalogu bieżącego, w którym mają zostać zapisane"
                                            " pliki pos.json, alive.csv oraz - opcjonalnie - chase.log.")

    parser.add_argument('--log', '-l', help='Określa poziom zdarzeń, które mają być zapisywane w dzienniku.', type=str)

    parser.add_argument('--rounds', '-r', help='Określa liczbę tur.', type=int)

    parser.add_argument('--sheep', '-s', help=' Określa liczbę owiec.', type=int)

    parser.add_argument('--wait', '-w', help=' Określa, że po wyświetlaniu podstawowych informacji o stanie symulacji '
                                             'na zakończenie każdej tury dalszy przebieg symulacji powinien zostać '
                                             'zatrzymany aż do naciśnięcia przez użytkownika jakiegoś klawisza.')

    args = parser.parse_args()

    dir_to_write = args.dir if args.dir else '.'

    if args.log :
        level = args.log
        file_handler = logging.FileHandler(dir_to_write + '/' + 'chase.log', 'w')
        stream_handler = logging.StreamHandler(stream=sys.stdout)

        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-6s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(formatter)

        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        logger.setLevel(level)
        logger.addHandler(file_handler)

    if args.rounds and args.rounds < 1 or args.rounds == 0:
        logger.critical("Obtained number of rounds less then 1")
        raise TooSmallNumber(f'{args.round=}'.split('=')[0], 1)
    if args.sheep and args.sheep < 1 or args.sheep == 0:
        logger.critical("Obtained number of sheeps less then 1")
        raise TooSmallNumber(f'{args.sheep=}'.split('=')[0], 1)
    # Jesli jakis argument nie zostal podany bedzie wykorzystywana wartosc domyslna zgodnie z puntkem 1 w tresci zadania
    move = True if args.wait else False

    sheeps = args.sheep if args.sheep else 15

    rounds = args.rounds if args.rounds else 50

    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)

        zoo.init_pos_limit = float(config['Terrain']['InitPosLimit'])
        zoo.wolf_move_dist = float(config['Movement']['WolfMoveDist'])
        zoo.sheep_move_dist = float(config['Movement']['SheepMoveDist'])

        if zoo.init_pos_limit <= 0 :
            logger.critical("Obtained number of init_pos_limit less then 0")
            raise TooSmallNumber(f'{zoo.init_pos_limit=}'.split('=')[0], 0)
        if zoo.wolf_move_dist <= 0 :
            logger.critical("Obtained number of zoo.wolf_move_dist less then 0")
            raise TooSmallNumber(f'{zoo.wolf_move_dist=}'.split('=')[0], 0)
        if zoo.sheep_move_dist <= 0:
            logger.critical("Obtained number of zoo.sheep_move_dist less then 0")
            raise TooSmallNumber(f'{zoo.sheep_move_dist=}'.split('=')[0], 0)

    sim = Simulator(rounds, move, sheeps, dir_to_write)
    sim.start()


if __name__ == '__main__':
    main()
