# formalization_rules

from z3 import *


def excess_of(x, y):
    return If(x > y, x - y, 0)


def check_equivalence(s, left_side, right_side, name_of_rule):
    s.push()
    s.add(left_side != right_side)
    if s.check() == unsat:
        print(f"{name_of_rule} works")
    else:
        print(f"{name_of_rule} does not work")
        if s.check() == sat:
            print(s.model())
    s.pop()


def lesser_of(x, y):
    return If(x < y, x, y)
