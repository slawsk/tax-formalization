# formalize

from z3 import *
import formalization_rules as fr

s = Solver()

# Capital gains and losses are integers because numbers
# on the tax return will generally be rounded to the nearest
# dollar.
LTCG = Int('LTCG')
LTCL = Int('LTCL')
STCG = Int('STCG')
STCL = Int('STCL')

# "Other income" is the non-capital gain net income.
# This will go into the 1211(b)(2) calculation.
Other_Income = Int("Other_Income")

Total_Gains = LTCG + STCG
Total_Losses = LTCL + STCL

# This is from Section 1211(b), which states that the amount of
# capital losses that can be carried forward equals the amount of
# capital gains plus the lesser of (1) $3000, or (2) the excess of
# capital losses over capital gains. This is the (1) or (2) part.
Section_1211_b_Amount = fr.lesser_of(
    3000, fr.excess_of(Total_Losses, Total_Gains))

# And here are the total permitted capital losses from Section 1211(b).
# The taxpayer is permitted to use capital losses up to capital gains,
# increased by the Section 1211(b) amount of the lesser of $3000 and
# the excess of Total Losses over Total Gains.
Permitted_Losses = fr.lesser_of(
    Total_Gains, Total_Losses) + Section_1211_b_Amount

# Taxable income includes capital gains and other income, reduced by
# permitted losses. This amount might be negative, but that's ok;
# this is not real taxable income, it is the "taxable income" number
# to be used in the Section 1212(b)(2) calculation, and in that section
# it explicitly says that negative taxable income is possible just for
# this calculation. Thus there is no constraint later that says that
# this must be positive.
Taxable_Income = Total_Gains + Other_Income - Permitted_Losses

# This is the adjusted taxable income as defined in Section 1212(b)(2)(B).
Adjusted_Taxable_Income = Taxable_Income + Section_1211_b_Amount

# This is the full Section 1212(b)(2)(A) amount, which will be added back in
# to do the calculation of short-term capital gain, for purposes of the
# capital loss carryforward only. Notice that this also includes a technical
# fix, where the Section 1212(b) amount cannot be negative.
Section_1212_b_Amount = If(Adjusted_Taxable_Income >= 0,
                           fr.lesser_of(Section_1211_b_Amount,
                                        Adjusted_Taxable_Income),
                           0)


# The definitions of Net Long Term Capital Gain, Net Long Term Capital Loss,
# Net Short Term Capital Gain, and Net Short Term Capital Loss,
# all from Section 1222.
NLTCG = fr.excess_of(LTCG, LTCL)
NLTCL = fr.excess_of(LTCL, LTCG)
NSTCG = fr.excess_of(STCG, STCL)
NSTCL = fr.excess_of(STCL, STCG)

# Net short-term capital gain and net short-term capital loss,
# recalculated for purposes of the carryforward only, as required
# by Section 1212(b)(2)(A).
STCG_for_carryover = STCG + Section_1212_b_Amount

NSTCG_for_carryover = fr.excess_of(STCG_for_carryover, STCL)
NSTCL_for_carryover = fr.excess_of(STCL, STCG_for_carryover)

# Definition of Net Capital Loss from Section 1222.
NCL = fr.excess_of((LTCL + STCL), Permitted_Losses)

# Long term capital gain, long term capital loss,
# short term capital gain, short term capital loss,
# and other income are all greater than or equal to 0.
s.add(LTCG >= 0, LTCL >= 0, STCL >= 0, STCG >= 0)

# This constraint just makes the examples easier to read--
# if something turns out not to be true and the program gives
# an example, this just says that certain values should be multiples
# of $100. Check whether the models work without it, and then
# uncomment it to get the counterexamples to be more legible.
# s.add(Other_Income % 100 == 0, LTCL % 100 == 0, LTCG % 100 == 0,
#      STCL % 100 == 0, STCG % 100 == 0)

# Section 1212(b)(1)(A). This does not include the requirement
# that there be a net capital loss.
statute_carryover_short = fr.excess_of(NSTCL_for_carryover, NLTCG)

# Section 1212(b)(1)(B). This does not include the requirement
# that there be a net capital loss.
statute_carryover_long = fr.excess_of(NLTCL, NSTCG_for_carryover)

# The total amount of losses that can be used is the sum of the
# long-term and short-term loss carryovers.
statute_carryover_total = statute_carryover_long + statute_carryover_short

# The statute says that IF there is net capital loss,
# then there is carryover. These three formalizations are thus
# what the statute actually says.
statute_carryover_short_actual = If(NCL > 0, statute_carryover_short, 0)

statute_carryover_long_actual = If(NCL > 0, statute_carryover_long, 0)

statute_carryover_total_actual = statute_carryover_short_actual + \
    statute_carryover_long_actual

# This is my formalization of the informal term "unused capital losses."
unused_capital_losses = fr.excess_of(
    (LTCL + STCL), (LTCG + STCG + Section_1212_b_Amount))

# Check to see whether the capital loss carryforwards as prescribed
# by the statute meet the informal statement that unused capital losses
# are carried forward. This does not require that there be a net capital loss.
fr.check_equivalence(s, statute_carryover_total,
                     unused_capital_losses, "Carryforward unused losses")

# Check to see whether the capital loss carryforwards as prescribed by
# the statute meet the informal statement that unused capital losses are
# carried forward. This does require that there be a net capital loss--
# as the statute requires.
fr.check_equivalence(s, statute_carryover_total_actual, unused_capital_losses,
                     "Carryforward unused losses require Net Capital Loss")

# These are the worksheet prescriptions for what to carry over.
worksheet_carryover_short = fr.excess_of(
    NSTCL, (NLTCG + Section_1212_b_Amount))
worksheet_carryover_long = fr.excess_of(
    NLTCL, (NSTCG + fr.excess_of(Section_1212_b_Amount, NSTCL)))


# This checks to see whether what the statute says to carry over
# and what the worksheet says to carry over are the same.
# It does not include the requirement that there be a net capital loss.
fr.check_equivalence(s, statute_carryover_long,
                     worksheet_carryover_long, "Statute v. Worksheet Long")

fr.check_equivalence(s, statute_carryover_short,
                     worksheet_carryover_short, "Statute v. Worksheet Short")


# This checks to see whether what the statute says to carry over
# and what the worksheet says to carry over are the same.
# It DOES include the requirement that there be a net capital loss.
fr.check_equivalence(s, statute_carryover_long_actual,
                     worksheet_carryover_long,
                     "Statute v. Worksheet Long require Net Capital Loss")

fr.check_equivalence(s, statute_carryover_short_actual,
                     worksheet_carryover_short,
                     "Statute v. Worksheet Short require Net Capital Loss")
