from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."
    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    """Parse user input into a command and its arguments."""
    try:
        cmd, *args = user_input.split()
        cmd = cmd.lower()
        return cmd, *args
    except ValueError:
        return ("Invalid",)


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Update a contact's phone number using an exact name match."""
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


def find_contacts(name: str, contacts: dict[str, str]) -> list[tuple[str, str]]:
    """Find all contacts matching a name, ignoring case."""
    matches = []
    for stored_name, phone in contacts.items():
        if stored_name.casefold() == name.casefold():
            matches.append((stored_name, phone))
    return matches


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """
    Return the phone number for a single match or formatted
    contact details when multiple names match.
    """
    name = args[0]
    matches = find_contacts(name, contacts)

    if not matches:
        raise KeyError(name)

    if len(matches) == 1:
        return matches[0][1]

    return "\n".join(f"{name}: {phone}" for name, phone in matches)


@input_error
def show_all(contacts: dict[str, str]) -> str:
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main() -> None:
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["exit", "close"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()