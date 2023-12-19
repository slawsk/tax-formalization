# excess_of

from z3 import *
import formalization_rules as fr

s = Solver()

a = Real('a')
b = Real('b')
c = Real('c')


s.add(a >= 0, b >= 0, c >= 0)


rule_1_left_side = fr.excess_of(a, (b + c))
rule_1_right_side = fr.excess_of((a - b), c)

fr.check_equivalence(s, rule_1_left_side, rule_1_right_side,
                     "Rule 1: Extract the Second Sum")

rule_2_left_side = fr.excess_of((a - b), c)
rule_2_right_side = fr.excess_of(fr.excess_of(a, b), c)

fr.check_equivalence(s, rule_2_left_side, rule_2_right_side,
                     "Rule 2: First Excess Of Equivalent to Subtraction")

rule_3_left_side = fr.excess_of((a + b), c)
rule_3_right_side = fr.excess_of(a, (c - b))

fr.check_equivalence(s, rule_3_left_side, rule_3_right_side,
                     "Rule 3: Push Through the First Sum")
