'''
This is the Pareto Regret Frontier for two experts.
Update: I'm now using this code to plot the 3-D frontier with one expert.

(c) March 2015 by Daniel Seita
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pareto_functions as par
import sys

'''
Computes the first plane for G_{T=1} which is the one where x+y+z=2. A plane is a*x+b*y+c*z+d=0,
[a,b,c] is the normal. Thus, we calculate d and we're set. We create a mesh grid and calculate the
corresponding z for all the (x,y) pairs in it.

It's tricky because this really only works with triangular meshes, which doesn't make it easy to
input it into the 3-d plotting functions, so I used the plot_trisurf function. This way, I can
manually put in the minimum amount of points, and it will plot it! (Putting in more will result in
triangles appearing.) I actually find the triangular surfacing easier than "normal" plotting.
'''
def plane_one():
    point = np.array([2./3, 2./3, 2./3])
    normal = np.array([1, 1, 1])
    d = -point.dot(normal)
    xx = np.array([0,1,1])
    yy = np.array([1,0,1])
    z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]
    return (xx, yy, z)

'''
Computes the second plane for G_{T=1} which is the triangular prism-like one over the x-axis. Or we
can swap the output to generate a plane in a different direction.
'''
def plane_two():
    point = np.array([1, 0.5, 0.5])
    normal = np.array([0, 1, 1])
    d = -point.dot(normal)
    xx, yy = np.meshgrid(np.linspace(1,2,10), np.linspace(0,1,10))
    z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]
    return (xx, yy, z)

'''
Given six points, returns either "Impossible", "Optimal", or "Suboptimal" for the case when we are
trying to find \mathbb{G}_{T=1} and our reference boundary is \mathbb{G}_{T=0}.
'''
def position_t0(points_list):
    for p in points_list:
        if p[0] < 0 or p[1] < 0 or p[2] < 0:
            return "Impossible"
    for p in points_list:
        if p[0] == 0 or p[1] == 0 or p[2] == 0:
            return "Optimal"
    return "Suboptimal"

'''
We'll manually put in some points to make plotting easier
'''
def simple_plot_tests():
    optimal = [np.array([2,.5,.5]),np.array([.5,2,.5]),np.array([.5,.5,2]), 
               np.array([2,2,0]),np.array([2,0,2]),np.array([0,2,2]),
               (1./99)*np.array([82,66,116]), 
               (1./99)*np.array([116,66,82]), 
               (1./99)*np.array([66,82,116]), 
               (1./99)*np.array([66,116,82]), 
               (1./99)*np.array([82,116,66]), 
               (1./99)*np.array([116,82,66]),]
    plt3d = plt.figure().gca(projection='3d')
    x_coordinates = [point[0] for point in optimal]
    y_coordinates = [point[1] for point in optimal]
    z_coordinates = [point[2] for point in optimal]
    plt3d.plot_trisurf(x_coordinates, y_coordinates, z_coordinates)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()

'''
Plot the G_{T=1} frontier by going through each of the planes and getting their meshgrids and z's
'''
def plot_3d_frontier():
    plt3d = plt.figure().gca(projection='3d')
    a,b,c = plane_one()
    plt3d.plot_trisurf(a,b,c)
    a,b,c = plane_two()
    plt3d.plot_surface(a,b,c)
    plt3d.plot_surface(b,a,c)
    plt3d.plot_surface(c,b,a)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()

'''
Find \mathbb{G}_{T=1} by brute-force simulation. A useful warm-up/test for the harder stages.
'''
def brute_force_t1():
    print "Now attempting to find \mathbb{G}_{T=1} by brute-force simulation..."
    num = 25
    (impossible,suboptimal,optimal) = ([],[],[])
    (basis0,basis1,basis2) = (np.array([0,1,1]), np.array([1,0,1]), np.array([1,1,0]))
    (c0,c1,c2) = np.meshgrid(np.linspace(0,1,num), np.linspace(0,1,num), np.linspace(0,1,num))
    (c0,c1,c2) = (c0.ravel(),c1.ravel(),c2.ravel())
    print "We must iterate through " + str(len(c0)) + " simulated points ... "
    # The case of i=0 is when all the components are zero.
    for i in range(1,len(c0)):
        if i % 100000 == 0:
            print "Now on point " + str(i)
        p = c0[i]*basis0 + c1[i]*basis1 + c2[i]*basis2
        w = np.array([c0[i], c1[i], c2[i]])
        w = w / np.sum(w)
        six_points = par.get_six_points(p, w, False)
        result = position_t0(six_points)
        if result == "Impossible":
            impossible.append(p)
        elif result == "Suboptimal":
            suboptimal.append(p)
        else:
            optimal.append(p)
    print "Number of impossible, suboptimal, and optimal points: {0}, {1}, {2}.".format(
        len(impossible),len(suboptimal),len(optimal))
    # Next step is to plot. There are several ways we can do this.
    plt3d = plt.figure().gca(projection='3d')
    x_coordinates = [point[0] for point in impossible]
    y_coordinates = [point[1] for point in impossible]
    z_coordinates = [point[2] for point in impossible]
    plt3d.plot_surface(x_coordinates, y_coordinates, z_coordinates)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()


'''
Given a list of 3-D points, we will augment the list by adding in all points that can be formed by
usin the same components. For instance, a list of:

