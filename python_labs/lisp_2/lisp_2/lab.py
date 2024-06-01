"""
6.101 Lab:
LISP Interpreter Part 2
"""

#!/usr/bin/env python3
import sys

sys.setrecursionlimit(20_000)


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    pos, tokens = 0, []
    while pos < len(source):
        sym = source[pos]
        if sym in {"(", ")"}:
            tokens.append(sym)
            pos += 1
            continue

        if sym == ";":
            pos = source.find("\n", pos) + 1 if "\n" in source[pos:] else len(source)
            continue
        if sym in {"\n", " "}:
            pos += 1
            continue

        end_pos = pos + 1
        while end_pos < len(source) and source[end_pos] not in {
            " ",
            "(",
            ")",
            ";",
            "\n",
        }:
            end_pos += 1
        tokens.append(source[pos:end_pos])
        pos = end_pos

    return tokens


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """

    def helper(tokens):
        """
        parse recursive function
        """

        if not tokens:
            return tokens
        if tokens[0] == "(":
            par, i = 1, 1

            while i < len(tokens):
                if tokens[i] == "(":
                    par += 1
                if ")" == tokens[i]:
                    par = par - 1
                if par == 0:
                    break
                i += 1

            if par != 0:
                raise SchemeSyntaxError
            return [helper(tokens[1:i])] + helper(tokens[1 + i :])

        if tokens[0] == ")":
            raise SchemeSyntaxError

        if not isinstance(number_or_symbol(tokens[0]), (int, float)):
            return [tokens[0]] + helper(tokens[1:])

        return [number_or_symbol(tokens[0])] + helper(tokens[1:])

    if len(helper(tokens)) <= 1:
        return helper(tokens)[0]
    raise SchemeSyntaxError


######################
# Built-in Functions #
######################
def multiply(args):
    """multiply functionality"""
    if len(args) == 0:
        return 1
    else:
        return multiply(args[1:]) * args[0]


def divide(args):
    """divide functionality"""
    if len(args) >= 2:
        return args[0] / multiply(args[1:])
    raise SchemeEvaluationError


def equal(arg):
    """equality comparison"""
    inter = set(arg)
    return 1 == len(inter)


def compare(arg, typer):
    """general comparisons"""
    comparisons = {
        "gt": lambda x, y: x > y,
        "ge": lambda x, y: x >= y,
        "lt": lambda x, y: x < y,
        "le": lambda x, y: x <= y,
    }
    container = []
    for curr, nxt in zip(arg, arg[1:]):
        result = comparisons[typer](curr, nxt)
        container.append(result)
    return all(container)


def greater_than(argm):
    """greater than comparison"""
    return compare(argm, "gt")


def greater_than_or_equal(argm):
    """greater or equal coparison"""
    return compare(argm, "ge")


def less_than(argm):
    """less than comparison func"""
    return compare(argm, "lt")


def less_than_or_equal(argm):
    """leq math function"""
    return compare(argm, "le")


def not_builtin(arguments):
    """the not function"""
    if len(arguments) != 1:
        raise SchemeEvaluationError
    return not arguments[0]


class Pair:
    """Class to represent a cons cell."""

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr


class EmptyList:
    """empty list representation for scheme"""

    pass


empty_list = EmptyList()


def evaluate_empty_list():
    """essentially points to empty representation"""
    return empty_list


def cons(args):
    """the con cel basic"""
    if len(args) == 2:
        return Pair(args[0], args[1])
    raise SchemeEvaluationError


def car(pair):
    """car function for left of pair"""
    if len(pair) != 1 or not isinstance(pair[0], Pair):
        raise SchemeEvaluationError
    return pair[0].car


def cdr(pair):
    """coulder function for right of pair"""
    if len(pair) != 1 or not isinstance(pair[0], Pair):
        raise SchemeEvaluationError
    return pair[0].cdr


def list_fn(arguments):
    """
    make linked list with the ordered args
    """
    if not arguments:
        return evaluate_empty_list()

    result = evaluate_empty_list()

    for arg in reversed(arguments):
        result = cons([arg, result])

    return result


def is_linked_list(obj):
    """
    Check if the given object is a linked list.
    """
    if len(obj) == 0 or len(obj) > 1:
        raise SchemeEvaluationError
    obj = obj[0]
    if obj == empty_list or isinstance(obj, EmptyList):
        return True
    if not isinstance(obj, Pair):
        return False
    while isinstance(obj, Pair):
        obj = obj.cdr
    return obj == empty_list


def length(litster):
    """
    length of linked list.
    """
    if not is_linked_list(litster) or len(litster) == 0:
        raise SchemeEvaluationError
    if len(litster) > 1:
        raise SchemeEvaluationError
    litster = litster[0]
    count = 0
    while litster != empty_list:
        count += 1
        litster = litster.cdr
    return count


def list_ref(args):
    """
    basically finding the index
    """
    if len(args) != 2 or not isinstance(args[1], int):
        raise SchemeEvaluationError
    litster, idx = args
    if not is_linked_list([litster]) and isinstance(litster, Pair):
        if idx == 0:
            return litster.car
        raise SchemeEvaluationError
    if not is_linked_list([litster]):
        raise SchemeEvaluationError
    current_idx = 0
    while litster != empty_list:
        if current_idx == idx:
            return litster.car
        litster = litster.cdr
        current_idx += 1

    raise SchemeEvaluationError


def append(lists):
    """
    concatenates many lists together.
    """
    if len(lists) == 1 and is_linked_list([lists[0]]):
        return lists[0]
    result = evaluate_empty_list()
    for litster in reversed(lists):
        if not is_linked_list([litster]):
            raise SchemeEvaluationError
        current = reversed_list(litster)
        while current != empty_list:
            result = cons([current.car, result])
            current = current.cdr
    return result


def reversed_list(litster):
    """helper to append for internal order"""
    result = evaluate_empty_list()
    while litster != empty_list:
        result = cons([litster.car, result])
        litster = litster.cdr
    return result


def begin(arguments):
    """the begin function  wrapping definitions"""
    if len(arguments) < 1:
        raise SchemeEvaluationError
    return arguments[-1]


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "#f": False,
    "#t": True,
    "()": evaluate_empty_list,
    "/": divide,
    "*": multiply,
    "equal?": equal,
    ">": greater_than,
    ">=": greater_than_or_equal,
    "<": less_than,
    "<=": less_than_or_equal,
    "not": not_builtin,
    "cons": cons,
    "car": car,
    "cdr": cdr,
    "list": list_fn,
    "list?": is_linked_list,
    "length": length,
    "list-ref": list_ref,
    "append": append,
    "begin": begin,
}


##############
# Evaluation #
##############
class Frame:
    """scoping instances for scheme"""

    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def define(self, name, value):
        """name assignment in frame"""
        self.bindings[name] = value

    def lookup(self, name):
        """value of name in frame"""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise SchemeNameError

    def delete(self, name):
        """delete a variable binding from the frame"""
        if name in self.bindings:
            return self.bindings.pop(name)
        else:
            raise SchemeNameError


class Personal:
    """non scheme_builtins func instances"""

    def __init__(self, parameters, body, defining_frame):
        self.parameters = parameters
        self.defining_frame = defining_frame
        self.body = body

    def __call__(self, arguments, frame=None):
        """
        calling function with arg in frame.
        """
        call_frame = Frame(parent=self.defining_frame)
        if len(self.parameters) != len(arguments):
            raise SchemeEvaluationError
        if frame is None:
            frame = self.defining_frame

        for arg, params in zip(arguments, self.parameters):
            call_frame.define(params, arg)
        return evaluate(self.body, call_frame)


def make_initial_frame():
    """
    global frame creation
    """
    global_frame = Frame(parent=Frame(parent=None))
    for name, value in scheme_builtins.items():
        global_frame.parent.define(name, value)
    return global_frame


def evaluate_file(file_name, frame=None):
    """
    Evaluate the expression from the file, optionally within a specified frame
    return the result.
    """
    if frame is None:
        frame = make_initial_frame()

    with open(file_name, "r") as file:
        expression = file.read()
        return evaluate(parse(tokenize(expression)), frame)


def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """

    if isinstance(tree, (int, float)):
        return tree

    if isinstance(tree, str):
        return evaluate_variable(tree, frame)

    if frame is None:
        frame = make_initial_frame()

    if isinstance(tree, list) and not tree:
        return empty_list

    if isinstance(tree, list):
        return evaluate_list(tree, frame)

    raise SchemeEvaluationError


