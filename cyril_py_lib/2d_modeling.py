import numpy as np
from scipy.sparse import diags as dig
from scipy.sparse import csc_matrix, linalg as sla
from matplotlib import pyplot as plt


def test_plot():
    """
    Test matplotlib: plot anything
    :return: nothing, opens a plot in new window
    """
    plt.plot([1, 2, 3], [2, 3, 2])
    plt.show()


def test_random_bitmap():
    """
    Function to test how hard it is to make and plot a grid with "pixels"
    :return: nothing, opens a plot in new window
    """
    grid = np.array([np.random.rand(4), np.random.rand(4), np.random.rand(4), np.random.rand(4)])
    print("Test grid: (size: {}, type{})\n{}".format(grid.size, type(grid), grid))
    plt.imshow(grid)
    plt.colorbar()
    plt.show()


def test_heatmap(n=100, m=None):
    """
    Function to test plt pixel grid display.
    :param n: Nr of pixels (in x and y if 'm' is undefined)
    :param m: Nr of pixels in y
    :return: Nothing, opens a plot in new window.
    """
    m = n if m is None else m
    plt.imshow(np.random.random((m, n)), cmap="Blues")
    plt.colorbar()
    plt.show()


def test_single_point_random_gradient():
    """
    Function to display "glooming" point (later: radiation point/source)
    :return: Nothing, opens a plot in new window.
    """
    grid = np.ones((100, 100))
    grid[50, 50] = 10
    # plot_grid(grid)
    updated_grid = update_grid(grid)
    plot_grid(updated_grid)
    print(updated_grid)


def plot_grid(grid, origin="lower", **kwargs):
    """
    Function to plot a grid
    :param origin: how the image should be oriented
    :param grid: 2d array to be plotted
    :return: nothing, opens a plot in new window
    """
    plt.imshow(grid, cmap="afmhot", origin=origin, **kwargs)
    plt.colorbar()
    plt.show()


def update_grid(grid):
    x_st = 50
    y_st = 50
    pth = [(x_st, y_st)]  # points to handle
    t = 0
    while t < 10:
        pth_next = []
        for pt in pth:
            neighs = ngbs(pt)
            for n in neighs:
                try:
                    grid[n] = grid[pt]-0.5
                    pth_next.append(n)
                except IndexError:
                    continue
        t += 1
        pth = pth_next
        pth.append((x_st, y_st))
        grid[x_st, y_st] = 10
    return grid


def ngbs(point):
    return (point[0], point[1]-1), (point[0]+1, point[1]), (point[0], point[1]+1), (point[0]-1, point[1])


def test_drawing_grid_by_brain():
    x_max, y_max = 100, 50
    grid = np.zeros((y_max, x_max))
    grid[20, 40] = 3
    for j in range(y_max):
        for i in range(x_max):
            if j == 2 or j == y_max-3 or i == 20 or i == x_max-3:
                grid[j, i] = 2
            if i == 70 and j < 35:
                grid[j, i] = 1
    plot_grid(grid, origin='lower')


def factory_simple_grid():
    x_max, y_max = 100, 50
    grid = np.ones((y_max, x_max))
    for j in range(y_max):
        for i in range(x_max):
            if j == 2 or j == y_max-3 or i == 10 or i == 11 or i == 12 or i == 13 or i == x_max-3:
                grid[j, i] = 200
            if i == 70 and j < 25:
                grid[j, i] = 200
            if i == 71 and j < 25:
                grid[j, i] = 200
    return grid


def test_grid_to_vector_and_back():
    grid = factory_simple_grid()
    plot_grid(grid)
    x, y = grid.shape
    vec = np.reshape(grid, x*y)
    vec[40+20*y] = 3
    plot_grid(np.reshape(vec, (x, y)))


def test_construct_diag(a):
    print(np.diag(a))
    print(dig([1], [-1], shape=(5,5)).todense())
    print(dig([1], [-1], shape=(5,5)))


def test_construct_sparce():
    x = np.arange(10)
    d = dig([1, 1, 2, 3], [-1, 1, 5, -5], shape=(len(x), len(x))).todense()
    np.fill_diagonal(d, x)
    print(d)


