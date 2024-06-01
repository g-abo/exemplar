"""
6.101 Lab:
SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def transformula(formula, assignments):
    """reduce formula and returns true updated assignments.
    raises exception for resultant False formulas"""
    complete_simple, delta = [], False

    def reducing(clause):
        """consider the clause's unassigned literals from the dictionary.
        make exception for false asignments making the clause"""
        simpler = []
        for var, val in clause:
            if var not in assignments:
                simpler += [(var, val)]
            elif assignments[var] == val:
                return bool(assignments[var] == val)
        if simpler:
            return simpler
        raise AttributeError("False clause asssignment")

    for claus in formula:
        satisfied = reducing(claus)

        if satisfied is True:
            continue
        if 1 != len(satisfied):
            complete_simple.append(satisfied)

        else:
            vari, valu = satisfied[0]
            assignments[vari], delta = valu, True

    return delta, complete_simple


def attempt(var, val, formula):
    """attempt solution with var as val"""
    try:
        assignments = {var: val}
        while True:
            changed, formula = transformula(formula, assignments)
            if not changed:
                break

        result = satisfying_assignment(formula)
        if result is not None:
            result.update(assignments)
            return result
    except AttributeError:
        return None


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None)
    is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    if not formula:
        return {}

    assigned = attempt(formula[0][0][0], formula[0][0][1], formula)
    if not assigned:
        assigned = attempt(formula[0][0][0], not formula[0][0][1], formula)
    return assigned


def combine(n, order):
    """generator fror n elem combination from some order"""
    if isinstance(order, dict):
        order = order.keys()
        order = list(order)
    if n == 0:
        yield []

    elif n == len(order):
        yield order
    else:
        sec, first = order[1:], order[0]
        yield from combine(n, sec)
        for combin in combine(n - 1, sec):
            total = combin + [first]
            yield total
        return


def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                          of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                      for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
              lab write-up

    We assume no student or room names contain underscores.
    """
    desired = []
    for stud, prefs in student_preferences.items():
        result_1 = [(f"{stud}_{ses}", True) for ses in prefs]
        desired.append(result_1)

    one_fit = []
    for stud in student_preferences:
        for comb in combine(2, room_capacities):
            result_2 = []
            for ses in comb:
                result_2.append((f"{stud}_{ses}", False))
            one_fit.append(result_2)

    no_oversub = []
    for ses, space in room_capacities.items():
        if space < len(student_preferences):
            for comb in combine(space + 1, student_preferences):
                clause = [(f"{stud}_{ses}", False) for stud in comb]
                no_oversub.append(clause)

    return desired + one_fit + no_oversub


if __name__ == "__main__":
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
