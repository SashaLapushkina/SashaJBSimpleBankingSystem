import random

class Card:
    def __init__(self, number, pin):
        self.number = number
        self.pin = pin
        self.balance = 0

    def show_balance(self):
        print("Balance: " + str(self.balance))

    def __eq__(self, other):
        return self.number == other.number and self.pin == other.pin

def exit_():
    print("Bye!")
    exit(0)

def check_luhn(number):
    numbers = list(number)
    for i in range(0, len(numbers)):
        if i % 2 == 0:
            numbers[i] = int(numbers[i]) * 2
    sum = 0
    for n in numbers:
        if int(n) > 9:
            n = int(n) - 9
        sum += int(n)
    return (10 - int(sum) % 10) % 10

def create():
    global cards
    number = "400000" + str(random.randint(100000000, 999999999))
    number += str(check_luhn(number))
    pin = random.randint(0, 9999)
    cards.append(Card(number, pin))
    print("Your card has been created")
    print("Your card number:")
    print(number)
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
    print("Enter your card number:")
    number = input()
    print("Enter your PIN:")
    pin = int(input())
    new_card = Card(number, pin)
    dont_exist = True
    for card in cards:
        if card == new_card:
            print("You have successfully logged in!")
            account(card)
            dont_exist = False
    if dont_exist:
        print("Wrong card number or PIN!")


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
