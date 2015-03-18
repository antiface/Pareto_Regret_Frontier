'''
This will be a personal library for various Pareto Regret functions that will be of use. This way, I
avoid having to do a ton of algebra, which is susceptible to mistakes. All arrays/matrices here
should be considered as NUMPY arrays/matrices.

(c) March 2015 by Daniel Seita
'''

import numpy as np

'''
A simple factorial function. Yes, I know that "raise Exception(...)" is bad practice...
'''
def factorial(n):
    if n < 0:
        raise Exception("Invalid input for factorial, n = " + str(n))
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)

'''
An n-choose-k that also deals with a special case where we have (n choose -1)s from Theorem 6.
'''
def nchoosek(n, k):
    if k == -1:
        if n == -1:
            return 1
        else:
            return 0
    else:
        return factorial(n) / (factorial(n-k) * factorial(k))

'''
The f_T(i) formula Wouter presented in Theorem 6. Here, i is the vertex index.
'''
def fT_formula(i, T):
    sum = 0
    for j in range(1,i+1):
        sum += (j * (2**(j-T)) * nchoosek(T-j-1,T-i-1))
    return sum

'''
Given two or three points, returns their convex combination. The third point is optional. The points
can be either probability weight vectors or points in 3-D space that are being tested.
'''
def convex_combo(point1, point2, point3=None):
    if point3 is None:
        return (1.0/2) * (point1 + point2)
    else:
        return (1.0/3) * (point1 + point2 + point3)

'''
Given a 3-D point (r_0,r_1,r_2), and a probability weight vector (p_0,p_1,p_2), determine the six
vectors the adversary could play to make the point "closer" to the origin. The third argument can be
set False if one wishes to suppress the default printing.
'''
def get_six_points(point, weights, print_info=True):
    (r0,r1,r2) = (point[0],point[1],point[2])
    (p1,p2) = (weights[1],weights[2])
    point1 = np.array([ r0 - (p1+p2), r1 - ((p1-1)+p2), r2 - (p1+(p2-1)) ])
    point2 = np.array([ r0 - (-p1),   r1 - (-(p1-1)),   r2 - (-p1) ])
    point3 = np.array([ r0 - (-p2),   r1 - (-p2),       r2 - (-(p2-1)) ])
    point4 = np.array([ r0 + (p1+p2), r1 + ((p1-1)+p2), r2 + (p1+(p2-1)) ])
    point5 = np.array([ r0 + (-p1),   r1 + (-(p1-1)),   r2 + (-p1) ])
    point6 = np.array([ r0 + (-p2),   r1 + (-p2),       r2 + (-(p2-1)) ])
    if print_info:
        print ""
        print "Using loss vector <0,1,1>, we get " + str(point1) 
        print "Using loss vector <1,0,1>, we get " + str(point2)
        print "Using loss vector <1,1,0>, we get " + str(point3)
        print "Using loss vector <1,0,0>, we get " + str(point4)
        print "Using loss vector <0,1,0>, we get " + str(point5)
        print "Using loss vector <0,0,1>, we get " + str(point6)
        print ""
    return [point1,point2,point3,point4,point5,point6]

'''
Given a 3-D point (r_0,r_1,r_2), tests to see this position relative to the \mathbb{G}_{T=1}
frontier. Possible return values are (1) on it (i.e., an optimal point with respect to the player),
(2) beyond it (i.e., impossible) or (3) before it (i.e., feasible but suboptimal). To make it
explicit, we return the following three strings: "optimal", "impossible", or "suboptimal".

NOTE I am testing an epsilon here of around 1e-6 in case rounding errors occur.

NOTE This is for a single point. Do not input a list of points.
'''
def position_t1(point):
    epsilon = 1e-5
    (r0,r1,r2) = (point[0],point[1],point[2])
    if r0 < 0 or r1 < 0 or r2 < 0:
        return "Impossible" # An easy case
    if r0 > 2./3 and r1 > 2./3 and r2 > 2./3:
        return "Suboptimal" # A bit redundant but I guess it doesn't hurt
    if r0 <= 1 and r1 <= 1 and r2 <= 1:
        # This case we are contained in the cube that contains the triangular plane at x+y+z=2.
        summ = r0 + r1 + r2
        if (summ > (2 - epsilon)) and (summ < (2 + epsilon)):
        #if summ == 2:
            return "Optimal"
        elif summ > 2:
            return "Suboptimal"
        else:
            return "Impossible"
    else:
        # Now we could be in any of the three other blocks. They are symmetric.
        if r0 >= 1:
            # Case of plane y + z = 1
            summ = r1 + r2
        elif r1 >= 1:
            # Case of plane x + z = 1
            summ = r0 + r2
        else:
            # Case of plane x + y = 1
            summ = r0 + r1
        if (summ > (1 - epsilon)) and (summ < (1 + epsilon)):
        #if summ == 1:
            return "Optimal"
        elif summ > 1:
            return "Suboptimal"
        else:
            return "Impossible"


