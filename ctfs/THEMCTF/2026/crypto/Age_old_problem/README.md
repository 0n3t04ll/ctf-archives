De Jurist

In the age of AI, we found this old unsolved problem at math.stackexchange, thankfully they have provided us a nice way to construct this relation, we're only missing a solution, solve it!

Hint: The runtime for the solver is a couple seconds

A slight note for Age* old problem, the chall.py used a more optimized version to generate the current instance, corrected find_c2_d2:

def find_c2_d2(c1: int, d1: int): """ Find integers (c2, d2) such that c1*c2 - d1*d2 == 1. """ if gcd(c1, d1) != 1: raise ValueError c2 = pow(c1, -1, d1) d2 = (c1 * c2 - 1) // d1 if d2 % 2 != 0: c2 += d1 d2 += c1 assert c1 * c2 - d1 * d2 == 1 assert d2 % 2 == 0 return c2, d2
NOTE: This does not impact the solve as the solve works for both versions, this only impacts the generation for the output.txt. It also seems unlikely that a solution exists for the old generation, but not for this one (or the other way around). So this should not impact progress
