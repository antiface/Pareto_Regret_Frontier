'''
This will be the REAL regret tradeoff profile for three experts, using expert 0/1 loss.
(c) April 2015 by Daniel Seita

This uses numpy and matplotlib to generate 3-D surface plots of the pareto regret frontier for 3
experts, using 0/1 expert loss, so the per-round loss is based on the player's probability weight
vector dotted with the adversary's loss vector. The adversary's loss vector's elements are in [0,1].

Usage:

python frontier.py <granularity>

where the granularity indicates how many points we want to plot. The code uses matplotlib's surface
mesh, so having more points increases the chances of getting "better", flatter surfaces, but
requires heavier computation. If no arguments are specified, then it defaults to granularity = 24.
'''

import numpy as np
import sys


########
# MAIN #
########

gran = 24
if len(sys.argv) == 3:
    gran = int(sys.argv[2])
if gran <= 0 or gran >= 100:
    print "Granularity of " + str(gran) + " would cause problems."
    sys.exit()

T = 1
# H[t][r0,r1] gives the minimum r2 (or NaN) for making <r0,r1,r2> optimal in t-round game.
H = [np.nan] # Putting NaN here as dummy first element
lossPatterns = np.array([[0,0,0],
                         [1,0,0],
                         [0,1,0],
                         [0,0,1],
                         [1,1,0],
                         [1,0,1],
                         [0,1,1]]) # Using <1,1,1> gives same result as <0,0,0> so ignore the former.

for t in range(1,T+1):
    print "Currently generating samples for round {}.\n".format(t)
    H.append(np.empty((gran*t+1, gran*t+1)) * np.nan)

    for r0 in range(1,gran*t+2):
        print "{0:.2f}%\r".format(100*float(r0-1)/(gran*t+1))
        # Can fill table in from symmetry TODO Check on when one of the elements is 0 ...
        H[t][r0, 1:r0-1] = H[t][1:r0-1, r0]

        for r1 in range(r0,gran*t+2):
            # Now find a (good) upper bound for r2 so we don't waste too much time searching.
            ubd = gran*t+1
            if r0 > 1:
                ubd = min(ubd, H[t][r0-1,r1])
            if r1 > 1:
                ubd = min(ubd, H[t][r0,r1-1])
            r2 = ubd

            # Now comes the challening part: finding the best <p0,p1,p2> for this <r0,r1,r2>.
            # We keep decrementing r2 until we hit a t-unrealizable triple.
            doneWithDecrements = False
            while not doneWithDecrements:
                realizable = False
                for p0 in range(0, gran+1):
                    for p1 in range(0, gran-p0+1):
                        p2 = gran-p0-p1
                        #print "<p0,p1,p2> = <{0},{1},{2}>".format(p0,p1,p2)

                        # First do an easy check if adversary can send any component negative
                        if ((r0-1) < p1+p2) or ((r1-1) < p0+p2) or ((r2-1) < p0+p1):
                            continue

                        # If t=1, then we already know we are safe
                        print "t = {}".format(t)
                        if t == 1:
                            realizable = True
                            break

                        # Efficiently compute 7 ways where adversary could "send" <r0,r1,r2>.
                        ix1 = np.tile(np.array([r0,r1,r2]), (7,1))
                        ix2 = gran*lossPatterns - np.tile(np.array(lossPatterns * [[p0],[p1],[p2]]), (1,3))
                        ix = ix1 - ix2
                        # TODO Not finished with this but I guess since this is only for T > 1...
                        # if (...) realizable=True, break

                    if realizable:
                        break

                # Still in while loop, but finished with looping through <p0,p1,p2>
                if not realizable: # This means we are at r2 = 0
                    doneWithDecrements = True
                else:
                    r2 = r2 - 1

            # Finished with while loop, have largest r2 that makes <r0,r1,r2> unrealizable
            if r2 == gran*t+1:
                H[t][r0,r1] = np.nan
            else:
                H[t][r0,r1] = r2+1 # Need next one up for being realizable

# Write to certain files
# Set up some plots, being sure to divide by 'gran' at the end!
for t in range(1,T+1):
    print "Not implemented yet"


print H[t]