def test_principle_without_normalisation(s_x=60, s_y=10):
    grid = factory_simple_grid()
    # plot_grid(grid)
    n_x, n_y = grid.shape
    source_x = s_x
    source_y = s_y
    source_strength = 1

    # initialise vecotrs
    F = np.zeros(n_x*n_y)
    F[source_y*n_x + source_x] = source_strength
    dic_vector = np.reshape(grid, n_x*n_y)

    # construct matrix
    A = dig([1, 1, 1, 1], [-1, 1, n_x, -1*n_x], shape=(len(dic_vector), len(dic_vector))).todense()
    np.fill_diagonal(A, dic_vector)

    # solve linear system
    lu = sla.splu(csc_matrix(A))
    x = lu.solve(F)

    plt.imshow(np.reshape(x, (n_x, n_y)), origin="lower", cmap="PuOr")
    plt.colorbar()
    plt.show()


def solver(s_x=50, s_y=25):
    # construct grid
    x_max, y_max = 100, 50  # nr of pixels (taken to be 10cm each)
    delta_x = 0.1  # taken to be 10cm = 0.1m
    omega = 5200 * 10**6  # Hz (?)
    c = 3 * 10**9  # speed of light in m/s

    sigma_air = 10**(-12)  # conductivity in Simens/meter
    sigma_wood = 10**(-3)  # conductivity in Simens/meter
    mu_air = 1.25663753 * 10**(-6)  # permeability in Henry/meter
    mu_concrete = 1.2566371 * 10**(-6)  # permeability in Henry/meter
    alpha_air = sigma_air * mu_air
    alpha_other = sigma_wood * mu_concrete

    beta = delta_x * omega / c

    air_const = (beta**2 - 4 - delta_x**2*omega*alpha_air)
    solid_const = (beta**2 - 4 - delta_x**2*omega*alpha_other)

    grid = np.ones((y_max, x_max)) * air_const

    construct_walls = True
    if construct_walls:
        for j in range(y_max):
            for i in range(x_max):
                if j == 2 or j == y_max-3 or i == 10 or i == 11 or i == 12 or i == 13 or i == x_max-3:
                    grid[j, i] = solid_const
                if i == 70 and j < 25:
                    grid[j, i] = solid_const
                if i == 71 and j < 25:
                    grid[j, i] = solid_const

    plot_grid(grid)
    n_x, n_y = grid.shape
    source_x = s_x
    source_y = s_y
    source_strength = -(delta_x**2)*1  # normalisation doesn't influence the shape (as it should)

    # ##########################################   SOLVER   ######################################################
    # initialise vecotrs
    F = np.zeros(n_x*n_y)
    F[source_y*n_x + source_x] = source_strength
    dic_vector = np.reshape(grid, n_x*n_y)

    # construct matrix
    A = dig([1, 1, 1, 1], [-1, 1, n_x, -1*n_x], shape=(len(dic_vector), len(dic_vector))).todense()
    np.fill_diagonal(A, dic_vector)

    # solve linear system
    lu = sla.splu(csc_matrix(A))
    x = lu.solve(F)
    reshaped = np.reshape(x, (n_x, n_y))
    # ##########################################   SOLVER   ######################################################

    plt.imshow(reshaped, origin="lower", cmap="PuOr")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    print("running: "+str(__file__))
    for x in [10, 30, 60, 90]:
        for y in [10, 40]:
            # solver(x, y)
            print(x, y)
    solver()
    # test_single_point_random_gradient()
    # test_drawing_grid_by_brain()
    # test_grid_to_vector_and_back()
    # test_construct_sparce()
    """
    test_principle_without_normalisation(30, 10)
    test_principle_without_normalisation(50, 10)
    test_principle_without_normalisation(90, 10)
    test_principle_without_normalisation(30, 30)
    test_principle_without_normalisation(50, 30)
    test_principle_without_normalisation(90, 30)
    test_principle_without_normalisation(10, 45)
    test_principle_without_normalisation(70, 45)
    test_principle_without_normalisation(90, 45)
    """
