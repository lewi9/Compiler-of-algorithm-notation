from Komendy import *

input_vars = set()
output_vars = set()
variables = {}
command_list = []
user_commands = []
command_id = 1
how_many = 0
command_list.append('Nazwa pliku')
nr_komendy = 1
wrong_commands = []


# Potrzebna isCommand


def end():
    global command_id
    command_id = 0
    pass


def Compile(directory):
    res = 1
    inp_isdeclared = 0
    outp_isdeclared = 0
    end_isdeclared = 0

    global input_vars
    global output_vars
    global variables
    global command_list
    global user_commands
    global command_id
    global how_many
    global nr_komendy
    global wrong_commands

    input_vars = set()
    output_vars = set()
    variables = {}
    user_commands = []
    command_list = []
    command_id = 1
    how_many = 0
    command_list.append('Nazwa pliku')
    nr_komendy = 1
    wrong_commands = []

    with open(directory, 'r') as f:
        for line in f:
            # Usuwanie spacji i komentarza
            line = ''.join(line.split())
            index = line.find("//")

            if index != -1:
                line = line[:index]

            if line == '':
                continue

            # Szukanie wejścia

            if not inp_isdeclared:
                if line[0:3] == 'we:':
                    user_commands.append(line)
                    inp_isdeclared = 1
                    line = line[3:]
                    var_list = line.split(',')
                    for var in var_list:
                        if '#' in var:
                            try:
                                nazwa, max_e = var.split('#')
                                try:
                                    max_e = int(max_e)
                                    variables['#{}'.format(nazwa)] = []
                                    variables['#{}'.format(nazwa)].append(max_e)
                                except:
                                    input_vars.add(max_e)
                                    variables[max_e] = None
                                    variables['#{}'.format(nazwa)] = []
                                    variables['#{}'.format(nazwa)].append(variables[max_e])
                                    variables['&{}'.format(nazwa)] = max_e

                                input_vars.add('#{}'.format(nazwa))

                            except:
                                print('Error nie poprawna deklaracja ciągu w wejściu')
                                res = 0
                        else:
                            variables[var] = None
                            input_vars.add(var)
                            input_vars.add(var)
                    continue
                else:
                    continue
                    # Szukanie wyjścia

            elif inp_isdeclared and not outp_isdeclared:
                if line == '\n':
                    continue
                elif line[0:3] == 'wy:':
                    user_commands.append(line)
                    outp_isdeclared = 1
                    line = line[3:]
                    var_list = line.split(',')
                    for var in var_list:
                        if '#' in var:
                            try:
                                nazwa, max_e = var.split('#')
                                try:
                                    max_e = int(max_e)
                                    variables['#{}'.format(nazwa)] = []
                                    variables['#{}'.format(nazwa)].append(max_e)
                                except:
                                    input_vars.add(max_e)
                                    variables[max_e] = None
                                    variables['#{}'.format(nazwa)] = []
                                    variables['#{}'.format(nazwa)].append(variables[max_e])
                                output_vars.add('#{}'.format(nazwa))
                            except:
                                print('Error nie poprawna deklaracja ciągu w wyjściu')
                                res = 0
                        else:
                            variables[var] = None
                            output_vars.add(var)
                            output_vars.add(var)
                else:
                    print("ERROR! Niepoprawne znaki między wejściem a wyjściem")
                    res = 0
                continue

            elif inp_isdeclared and outp_isdeclared:

                if line == '\n':
                    continue

                user_commands.append(line)
                temp_list = line.split('.')
                if len(temp_list) != 2:
                    print('ERROR zła ilość kropek w komendzie {}'.format(nr_komendy))
                    res = 0
                    wrong_commands.append(nr_komendy)

                elif int(temp_list[0]) == nr_komendy:
                    comm = isCommand(temp_list[1])

                    if comm:
                        command_list.append(comm)
                        # user_commands.append(line)
                        if comm == 'end()':
                            end_isdeclared = 1
                        # nr_komendy += 1
                    else:
                        print('Error! niepoprawna komenda! {}'.format(nr_komendy))
                        res = 0
                        wrong_commands.append(nr_komendy)
                else:
                    print('Error! nie poprawne znaki między kolejnymi komendami {}'.format(nr_komendy))
                    res = 0
                    wrong_commands.append(nr_komendy)
            nr_komendy += 1
            if end_isdeclared == 1:
                break
        if not end_isdeclared:
            user_commands.append('Brak end')
            print("Error end isn't declared")
            res = 0
            wrong_commands.append(nr_komendy)
        return res


def Execute():
    global command_list
    global command_id
    global how_many
    while True:
        if isinstance(command_list[command_id], tuple):
            try:
                if eval(command_list[command_id][0]):
                    # print('wykonane')
                    exec(command_list[command_id][1], globals())
            except KeyError:
                print("Zmienna niezadeklarowana")
                return 0
            except IndexError:
                print("Indeks poza zasięgiem")
                return 0
            except ZeroDivisionError:
                print("Dzielenie przez zero")
                return 0
        else:
            if command_list[command_id] == 'end()':
                how_many += 1
                return how_many
            # print(command_list[command_id])
            try:
                exec(command_list[command_id], globals())
            except KeyError:
                print("Zmienna niezadeklarowana")
                return 0
            except IndexError:
                print("Indeks poza zasięgiem")
                return 0
            except ZeroDivisionError:
                print("Dzielenie przez zero")
                return 0
        # if command_list[command_id] == 'end()':
        # how_many += 1
        # return how_many
        command_id += 1
        how_many += 1
        if how_many == 100000:
            print('Computation takes too long, prob endless loop')
            return -1


def make_step():
    global command_list
    global command_id
    global how_many
    if isinstance(command_list[command_id], tuple):
        print(command_list[command_id])
        try:
            if eval(command_list[command_id][0]):
                print('wykonane')
                exec(command_list[command_id][1], globals())
        except KeyError:
            print("Zmienna niezadeklarowana")
            return 0
        except IndexError:
            print("Indeks poza zasięgiem")
            return 0
        except ZeroDivisionError:
            print("Dzielenie przez zero")
            return 0
    else:
        print(command_list[command_id])
        try:
            exec(command_list[command_id], globals())
        except KeyError:
            print("Zmienna niezadeklarowana")
            return 0
        except IndexError:
            print("Indeks poza zasięgiem")
            return 0
        except ZeroDivisionError:
            print("Dzielenie przez zero")
            return 0
    if command_list[command_id] == 'end()':
        how_many += 1
        return how_many
    command_id += 1
    how_many += 1
    return 1


def check_with_test(test):
    global input_vars
    global output_vars
    if test[0].keys() == input_vars:
        if test[1].keys() == output_vars:
            for key in test[0]:
                variables[key] = test[0][key]
        else:
            print("Error, różnica outputów między testem a algorytmem")
    else:
        print("Error, różnica inputów między testem a algorytmem")

    temp = Execute()
    if not temp:
        return 0

    for key in test[1]:
        print(variables[key])
        if variables[key] != test[1][key]:
            return 0
    return temp


def ciag_rozmiar_update(nazwa):
    try:
        name = variables['&{}'.format(nazwa)]
        variables['#{}'.format(nazwa)][0] = variables[name]
    except:
        pass

