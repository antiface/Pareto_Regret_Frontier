'''
This is the Pareto Regret Frontier for two experts.

Edit: I'm now using this code to plot the 3-D frontier with one expert.

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
    xx, yy = np.meshgrid(np.linspace(1,3,10), np.linspace(0,1,10))
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


########
# MAIN #
########

# To make it simple, we manually choose which task we want to do here.
brute_force_t1 = True
brute_force_t2 = False
plot_3d_frontier = False
plot_2d_frontier = False

# Find \mathbb{G}_{T=1} by brute-force simulation. A useful warm-up/test for the harder stages.
if brute_force_t1:
    print "Now attempting to find \mathbb{G}_{T=1} by brute-force simulation..."
    num = 50
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
    x_coordinates = [point[0] for point in optimal]
    y_coordinates = [point[1] for point in optimal]
    z_coordinates = [point[2] for point in optimal]
    plt3d.scatter(x_coordinates, y_coordinates, z_coordinates)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()


# Attempts to find \mathbb{G}_{T=2} by brute-force simulation, so have coordinates in [0,2].
# Remember that the points in the mesh grid are NOT the actual points we want to sample. These are
# the raw points with two rounds left. For each of these points, then, we must assign an optimal
# probability vector. Then 
if brute_force_t2:
    print "Now attempting to find \mathbb{G}_{T=2} by brute-force simulation..."
    impossible = []
    suboptimal = []
    optimal = []
    num = 100
    xx,yy,zz = np.meshgrid(np.linspace(0,2,num), np.linspace(0,2,num), np.linspace(0,2,num))
    x_coords,y_coords,z_coords = (xx.ravel(), yy.ravel(), zz.ravel())
    num_points = len(x_coords)
    print "We must iterate through " + str(num_points) + " simulated points ... "
    for i in range(num_points):
        p = (x_coords[i], y_coords[i], z_coords[i])

        # TODO Assign raw probability vector! Once we have that, then it's easy, because we call
        # par.get_six_points(...,...) to find where the adversary could send it. If ANY of the six
        # points are impossible, the point overall is impossible. If none are impossible, then check
        # if ANY of the six points are OPTIMAL. If so, the overall point is optimal and belongs on
        # the boundary of \mathbb{G}_{T=2}. If ALL SIX are suboptimal, then the point overall is
        # suboptimal because we could therefore always decrease one of its components by epsilon and
        # we would still be safe.

        # So, the main challenge is to find the correct probability weight vector, and this I
        # believe will require some clever convex combination of certain probabilities. Also, we may
        # (as I mentioned in that code) need to make it work for a certain epsilon tolerance since
        # we may have +/- 0.00001-ish errors due to rounding and floating point arithmetic.

        # NOTE: this is not correct. It was only for experimentation.
        '''
        result = par.position_t1(p)
        if result == "Impossible":
            impossible.append(p)
        elif result == "Suboptimal":
            suboptimal.append(p)
        else:
            optimal.append(p)
        '''
    print "\nFirst, the impossible points:"
    print impossible
    print "\nNow the suboptimal points:"
    print suboptimal
    print "\nNow the optimal points:"
    print optimal


# Plot the G_{T=1} frontier by going through each of the planes and getting their meshgrids and z's
if plot_3d_frontier:
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


# The following is old code that can reproduce Wouter's plot of the 2-D Pareto Regret frontier.
if plot_2d_frontier:
    if len(sys.argv) != 2:
        print "Usage: python pareto_two_dim.py <max_T>"
        sys.exit(-1)
    max_T = int(sys.argv[1])
    for T in range(0,max_T+1):
        values = [pareto.fT_formula(i,T) for i in range(0,T+1)]
        plt.plot(values, values[::-1])
    plt.show()




