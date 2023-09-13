import csv
from tabulate import tabulate
import os


def main():
    print("\nEduCLI | A CLI application for student database management")
    active = True
    database = []

    with open("student.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            database.append({"ID": line["id"], "First": line["first"], "Last": line["last"], "House": line["house"]})

    while active:
        option = get_input()
        match option:
            case "V":
                view_student(database)
            case "A":
                create_student(database)
            case "U":
                update_student(database)
            case "D":
                delete_student(database)
            case _:
                print("Goodbye!")
                active = False


def get_input():
    options = [{"Key": "V", "Action": "View Students"},
               {"Key": "A", "Action": "Add a Student"},
               {"Key": "U", "Action": "Update a Student"},
               {"Key": "D", "Action": "Delete a Student"},
               {"Key": "E", "Action": "Exit"}]

    while True:
        print(tabulate(options, headers="keys", tablefmt="rounded_grid"))
        option = input("What do you want to do?: ").upper()

        if option in ["V", "A", "U", "D", "E"]:
            return option
        else:
            print("Invalid option, try again.")


def view_student(data):
    print(tabulate(data, headers="keys", tablefmt="rounded_grid"))


def create_student(data):
    with open("student.csv", 'a', newline='') as csvfile:
        fieldnames = ["id", "first", "last", "house"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        i = 1
        for _ in data:
            i += 1
        first = input("First Name: ")
        last = input("Last Name: ")
        house = input("House: ")
        writer.writerow({"id": i, "first": first, "last": last, "house": house})
    data = []
    with open("student.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append({"ID": line["id"], "First": line["first"], "Last": line["last"], "House": line["house"]})
    view_student(data)


def update_student(data):
    stud_id = verify_id(data)
    update_csv(stud_id)

    data = []
    with open("student.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append({"ID": line["id"], "First": line["first"], "Last": line["last"], "House": line["house"]})
    view_student(data)


def delete_student(data):
    numbers = list(student["ID"] for student in data)
    while True:
        try:
            stud_id = input("Which student's data would you like to delete?: ")
            if stud_id in numbers:
                break
            else:
                print("Invalid student ID, please try again.")

        except ValueError:
            print("Invalid input, try again.")

    with open("student.csv", "r") as before:
        with open("temp.csv", "w", newline="") as temp:
            fieldnames = ["id", "first", "last", "house"]
            reader = csv.DictReader(before, fieldnames=fieldnames)
            writer = csv.DictWriter(temp, fieldnames=fieldnames)
            n = 0
            for row in reader:
                if stud_id == row["id"]:
                    print("Deleting student", row["id"])
                    n = 1
                    pass
                else:
                    if n == 1:
                        row = {"id": int(row["id"])-1, "first": row["first"], "last": row["last"], "house": row["house"]}
                        writer.writerow(row)
                    else:
                        row = {"id": row["id"], "first": row["first"], "last": row["last"], "house": row["house"]}
                        writer.writerow(row)
    with open("temp.csv", "r") as after:
        with open("student.csv", "w", newline="") as final:
            fieldnames = ["id", "first", "last", "house"]
            reader = csv.DictReader(after, fieldnames=fieldnames)
            writer = csv.DictWriter(final, fieldnames=fieldnames)
            for row in reader:
                writer.writerow(row)
    os.remove("temp.csv")

    data = []
    with open("student.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append({"ID": line["id"], "First": line["first"], "Last": line["last"], "House": line["house"]})
    view_student(data)


def verify_id(data):
    numbers = list(student["ID"] for student in data)
    while True:
        try:
            stud_id = input("Which student's data would you like to update?: ")
            if stud_id in numbers:
                break
            else:
                print("Invalid student ID, please try again.")

        except ValueError:
            print("Invalid input, try again.")
    return stud_id


def update_csv(stud_id):
    first = input("Student's updated first name: ")
    last = input("Student's updated last name: ")
    house = input("Student's updated house: ")

    with open("student.csv", "r") as before:
        with open("temp.csv", "w", newline="") as temp:
            fieldnames = ["id", "first", "last", "house"]
            reader = csv.DictReader(before, fieldnames=fieldnames)
            writer = csv.DictWriter(temp, fieldnames=fieldnames)
            for row in reader:
                if stud_id == row["id"]:
                    print("Updating student", row["id"])
                    if first == "":
                        first = row["first"]
                    if last == "":
                        last = row["last"]
                    if house == "":
                        house = row["house"]
                    row["first"], row["last"], row["house"] = first, last, house
                    row = {"id": stud_id, "first": row["first"], "last": row["last"], "house": row["house"]}
                    writer.writerow(row)
                else:
                    writer.writerow(row)

    with open("temp.csv", "r") as after:
        with open("student.csv", "w", newline="") as final:
            fieldnames = ["id", "first", "last", "house"]
            reader = csv.DictReader(after, fieldnames=fieldnames)
            writer = csv.DictWriter(final, fieldnames=fieldnames)
            for row in reader:
                writer.writerow(row)
    os.remove("temp.csv")


if __name__ == "__main__":
    main()
