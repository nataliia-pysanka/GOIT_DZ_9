import json


# CONTACTS = {}
# PLAY = True

def read_file():
    with open('contacts.json', 'r', encoding='UTF-8') as file:
        return json.load(file)


def write_file(contacts):
    with open('contacts.json', 'w', encoding='UTF-8') as file:
        json.dump(contacts, file)


def input_error(func):
    def wrapped(*args):
        try:
            return func(*args)
        except KeyError:
            return "No name in contacts"
        except ValueError:
            return "Give me name and phone please"
        except IndexError as e:
            return "Sorry, not enough params for command."
        except TypeError as e:
            return "Not enough arguments"

    return wrapped


@input_error
def hello_func(*args):
    return 'Hello'

@input_error
def add_contact(*args):
    name = args[0]
    number = args[1]
    contacts = read_file()
    if contacts.get(args[0]):
        return 'This contact already exist'
    else:
        contacts.update({name: number})
    write_file(contacts)
    return "Contact add successfully"


@input_error
def change_contact(*args):
    name = args[0]
    number = args[1]
    contacts = read_file()
    if contacts.get(name):
        contacts.update({name: number})
    else:
        return f'No contact "{name}"'
    write_file(contacts)
    return "Contact change successfully"


@input_error
def get_contact(*args):
    name = args[0]
    contacts = read_file()
    if contacts.get(name):
        return '\t{:>20} : {:<12} '.format(name, contacts.get(name))
    else:
        return f'No contact "{name}"'


@input_error
def show_all_contacts(*args):
    contacts = read_file()
    result = []
    for name, numbers in contacts.items():
        result.append('\t{:>20} : {:<12} '.format(name, numbers))
    return '\n'.join(result)

@input_error
def exit_func(*args):
    return 'Good Bye!'


@input_error
def waiting_func(*args):
    return True


OPERATIONS = {
    'hello': hello_func,
    'add': add_contact,
    'change': change_contact,
    'phone': get_contact,
    'show all': show_all_contacts,
    'good bye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    'else': waiting_func
}


def parser(msg: str):
    command = None
    operands = []
    for key in OPERATIONS:
        if msg.lower().startswith(key):
            command = OPERATIONS[key]
            msg = msg.lstrip(key)
            for item in filter(lambda x: x != '', msg.split(' ')):
                operands.append(item)
            return command, operands
    return command, operands


def get_handler(operator):
    return OPERATIONS.get(operator, waiting_func)


def main():
    play = True

    while play:
        msg = input("Input your message >> ")
        command, data = parser(msg)
        if command:
            print(command(*data))
            if command == exit_func:
                break
        else:
            print("Sorry, unknown command. Try again.")

if __name__ == '__main__':
    # CONTACTS = read_file()
    main()
    # write_file()