[np.array([1,2,3]), np.array([1,1,1])]

Turns into:

[np.array([1,2,3]), np.array([2,1,3]), np.array([1,3,2]), np.array([3,2,1]), np.array([3,1,2]),
np.array([2,3,1]), np.array([1,1,1])]

This should be fine because if np.array([a,b,c]) is a valid point, then there exists a probability
vector. Now if the order of a,b,c, gets changed, we just change the probability vector accordingly.

Input: coordinates is a numpy array.
'''
def replicate(coordinates):
    result = [coordinates]
    r1,r2,r3 = coordinates[0],coordinates[1],coordinates[2]
    p2 = np.array([r1,r3,r2])
    if not any((p2 == x).all() for x in result):
        result.append(p2)
    p3 = np.array([r2,r1,r3])
    if not any((p3 == x).all() for x in result):
        result.append(p3)
    p4 = np.array([r2,r3,r1])
    if not any((p4 == x).all() for x in result):
        result.append(p4)
    p5 = np.array([r3,r1,r2])
    if not any((p5 == x).all() for x in result):
        result.append(p5)
    p6 = np.array([r3,r2,r1])
    if not any((p6 == x).all() for x in result):
        result.append(p6)
    return result


########
# MAIN #
########

# To make it simple, we manually choose which task we want to do here.
brute_force_t2 = True
simple_plot_tests = False
brute_force_t1 = False
plot_3d_frontier = False
if simple_plot_tests:
    simple_plot_tests()
if plot_3d_frontier:
    plot_3d_frontier()
if brute_force_t1:
    brute_force_t1()

# Attempts to find \mathbb{G}_{T=2} by brute-force simulation.
# Note: "optimal" starts with three known corner cases that this simulation will not capture
# Also, we only need c0 <= c1 <= c2 because the others can be found by swapping the components
if brute_force_t2:
    print "Now attempting to find \mathbb{G}_{T=2} by brute-force simulation..."
    impossible,suboptimal = [],[]
    optimal = [np.array([2,.5,.5]),np.array([.5,2,.5]),np.array([.5,.5,2]),
               np.array([0,2,2]),np.array([2,0,2]),np.array([2,2,0]),
               np.array([1.5,1.5,1./3]),np.array([1./3,1.5,1.5]),np.array([1.5,1./3,1.5])]
    (basis0,basis1,basis2) = (np.array([0,2,2]), np.array([2,0,2]), np.array([2,2,0]))
    rationals = par.generate_rationals(30, 1)
    print "There are a total of " + str(len(rationals)) + " possible values for a single basis... "
    points_tested = 0
    for first in range(0, len(rationals)):
        for second in range(first, len(rationals)):
            for third in range(second, len(rationals)):
                (c0,c1,c2) = (rationals[first],rationals[second],rationals[third])
                p = c0*basis0 + c1*basis1 + c2*basis2
                if np.sum(p) < 2:
                    continue
                w = np.array([c0, c1, c2])
                w = w / np.sum(w)
                six_points = par.get_six_points(p, w, False)
                points_tested += 1
                if points_tested % 250000 == 0:
                    print "Points tested: {}.".format(points_tested)
                done = False
                for s in six_points:
                    if par.position_t1(s) == "Impossible":
                        done = True
                        break
                if not done:
                    for s in six_points:
                        if par.position_t1(s) == "Optimal":
                            symmetrical_points = replicate(p)
                            for pt in symmetrical_points:
                                optimal.append(pt)
                            done = True
                            break
    print "Number of optimal points: {}.".format(len(optimal))
    print "Total points tested: {}".format(points_tested)
    f = open('known_points', 'w')
    for item in optimal:
        f.write(str(item) + '\n')
    f.close()
    # Next step is to plot. There are several ways we can do this.
    plt3d = plt.figure().gca(projection='3d')

    a,b,c = plane_one()
    plt3d.plot_trisurf(a,b,c,color='y')
    a,b,c = plane_two()
    plt3d.plot_surface(a,b,c,color='y')
    plt3d.plot_surface(b,a,c,color='y')
    plt3d.plot_surface(c,b,a,color='y')

    x_coordinates = [point[0] for point in optimal]
    y_coordinates = [point[1] for point in optimal]
    z_coordinates = [point[2] for point in optimal]
    plt3d.scatter(x_coordinates, y_coordinates, z_coordinates, c='k')
    #plt3d.plot_trisurf(x_coordinates, y_coordinates, z_coordinates)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()



