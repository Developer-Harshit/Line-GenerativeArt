import pygame


# to remap from (ti,tf) to (si,sf)
def alpha_screen(width, height, alpha=10, color=(0, 0, 0)):
    screen = pygame.Surface((width, height))
    screen.fill(color)
    screen.set_alpha(alpha)
    return screen


def remap(value, ti, tf, si, sf):
    result = ((value - ti) * (sf - si) / (tf - ti)) + si
    return result


def lerp(a, b, t):
    return a + (b - t) * t


# p0,p1,p2
def bezier(p0, p1, p2, t):
    x = ((1 - t) ** 2 * p0[0]) + (2 * (1 - t) * t * p1[0]) + (t * t * p2[0])
    y = ((1 - t) ** 2 * p0[1]) + (2 * (1 - t) * t * p1[1]) + (t * t * p2[1])
    return (x, y)


# (1-t)**2 p0[0] + 2*(1-t) *t*p1[0] + t**2*p2[0]
def get_curve(points, inc=0.1):
    pt_len = len(points)

    extra_points = [points[pt_len - 1]] * 2
    control_points = points  # + extra_points

    curve = []
    for i in range(0, pt_len - 1, 2):
        p0 = control_points[i]
        p1 = control_points[i + 1]
        p2 = control_points[i + 2]
        t = 0
        while t < 1:
            new_point = bezier(p0, p1, p2, t)
            curve.append(new_point)
            if (
                new_point[0] == control_points[-1][0]
                and new_point[1] == control_points[-1][1]
            ):
                break
            t += inc

    return curve


# p0 = [0, 0]
# p1 = [2, 6]
# p2 = [4, 7]
# p3 = [9, 10]
# p4 = [10, 23]
# get_curve([p0, p1, p2, p3, p4])
