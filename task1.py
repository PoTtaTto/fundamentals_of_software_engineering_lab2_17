#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Standard
import os
import click
from random import randint
import json
import jsonschema


def save_trains(file_name, trains):
    """
    Сохраняет список поездов в файл в формате JSON.

    Args:
    - file_name (str): Имя файла.
    - trains (list): Список поездов.

    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(trains, fout, ensure_ascii=False, indent=4)


def load_trains(file_name):
    """
    Загружает список поездов из файла в формате JSON.

    Args:
    - file_name (str): Имя файла.

    Returns:
    - trains (list): Список поездов.

    """
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as fin:
            loaded_data = json.load(fin)

        with open('scheme.json', 'r', encoding='utf-8') as scheme_file:
            scheme = json.load(scheme_file)

        try:
            jsonschema.validate(loaded_data, scheme)
            return loaded_data
        except jsonschema.exceptions.ValidationError as e:
            print('Ошибка валидации данных:', e)
            return None
    else:
        return []


@click.group()
@click.version_option('1.0.0')
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path())
@click.option('-n', '--number', type=int, prompt=True, help='The number of a train')
@click.option('-d', '--destination', prompt=True, help='Destination point')
@click.option('-st', '--start_time', prompt=True, help='Depart time')
def add(filename, num, destination, start_time):
    """
    Добавляет информацию о поезде в список trains.

    Args:
    - trains (list): Список поездов.
    - num (int): Номер поезда.
    - destination (str): Пункт назначения.
    - start_time (str): Время отправки

    Returns:
    - trains (list): Список поездов.
    """
    trains = load_trains(file_name=filename)

    trains.append({
        'num': num,
        'destination': destination,
        'start_time': start_time
    })
    if len(trains) > 1:
        trains.sort(key=lambda item: item['start_time'])

    save_trains(file_name=filename, trains=trains)


@cli.command()
@click.argument('filename', type=click.Path())
def display(filename):
    """
    Выводит список поездов на экран.

    Args:
    - trains (list): Список поездов.

    """
    line = f'+-{"-" * 15}-+-{"-" * 30}-+-{"-" * 25}-+'
    print(line)
    header = f"| {'№ поезда':^15} | {'Пункт назначения':^30} | {'Время отъезда':^25} |"
    print(header)
    print(line)
    for train in load_trains(file_name=filename):
        num = train.get('num', randint(1000, 10000))
        destination = train.get('destination', 'None')
        start_time = train.get('start_time', 'None')
        recording = f"| {num:^15} | {destination:^30} | {start_time:^25} |"
        print(recording)
    print(line)


@cli.command()
@click.argument('filename', type=click.Path())
@click.option('-D', '--destination', prompt=True, help='The required destination')
def select(filename, destination):
    """
    Выводит информацию о поездах, направляющихся в указанный пункт.

    Args:
    - trains (list): Список поездов.
    - destination (list): Пункт назначения.

    Returns:
    - trains (list): Список поездов.

    """

    return [train for train in load_trains(file_name=filename) if train['destination'].strip() == destination]


def main(command_line=None):
    cli()


if __name__ == '__main__':
    main()
