import json


CONTACTS = {}
PLAY = True


def input_error(func):
    def wrapped(*args):
        try:
            return func(*args)
        except KeyError as e:
            print("No name in contacts",)
            return True
        except ValueError as e:
            print("Give me name and phone please")
            return True
        except IndexError as e:
            print(e)
            return True
        except TypeError as e:
            print("Not enough arguments", e)
            return True

    return wrapped


@input_error
def hello_func(*args):
    print('Hello')
    return True


@input_error
def add_contact(*args):
    if not args:
        raise IndexError('No name')
    if len(args) < 2:
        raise IndexError('No number')
    name = args[0]
    number = args[1]
    if CONTACTS.get(args[0]):
        print('This contact already exist')
    else:
        CONTACTS.update({name: number})
    return True


@input_error
def change_contact(*args):
    if not args:
        raise IndexError('No name')
    if len(args) < 2:
        raise IndexError('No number')
    name = args[0]
    number = args[1]
    if CONTACTS.get(name):
        CONTACTS.update({name: number})
    else:
        print(f'No contact "{name}"')
    return True


@input_error
def get_contact(*args):
    if not args:
        raise IndexError('No name')
    name = args[0]
    if CONTACTS.get(name):
        print('\t{:>20} : {:<12} '.format(name, CONTACTS.get(name)))
    else:
        print(f'No contact "{name}"')
    return True


@input_error
def show_all_contacts(*args):
    for name, numbers in CONTACTS.items():
        print('\t{:>20} : {:<12} '.format(name, numbers))
    return True

@input_error
def exit_func(*args):
    return False


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
    operands = []
    for key in OPERATIONS:
        if msg.lower().startswith(key):
            operands.append(key)
            msg = msg.lstrip(key)
            for item in filter(lambda x: x != '', msg.split(' ')):
                operands.append(item.upper())
            return operands
    return ['else']


def get_handler(operator):
    return OPERATIONS.get(operator, waiting_func)


def read_file():
    with open('contacts.json', 'r', encoding='UTF-8') as file:
        contacts = json.load(file)
    return contacts


def write_file():
    with open('contacts.json', 'w', encoding='UTF-8') as file:
        json.dump(CONTACTS, file)


def main():
    play = True

    while play:
        msg = input("Input your message >> ")
        operands = parser(msg)

        handler = get_handler(operands[0])
        if len(operands) == 1:
            play = handler()
        elif len(operands) == 2:
            play = handler(operands[1])
        else:
            play = handler(operands[1], operands[2])


if __name__ == '__main__':
    CONTACTS = read_file()
    main()
    write_file()
