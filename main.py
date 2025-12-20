from address_book import AddressBook, Record
from colorama import Fore, Style, init


init(autoreset=True)
BROWN = "\033[38;5;94m"


def input_error(value_error_msg=None, key_error_msg=None, index_error_msg=None):

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError as e:
                return (
                    key_error_msg
                    or f"{Fore.RED}Error{Style.RESET_ALL}: contact not found"
                )
            except AttributeError:
                return key_error_msg or "No contact with this name"
            except ValueError as e:
                msg = str(e)

                if (
                    "not enough values to unpack" in msg
                    or "too many values to unpack" in msg
                ):
                    return value_error_msg or "Enter the argument for the command"

                return f"{Fore.RED}Error{Style.RESET_ALL}: {msg}"

            except IndexError:
                return index_error_msg or "Error: not enough arguments provided."
            except Exception as e:
                return f"Unexpected error: {e}"

        return inner

    return decorator


@input_error()
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error(
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide both name and phone number (example: {Fore.MAGENTA}add Alice 1234578910{Style.RESET_ALL})",
)
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = f"{Style.RESET_ALL}Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"{Style.RESET_ALL}Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error(
    key_error_msg="No contact with this name",
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide both name and phone number (example: {Fore.MAGENTA}change Alice 1234578910 10987654321{Style.RESET_ALL}) ",
)
def change_contact(args, book: AddressBook):
    name, old_phone, phone = args
    record = book.find(name)

    record.edit_phone(old_phone, phone)

    return f"{Style.RESET_ALL}Contact {BROWN}'{name}'{Style.RESET_ALL} updated."


@input_error(
    key_error_msg="No phone with this name",
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide a name (example: {Fore.MAGENTA}phone Alice {Style.RESET_ALL})",
)
def show_phone(args, book: AddressBook):
    (name,) = args
    record = book.find(name)
    phones = ", ".join(phone.value for phone in record.phones)

    return f"{Style.RESET_ALL}Phone '{name}': {BROWN}'{phones}' {Style.RESET_ALL}."


@input_error(
    key_error_msg="No contacts.",
    index_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide (example: {Fore.MAGENTA} all{Style.RESET_ALL})",
)
def show_all(args, book: AddressBook):
    if not book:
        raise KeyError
    if args:
        raise IndexError

    return f"{BROWN}{book}{Style.RESET_ALL}"


@input_error(
    key_error_msg="No contact with this name",
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide both name and birthday (example: {Fore.MAGENTA}add-birthday Alice DD.MM.YYYY{Style.RESET_ALL})",
)
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)

    add_b = record.add_birthday(birthday)
    return f"{Style.RESET_ALL}Birthday '{name}': {BROWN}'{add_b}' {Style.RESET_ALL}."


@input_error(
    key_error_msg="No contact with this name",
    value_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide a name (example: {Fore.MAGENTA}show-birthday Alice {Style.RESET_ALL})",
)
def show_birthday(args, book: AddressBook):
    (name,) = args
    record = book.find(name)

    record_birthday = record.birthday.value

    return f"{Style.RESET_ALL}Birthday '{name}': {BROWN}'{record_birthday}' {Style.RESET_ALL}."


@input_error(
    key_error_msg="No birthdays.",
    index_error_msg=f"{Fore.RED}Error{Style.RESET_ALL}: you must provide (example: {Fore.MAGENTA} birthdays{Style.RESET_ALL})",
)
def all_birthdays(args, book: AddressBook):
    if not book:
        raise KeyError
    if args:
        raise IndexError

    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        raise KeyError

    return f"{BROWN}{birthdays}{Style.RESET_ALL}"


def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input(
            f"Enter {Fore.MAGENTA}a command{Style.RESET_ALL}: {Fore.CYAN}"
        )
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Style.RESET_ALL}Good bye!")
            break
        elif command == "hello":
            print(f"{Style.RESET_ALL}How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(all_birthdays(args, book))
        else:
            print(f"{Style.RESET_ALL}Invalid command.")


if __name__ == "__main__":
    main()
