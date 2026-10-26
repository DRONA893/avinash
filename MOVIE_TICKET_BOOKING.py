import os

FILE = "bookings.txt"

def book_ticket():
    name = input("ENTER CUSTOMER NAME: ")
    movie = input("ENTER MOVIE NAME: ")
    tickets = input("ENTER NUMBER OF TICKETS: ")

    with open(FILE, "a") as f:
        f.write(name + "," + movie + "," + tickets + "\n")

    print("TICKET BOOKED SUCCESSFULLY!")

def view_bookings():
    if not os.path.exists(FILE):
        print("NO BOOKINGS FOUND.")
        return

    with open(FILE, "r") as f:
        data = f.readlines()

    if len(data) == 0:
        print("NO BOOKINGS AVAILABLE.")
    else:
        print("\n--- Booking Records ---")
        for line in data:
            name, movie, tickets = line.strip().split(",")
            print("NAME:", name)
            print("MOVIE:", movie)
            print("TICKETS:", tickets)
            print("----------------------")

def search_booking():
    search = input("ENTER CUSTOMER NAME: ")

    if not os.path.exists(FILE):
        print("NO BOOKINGS FOUND.")
        return

    found = False

    with open(FILE, "r") as f:
        for line in f:
            name, movie, tickets = line.strip().split(",")
            if name.lower() == search.lower():
                print("\nBooking Found")
                print("MOVIE:", movie)
                print("TICKETS:", tickets)
                found = True

    if not found:
        print("BOOKING NOT FOUND.")

def cancel_booking():
    if not os.path.exists(FILE):
        print("NO BOOKINGS FOUND.")
        return

    search = input("ENTER CUSTOMER NAME TO CANCEL BOOKING: ")

    with open(FILE, "r") as f:
        lines = f.readlines()

    with open(FILE, "w") as f:
        found = False
        for line in lines:
            name, movie, tickets = line.strip().split(",")
            if name.lower() != search.lower():
                f.write(line)
            else:
                found = True

    if found:
        print("BOOKING CANCELLED SUCCESSFULLY!")
    else:
        print("BOOKING NOT FOUND.")

while True:
    print("\n===== MOVIE TICKET BOOKING SYSTEM =====")
    print("1. BOOK TICKETS")
    print("2. VIEW BOOKING")
    print("3. SEARCH BOOKING")
    print("4. CANCEL BOOKING")
    print("5. EXIT")

    choice = input("ENTER YOUR CHOICE: ")

    if choice == "1":
        book_ticket()
    elif choice == "2":
        view_bookings()
    elif choice == "3":
        search_booking()
    elif choice == "4":
        cancel_booking()
    elif choice == "5":
        print("THANK YOU!")
        break
    else:
        print("INVALID CHOICE")
