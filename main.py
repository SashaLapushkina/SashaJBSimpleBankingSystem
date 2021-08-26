import random
import sqlite3

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXIST cards ()")

class Card:
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin
        self.balance = 0

    def show_balance(self):
        print("Balance: " + str(self.balance))

    def __eq__(self, other):
        return self.id == other.id and self.pin == other.pin

def exit_():
    print("Bye!")
    exit(0)

def check_luhn(id):
    ids = list(id)
    sum = 0
    map(int, ids)
    for i in range(len(ids)):
        if i % 2 == 0:
            ids[i] *= 2
        if ids[i] > 9:
            sum += ids[i] - 9
        else:
            sum += ids[i]
    return (10 - sum % 10) % 10

def create():
    global cards
    id = (4000000000000000 + random.randint(100000000, 999999999)) * 10
    id += check_luhn(id)
    pin = random.randint(0, 9999)
    cards.append(Card(id, pin))
    print("Your card has been created")
    print("Your card id:")
    print(id)
    print("Your card PIN:")
    print("%04i" % pin)

def account(card):
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")

    command = input()

    if command == '1':
        card.show_balance()
        account(card)
    elif command == '2':
        print("You have successfully logged out!")
        menu()
    elif command == '0':
        exit_()

def log_in():
    print("Enter your card id:")
    id = input()
    print("Enter your PIN:")
    pin = int(input())
    new_card = Card(id, pin)
    dont_exist = True
    for card in cards:
        if card == new_card:
            print("You have successfully logged in!")
            account(card)
            dont_exist = False
    if dont_exist:
        print("Wrong card id or PIN!")


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

cards = []
#menu()
print(check_luhn("400000261634864"))