def evaluate_variable(var, frame):
    """
    variable eval by looking it up in the frame.
    """
    return frame.lookup(var)


def evaluate_list(tree, frame):
    """
    list eval bosed on its first element.
    """
    if tree[0] == "define":
        return evaluate_define(tree, frame)
    elif isinstance(tree[0], list):
        return inner_list(tree, frame)
    elif "lambda" == tree[0]:
        return evaluate_lambda(tree, frame)
    elif tree[0] == "if":
        return evaluate_if(tree, frame)
    elif tree[0] == "and":
        return evaluate_and(tree, frame)
    elif tree[0] == "or":
        return evaluate_or(tree, frame)
    elif tree[0] == "del":
        return evaluate_delete(tree, frame)
    elif tree[0] == "let":
        return evaluate_let(tree, frame)
    elif tree[0] == "set!":
        return evaluate_set(tree, frame)
    else:
        return evaluate_function_call(tree, frame)


def evaluate_define(tree, frame):
    """
    'define' special form.
    """
    if isinstance(tree[1], list):
        name = tree[1][0]
        parameters = tree[1][1:]
        body = tree[2]
        tree = ["define", name, ["lambda", parameters, body]]

    if not isinstance(tree[1], str):
        raise SchemeSyntaxError
    name, value = tree[1], evaluate(tree[2], frame)
    frame.define(name, value)
    return value


