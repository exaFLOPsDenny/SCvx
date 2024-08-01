import matplotlib.pyplot as plt
import random

class Voronoi:
    def __init__(self):
        self.eps = 2**-23

    def compute(self, sites, pad):  # pad: box padding
        boundary = self.points_boundary(sites)

        x_left = boundary[0] - pad   # min x
        y_bottom = boundary[1] - pad # min y
        x_right = boundary[2] + pad  # max x
        y_top = boundary[3] + pad    # max y

        sites = self.preprocess_sites(sites)

        n = len(sites)

        voronoi_box = [
            [x_left, y_top], [x_right, y_top],
            [x_right, y_bottom], [x_left, y_bottom]
        ]

        cells = []  # output

        for i in range(n):
            cell = voronoi_box.copy()
            current_site = sites[i]

            for j in range(n):
                if i == j:
                    continue

                m = len(cell)
                new_cell = []
                next_site = sites[j]
                bisector = self.two_points_bisector(current_site, next_site)

                if bisector[0] == 0 and bisector[1] == 0:
                    continue

                for k in range(m):
                    current_vertex = cell[k]
                    next_vertex = cell[(k + 1) % m]
                    first_intersection = self.line_and_segment_intersection(bisector, current_vertex, next_vertex)

                    if first_intersection:
                        intersection_is_next_vertex = (first_intersection[0] == next_vertex[0]) and (first_intersection[1] == next_vertex[1])

                        if intersection_is_next_vertex:
                            new_cell.extend([next_vertex, cell[(k + 2) % m]])
                            first_intersection_index = (k + 2) % m
                        else:
                            new_cell.extend([first_intersection, next_vertex])
                            first_intersection_index = (k + 1) % m

                        break

                if not new_cell:
                    new_cell = cell
                else:
                    for k in range(first_intersection_index, m):
                        current_vertex = cell[k]
                        next_vertex = cell[(k + 1) % m]
                        second_intersection = self.line_and_segment_intersection(bisector, current_vertex, next_vertex)

                        if second_intersection:
                            new_cell.append(second_intersection)
                            second_intersection_index = k + 1
                            break
                        else:
                            new_cell.append(next_vertex)

                    if not self.is_point_in_polygon(current_site, new_cell):
                        new_cell = [] if self.two_points_equal(second_intersection, cell[second_intersection_index % m]) else [second_intersection]

                        for k in range(second_intersection_index, m):
                            v1 = cell[k % m]
                            v2 = cell[(k + 1) % m]

                            if self.two_points_equal(v1, v2):
                                continue

                            new_cell.append(v1)

                        if not self.two_points_equal(first_intersection, v1):
                            new_cell.append(first_intersection)

                cell = new_cell

            cells.append(cell if cell else None)

        return {'sites': sites, 'cells': cells}

    def preprocess_sites(self, sites):
        # REMOVE REPEATED POINTS
        new_sites = list({tuple(x): x for x in sites}.values())

        # THIS MAY HELP WITH FLOATING POINTS ISSUES
        magnitude = self.max_xy(new_sites)
        mag_x = self.eps * magnitude[0] * 100
        mag_y = self.eps * magnitude[1] * 100

        for i in range(len(new_sites)):
            new_sites[i][0] += random.uniform(0, mag_x)
            new_sites[i][1] += random.uniform(0, mag_y)

        return new_sites

    def max_xy(self, points):
        x = abs(points[0][0])
        y = abs(points[0][1])

        for point in points[1:]:
            x1 = abs(point[0])
            y1 = abs(point[1])

            if x1 > x:
                x = x1
            if y1 > y:
                y = y1

        x = max(x, 1)
        y = max(y, 1)

        return [x, y]

    def two_points_equal(self, a, b):
        return (a[0] == b[0]) and (a[1] == b[1])

    def points_boundary(self, points):
        min_x = max_x = points[0][0]
        min_y = max_y = points[0][1]

        for x, y in points[1:]:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        return [min_x, min_y, max_x, max_y]

    def two_points_bisector(self, A, B):  # ax + by + c = 0
        midpoint = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2]
        a = B[0] - A[0]
        b = B[1] - A[1]
        c = -midpoint[0] * a - midpoint[1] * b
        return [a, b, c]

    def isclose(self, a, b, tolerance=None):
        if tolerance is None:
            tolerance = self.eps
        return abs(a - b) < tolerance

    def cross_prod(self, a, b):  # a, b: 3D vectors (arrays)
        s1 = a[1] * b[2] - a[2] * b[1]
        s2 = a[2] * b[0] - a[0] * b[2]
        s3 = a[0] * b[1] - a[1] * b[0]
        return [s1, s2, s3]

    def line_and_segment_intersection(self, line, A, B):  # intersection between line and segment AB
        a = A[1] - B[1]
        b = B[0] - A[0]
        c = A[0] * B[1] - B[0] * A[1]
        AB_line = [a, b, c]  # ax + by + c = 0

        if (b == 0 or line[1] == 0) or (self.isclose(b, 0) or self.isclose(line[1], 0)):
            return None

        if (a / b == line[0] / line[1]) and (c / b == line[2] / line[1]):
            return None

        p = self.cross_prod(line, AB_line)

        if p[2] == 0:  # the lines do not intersect
            return None
        else:
            intersection = [p[0] / p[2], p[1] / p[2]]

            is_vertical = self.isclose(A[0], B[0])  # AB is "vertical"
            is_horizontal = self.isclose(A[1], B[1])  # AB is "horizontal"
            is_endpoint_y = self.isclose(intersection[1], A[1]) or self.isclose(intersection[1], B[1])  # intersection is an endpoint
            is_endpoint_x = self.isclose(intersection[0], A[0]) or self.isclose(intersection[0], B[0])  # intersection is an endpoint
            is_between_x_axis = (intersection[0] < A[0]) != (intersection[0] < B[0])  # intersection is between AB x-axis
            is_between_y_axis = (intersection[1] < A[1]) != (intersection[1] < B[1])  # intersection is between AB y-axis
            is_between_AB = is_between_x_axis and is_between_y_axis  # intersection is between AB

            if is_vertical and (is_endpoint_y or is_between_y_axis):
                return intersection
            elif is_horizontal and (is_endpoint_x or is_between_x_axis):
                return intersection
            elif is_between_AB:
                return intersection
            else:
                return None

    def cross_2D(self, u, v):
        return u[0] * v[1] - u[1] * v[0]

    def is_point_in_polygon(self, point, polygon):  # convex polygon
        n = len(polygon)

        for i in range(n):
            t = [polygon[i][0] - polygon[(i + 1) % n][0], polygon[i][1] - polygon[(i + 1) % n][1]]
            u = [point[0] - polygon[(i + 1) % n][0], point[1] - polygon[(i + 1) % n][1]]
            v = [polygon[(i + 2) % n][0] - polygon[(i + 1) % n][0], polygon[(i + 2) % n][1] - polygon[(i + 1) % n][1]]

            if not (self.cross_2D(t, u) * self.cross_2D(t, v) >= 0 and self.cross_2D(v, u) * self.cross_2D(v, t) >= 0):
                return False

        return True

# Usage
points = [[1, 3], [2, 2], [3, 4], [2, 1]]
padding = 0.5

voronoi = Voronoi()
my_diagram = voronoi.compute(points, padding)

sites = my_diagram['sites']
cells = my_diagram['cells']

# Plotting
def plot_voronoi(sites, cells):
    fig, ax = plt.subplots()
    for cell in cells:
        if cell:
            polygon = plt.Polygon(cell, fill=None, edgecolor='r')
            ax.add_patch(polygon)
    xs, ys = zip(*sites)
    plt.scatter(xs, ys, color='b')
    plt.xlim(min(xs) - 1, max(xs) + 1)
    plt.ylim(min(ys) - 1, max(ys) + 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

plot_voronoi(sites, cells)
