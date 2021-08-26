import random
import sqlite3

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
connection.commit()


def print_data():
    cursor.execute("SELECT * FROM card")
    print(cursor.fetchall())


def exit_():
    print("Bye!")
    exit(0)


def check_luhn(number):
    numbers = list(str(number))
    sum = 0
    for i in range(len(numbers)):
        if i % 2 == 0:
            numbers[i] = int(numbers[i]) * 2
        if int(numbers[i]) > 9:
            sum += int(numbers[i]) - 9
        else:
            sum += int(numbers[i])
    return (10 - sum % 10) % 10


def create():
    number = (400000000000000 + random.randint(100000000, 999999999)) * 10
    number += check_luhn(number)
    pin = random.randint(0, 9999)
    cursor.execute("INSERT INTO card (number, pin) values ({}, {})".format(str(number), str(pin)))
    connection.commit()
    print("Your card has been created")
    print("Your card id:")
    print(number)
    print("Your card PIN:")
    print("%04i" % pin)


def account(number, pin):
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")

    command = input()

    if command == '1':
        cursor.execute("SELECT balance FROM card WHERE number = {} and pin = {}".format(str(number), str(pin)))
        print(cursor.fetchone()[0])
        account(number, pin)
    elif command == '2':
        print("You have successfully logged out!")
        menu()
    elif command == '0':
        exit_()


def log_in():
    print("Enter your card id:")
    number = int(input())
    print("Enter your PIN:")
    pin = int(input())
    cursor.execute("SELECT * FROM card WHERE number = {} and pin = {}".format(str(number), str(pin)))
    if cursor.fetchone() == None:
        print("Wrong card id or PIN!")
    else:
        print("You have successfully logged in!")
        account(number, pin)


def menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    command = input()

    if command == '1':
        create()
        menu()
    elif command == '2':
        log_in()
        menu()
    elif command == '0':
        exit_()

menu()