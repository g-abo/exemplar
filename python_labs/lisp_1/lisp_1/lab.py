"""
6.101 Lab:
LISP Interpreter Part 1
"""

#!/usr/bin/env python3

import sys

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


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
    return 1 if len(args) == 0 else multiply(args[1:]) * args[0]


def divide(args):
    """divide functionality"""
    if len(args) >= 2:
        return args[0] / multiply(args[1:])
    raise SchemeEvaluationError

def typer(a):
    return type(a)
scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
}

scheme_builtins["/"] = divide

scheme_builtins["*"] = multiply

scheme_builtins["type"] = typer

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
        """value of some name in frame"""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.lookup(name)
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
        return frame.lookup(tree)

    if frame is None:
        frame = make_initial_frame()
    if isinstance(tree, list):
        if not tree:
            raise SchemeEvaluationError

        if tree[0] == "define":
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

        elif isinstance(tree[0], list):
            arguments = [evaluate(arg, frame) for arg in tree[1:]]
            lambda_func = evaluate(tree[0], frame)
            return lambda_func(arguments)

        elif "lambda" == tree[0]:
            body, parameters = tree[2], tree[1]
            return Personal(parameters, body, frame)

        arguments = [evaluate(arg, frame) for arg in tree[1:]]
        if callable(evaluate(tree[0], frame)):
            return evaluate(tree[0], frame)(arguments)
        raise SchemeEvaluationError
    raise SchemeEvaluationError

if __name__ == "__main__":
    # NOTE THERE HAVE BEEN CHANGES TO THE REPL, KEEP THIS CODE BLOCK AS WELL
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    import os
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    import schemerepl
    schemerepl.SchemeREPL(use_frames=True, verbose=False, global_frame=None).cmdloop()

# if __name__ == "__main__":
#     # code in this block will only be executed if lab.py is the main file being
#     # run (not when this module is imported)
#     import os

#     sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
#     import schemerepl

#     schemerepl.SchemeREPL(use_frames=True, verbose=False).cmdloop()
