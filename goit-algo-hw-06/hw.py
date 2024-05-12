from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError("Phone number must contain 10 digits.")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        phone_obj.validate()
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        del self.data[name]


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid value provided."
        except IndexError:
            return "Missing required arguments."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error
def add_contact(address_book, name, *phones):
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."


@input_error
def change_contact(address_book, name, *phones):
    record = address_book.find(name)
    if record:
        for phone in phones:
            record.edit_phone(phone, phones[-1])
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(address_book, name):
    record = address_book.find(name)
    if record:
        return str(record)
    else:
        raise KeyError


@input_error
def show_all(address_book):
    if address_book:
        return "\n".join(str(record) for record in address_book.values())
    else:
        return "No contacts found."


def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(address_book, *args))
        elif command == "change":
            print(change_contact(address_book, *args))
        elif command == "phone":
            print(show_phone(address_book, *args))
        elif command == "all":
            print(show_all(address_book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
