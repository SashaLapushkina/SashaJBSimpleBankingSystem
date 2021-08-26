import random
import sqlite3

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute("DROP TABLE card")
cursor.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
connection.commit()


def print_data():
    cursor.execute("SELECT * FROM card")
    print(cursor.fetchall())


def exit_():
    print("Bye!")
    exit(0)


def find_luhn(number):
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

def check_luhn(number):
    return find_luhn(int(number / 10)) == number % 10


def create():
    number = (400000000000000 + random.randint(100000000, 999999999)) * 10
    number += find_luhn(number)
    pin = random.randint(0, 9999)
    cursor.execute("INSERT INTO card (number, pin) values ({}, {})".format(str(number), str(pin)))
    connection.commit()
    print("Your card has been created")
    print("Your card id:")
    print(number)
    print("Your card PIN:")
    print("%04i" % pin)

def get_balance(number):
    cursor.execute("SELECT balance FROM card WHERE number = {}".format(str(number)))
    return cursor.fetchone()[0]

def change_balance(number, amount):
    cursor.execute("UPDATE card SET balance = {} WHERE number = {}".format(get_balance(number) + amount, str(number)))
    connection.commit()

def income(number):
    print("Enter income:")
    amount = int(input())
    change_balance(number, amount)
    print("Income was added!")

def transfer(from_number):
    print("Enter card number:")
    to_number = int(input());
    cursor.execute("SELECT * FROM card WHERE number = {}".format(str(to_number)))
    if not check_luhn(to_number):
        print("Probably you made a mistake in the card number. Please try again!")
    elif cursor.fetchone() == None:
        print("Such a card does not exist.")
    else:
        print("Enter how much money you want to transfer:")
        amount = int(input())
        if amount > get_balance(from_number):
            print("Not enough money!")
        else:
            change_balance(from_number, -amount)
            change_balance(to_number, amount)
            print("Success!")


def close_account(number):
    cursor.execute("DELETE FROM card WHERE number = {}".format(str(number)))
    connection.commit()
    print("The account has been closed!")


def account(number):
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")

    command = input()

    if command == '1':
        print(get_balance(number))
        account(number)
    elif command == '2':
        income(number)
        account(number)
    elif command == '3':
        transfer(number)
        account(number)
    elif command == '4':
        close_account(number)
        menu()
    elif command == '5':
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
        account(number)


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