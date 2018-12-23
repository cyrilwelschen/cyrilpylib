import numpy as np
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


def plot_grid(grid, **kwargs):
    """
    Function to plot a grid
    :param grid: 2d array to be plotted
    :return: nothing, opens a plot in new window
    """
    plt.imshow(grid, cmap="afmhot", **kwargs)
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


if __name__ == "__main__":
    print("running: "+str(__file__))
    # test_single_point_random_gradient()
    test_drawing_grid_by_brain()
