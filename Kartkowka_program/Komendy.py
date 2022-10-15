def isCommand(line):
    command = isEvaluate(line)
    if command:
        return command
    command = isIf(line)
    if command:
        return command
    command = isGoto(line)
    if command:
        return command
    command = isEnd(line)
    if command:
        return command
    return False


def isIdentificator(variable):
    if len(variable) == 0:
        return False
    if not variable[0].isalpha():
        return False
    for i in range(1, len(variable)):
        if not (variable[i].isalpha() or variable[i].isdigit() or variable[i] == "_"):
            if variable[i] == '#':
                index = variable[i+1:]
                if not index.isdigit():
                    temp = isIdentificator(index)
                    if '#' in index or temp is False:
                        return False
                    if temp[1] is None:
                        index = "variables['" + temp[0] + "']"
                variable = variable.split('#')[0]
                return variable, index
            return False
    return variable, None


def isOperation(operation):
    x = operation.count('+')
    y = operation.count('-')
    z = operation.count('*')
    w = operation.count('/')
    if x + y + z + w > 1:
        return False
    if x or y or z or w:
        if x:
            operation = operation.split('+')
            op = '+'
        elif y:
            operation = operation.split('-')
            op = '-'
        elif z:
            operation = operation.split('*')
            op = '*'
        elif w:
            operation = operation.split('/')
            op = '//'
        operation[0] = isOperand(operation[0])
        operation[1] = isOperand(operation[1])
        if operation[0] is False or operation[1] is False:
            return False
        res = ''
        if isinstance(operation[0], tuple):
            if operation[0][1] is None:
                res += "variables['" + operation[0][0] + "']" + op
            else:
                res += "variables['#" + operation[0][0] + "']" + "[" + operation[0][1] + "]" + op
        else:
            res += operation[0] + op
        if isinstance(operation[1], tuple):
            if operation[1][1] is None:
                res += "variables['" + operation[1][0] + "']"
            else:
                res += "variables['#" + operation[1][0] + "']" + "[" + operation[1][1] + "]"
        else:
            res += operation[1]
        return res
    res = ''
    operation = isOperand(operation)
    if operation is False:
        return False
    if isinstance(operation, tuple):
        if operation[1] is None:
            res += "variables['" + operation[0] + "']"
        else:
            res += "variables['#" + operation[0] + "']" + "[" + operation[1] + "]"
    else:
        res += operation
    return res


def isOperand(operand):
    operand1 = isIdentificator(operand)
    if operand1:
        return operand1
    if operand.isdigit():
        return operand
    return False


def isEvaluate(line):
    line = line.split("<-")
    if len(line) != 2:
        return False
    temp = isIdentificator(line[0])
    if temp is False:
        return False
    line[0], ind1 = temp
    line[1] = isOperation(line[1])
    if line[1] is False:
        return False
    if ind1 is None:
        return "variables['" + line[0] + "']=" + line[1]
    else:
        return "variables['#" + line[0] + "'][" + ind1 + "]=" + line[1]


def isGoto(line):
    if line[:4] == "goto":
        if line[4:].isdigit():
            n = str((int(line[4:]) - 1))
            return "command_id=" + n
    return False


def isEnd(line):
    line = line.upper()
    if line == "END":
        return "end()"
    return False


def isIf(line):
    res = ''
    if line[:2] != "if":
        return False
    line = line.split(")")
    if len(line) != 2:
        return False
    if line[0][2] != "(":
        return False
    line[0] = line[0][3:]

    x = line[0].count('>')
    if x>1:
        print("x")
        return False

    y = line[0].count('<')
    if y>1:
        print('y')
        return False

    a = line[0].count('=')
    if a>1:
        print('a')
        return False

    if (a+x+y!=1) and (a+x+y!=2):
        print(a+x+y)
        return False

    z = line[0].count('>=')
    w = line[0].count('<=')
    b = line[0].count('!=')
    
    #if x:
    #    line[0] = line[0].split('>')
    #    op = '>'
    #elif y:
    #    line[0] = line[0].split('<')
    #    op = '<'
    #elif z:
    #    line[0] = line[0].split('>=')
    #    op = '>='
    #elif w:
    #    line[0] = line[0].split('<=')
    #    op = '<='
    #elif a:
    #    line[0] = line[0].split('=')
    #    op = '=='
    #elif b:
    #    line[0] = line[0].split('!=')
    #    op = '!='

    if b:
        line[0] = line[0].split('!=')
        op = '!='
    elif z:
        line[0] = line[0].split('>=')
        op = '>='
    elif w:
        line[0] = line[0].split('<=')
        op = '<='
    elif a:
        line[0] = line[0].split('=')
        op = '=='
    elif x:
        line[0] = line[0].split('>')
        op = '>'
    elif y:
        line[0] = line[0].split('<')
        op = '<'

    operand1 = isOperand(line[0][0])
    operand2 = isOperand(line[0][1])
    if operand1 and operand2:
        if isinstance(operand1, tuple):
            if operand1[1] is None:
                res += "variables['" + operand1[0] + "']" + op
            else:
                res += "variables['#" + operand1[0] + "']" + "[" + operand1[1] + "]" + op
        else:
            res += operand1 + op
        if isinstance(operand2, tuple):
            if operand2[1] is None:
                res += "variables['" + operand2[0] + "']"
            else:
                res += "variables['#" + operand2[0] + "']" + "[" + operand2[1] + "]"
        else:
            res += operand2
    else:
        return False

    line[1] = isCommand(line[1])
    if line[1] and len(line[1]) != 2:
        return res, line[1]
    return False