def inner_list(tree, frame):
    """
    evaluate again for inner list

    """
    arguments = [evaluate(arg, frame) for arg in tree[1:]]
    return evaluate(tree[0], frame)(arguments)


def evaluate_lambda(tree, frame):
    """
    evaluate lambda special form.
    """
    body, parameters = tree[2], tree[1]
    return Personal(parameters, body, frame)


def evaluate_if(tree, frame):
    """
    'if' special form.
    """
    pred, true_exp, false_exp = tree[1], tree[2], tree[3]
    result = evaluate(pred, frame)
    if result:
        return evaluate(true_exp, frame)
    else:
        return evaluate(false_exp, frame)


def evaluate_and(tree, frame):
    """
    'and' special form.
    """
    for arg in tree[1:]:
        if not evaluate(arg, frame):
            return False
    return True


def evaluate_or(tree, frame):
    """
    'or' special form.
    """
    for arg in tree[1:]:
        if evaluate(arg, frame):
            return True
    return False


def evaluate_delete(tree, frame):
    """
    'del' special form
    """
    if not isinstance(tree[1], str):
        raise SchemeSyntaxError
    var_name = tree[1]
    try:
        return frame.delete(var_name)
    except:
        raise SchemeNameError


def evaluate_let(tree, frame):
    """
    'let' special form.
    """
    if not isinstance(tree[1], list) or not all(
        isinstance(pair, list) and len(pair) == 2 for pair in tree[1]
    ):
        raise SchemeSyntaxError

    bindings = tree[1]
    new_frame = Frame(parent=frame)
    for var, val_expr in bindings:
        val = evaluate(val_expr, frame)
        new_frame.define(var, val)

    return evaluate(tree[2], new_frame)


def evaluate_set(tree, frame):
    """
    'set!' special form

    """
    if not isinstance(tree[1], str):
        raise SchemeSyntaxError
    var_name = tree[1]
    new_value = evaluate(tree[2], frame)

    target_frame = frame
    while target_frame is not None:
        if var_name in target_frame.bindings:
            target_frame.define(var_name, new_value)
            return new_value
        target_frame = target_frame.parent
    raise SchemeNameError


def evaluate_function_call(tree, frame):
    """
    evaluate callable Personal functions.
    """
    arguments = [evaluate(arg, frame) for arg in tree[1:]]
    if callable(evaluate(tree[0], frame)):
        return evaluate(tree[0], frame)(arguments)
    raise SchemeEvaluationError


if __name__ == "__main__":
    # NOTE THERE HAVE BEEN CHANGES TO THE REPL, KEEP THIS CODE BLOCK AS WELL
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    import os

    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

    import schemerepl

    global_frame = make_initial_frame()
    for file_name in sys.argv[1:]:
        if not os.path.exists(file_name):
            raise SchemeNameError
        evaluate_file(file_name, global_frame)
    schemerepl.SchemeREPL(
        sys.modules[__name__], use_frames=True, verbose=False, global_frame=global_frame
    ).cmdloop()
