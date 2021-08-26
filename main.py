import random
import sqlite3

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS cards (id INT, pin INT, balance INT)")
connection.commit()

def print_data():
    cursor.execute("SELECT * FROM cards")
    print(cursor.fetchall())

def exit_():
    print("Bye!")
    exit(0)

def check_luhn(id):
    ids = list(str(id))
    sum = 0
    for i in range(len(ids)):
        if i % 2 == 0:
            ids[i] = int(ids[i]) * 2
        if int(ids[i]) > 9:
            sum += int(ids[i]) - 9
        else:
            sum += int(ids[i])
    return (10 - sum % 10) % 10

def create():
    id = (400000000000000 + random.randint(100000000, 999999999)) * 10
    id += check_luhn(id)
    pin = random.randint(0, 9999)
    cursor.execute("INSERT INTO cards values ({}, {}, 0)".format(id, pin))
    connection.commit()
    print_data()
    print("Your card has been created")
    print("Your card id:")
    print(id)
    print("Your card PIN:")
    print("%04i" % pin)

def account(id, pin):
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")

    command = input()

    if command == '1':
        cursor.execute("SELECT balance FROM cards WHERE id = {} and pin = {}".format(id, pin))
        print(cursor.fetchone()[0])
        account(id, pin)
    elif command == '2':
        print("You have successfully logged out!")
        menu()
    elif command == '0':
        exit_()

def log_in():
    print("Enter your card id:")
    id = int(input())
    print("Enter your PIN:")
    pin = int(input())
    cursor.execute("SELECT * FROM cards WHERE id = {} and pin = {}".format(id, pin))
    if cursor.fetchone() == None:
        print("Wrong card id or PIN!")
    else:
        print("You have successfully logged in!")
        account(id, pin)

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
