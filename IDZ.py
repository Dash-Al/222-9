#Использовать словарь, содержащий следующие ключи: фамилия, имя; знак Зодиака; дата рождения (список из трёх чисел).
# Написать программу, выполняющую следующие действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть упорядочены по датам рождения; вывод на экран информацию о людях, родившихся под знаком, название которого введено с клавиатуры;
# если таких нет, выдать на дисплей соответствующее сообщение. Оформив каждую команду в виде отдельной функции.
# Добавьте возможность получения имени файла данных, используя соответствующую переменную окружения.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
def input_data():
    data = []
    while True:
        surname = input("Введите фамилию: ")
        name = input("Введите имя: ")
        zodiac = input("Введите знак Зодиака: ")
        birthday = input("Введите дату рождения (через пробел): ").split()
        if len(birthday) != 3:
            print("Неверный формат даты. Повторите ввод.")
            continue
        try:
            birthday = [int(x) for x in birthday]
        except ValueError:
            print("Неверный формат даты. Повторите ввод.")
            continue
        data.append({
            "фамилия": surname,
            "имя": name,
            "знак Зодиака": zodiac,
            "дата рождения": birthday
        })
        if input("Желаете добавить еще запись? (y/n): ") != 'y':
            break
    data.sort(key=lambda x: x["дата рождения"])
    return data


def find_people_by_zodiac(data, zodiac):
    people = []
    for person in data:
        if person["знак Зодиака"] == zodiac:
            people.append(person)
    return people


def print_people(people):
    if len(people) == 0:
        print("Нет людей с таким знаком Зодиака.")
    else:
        for person in people:
            print("Фамилия: {}".format(person["фамилия"]))
            print("Имя: {}".format(person["имя"]))
            print("Знак Зодиака: {}".format(person["знак Зодиака"]))
            print("Дата рождения: {}/{}/{}".format(person["дата рождения"][0], person["дата рождения"][1],
                                                   person["дата рождения"][2]))
            print()


def main():
    filename = os.environ.get("DATA_FILE")
    if filename:
        with open(filename, "r") as file:
            data = eval(file.read())
    else:
        data = input_data()

    zodiac = input("Введите знак Зодиака для поиска: ")
    people = find_people_by_zodiac(data, zodiac)
    print_people(people)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = []

    def test_input_data(self):
        input_data(self.db)
        self.assertEqual(len(self.db), 2)
        self.assertEqual(self.db[0]["фамилия"], "Иванов")
        self.assertEqual(self.db[1]["фамилия"], "Петров")

    def test_find_persons_by_zodiac(self):
        self.db = [
            {"фамилия": "Иванов", "имя": "Иван", "знак Зодиака": "Овен", "дата рождения": [1, 4, 2000]},
            {"фамилия": "Петров", "имя": "Петр", "знак Зодиака": "Лев", "дата рождения": [5, 6, 1999]},
            {"фамилия": "Сидорова", "имя": "Мария", "знак Зодиака": "Овен", "дата рождения": [7, 8, 2001]}
        ]

        # Тест существующего знака Зодиака
        result = find_persons_by_zodiac(self.db, "Овен")
        self.assertEqual(result, "Иванов Иван: [1, 4, 2000]\nСидорова Мария: [7, 8, 2001]")

        # Тест несуществующего знака Зодиака
        result = find_persons_by_zodiac(self.db, "Рыбы")
        self.assertEqual(result, "В базе данных нет людей, родившихся под этим знаком Зодиака")


if __name__ == "__main__":
    unittest.main()
