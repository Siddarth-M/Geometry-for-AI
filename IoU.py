"""
Given two 2D polygons write a function that calculates the IoU of their areas,
defined as the area of their intersection divided by the area of their union.
The vertices of the polygons are constrained to lie on the unit circle and you
can assume that each polygon has at least 3 vertices, given and in sorted order.

- You are free to use basic math functions/libraries (sin, cos, atan2, numpy etc)
  but not geometry-specific libraries (such as shapely).
- You are free to look up geometry-related formulas, optionally copy paste in
  short code snippets and adapt them to your needs.
- We do care and evaluate your general code quality, structure and readability
  but you do not have to go crazy on docstrings.
"""
from functools import reduce
import operator
import math


def area_poly(poly1):  # Finding area of the polygon using the endpoints

    area = 0.0
    n = len(poly1)
    j = n - 1
    for i in range(0, n):
        area += (poly1[j][0] + poly1[i][0]) * (poly1[j][1] - poly1[i][1])
        j = i
    return abs(area / 2.0)
    # THe above is called the shoelace formula


def line_intersection(line1, line2):
    a_first = line1[0][0]   # x 1
    b_first = line1[1][0]   # x 2

    a_second = line1[0][1]  # y 1
    b_second = line1[1][1]  # y 2

    c_first = line2[0][0]   # x 3
    d_first = line2[1][0]   # x 4
    c_second = line2[0][1]  # y 3
    d_second = line2[1][1]  # y 4

    x_1 = a_first
    x_2 = b_first
    y_1 = a_second
    y_2 = b_second
    x_3 = c_first
    x_4 = d_first
    y_3 = c_second
    y_4 = d_second

    a_one=((x_4-x_3)*(y_1-y_3)-(y_4-y_3)*(x_1-x_3))
    a_two=((y_4-y_3)*(x_2-x_1)-(x_4-x_3)*(y_2-y_1))

    if a_one == 0 and a_two == 0:
        return []
    if a_two == 0 and a_one is not 0:
        return []
    else:
        s_a=a_one/a_two

    b_one=(x_2-x_1)*(y_3-y_1)-(y_2-y_1)*(x_3-x_1)
    b_two=(y_2-y_1)*(x_4-x_3)-(x_2-x_1)*(y_4-y_3)
    if b_one == 0 and b_two == 0:
        return []
    if b_two == 0 and b_one is not 0:
        return []
    else:
        s_b=b_one/b_two

    #s_b = ((x_2-x_1)*(y_3-y_1)-(y_2-y_1)*(x_3-x_1))/((y_2-y_1)*(x_4-x_3)-(x_2-x_1)*(y_4-y_3))
    #s_b = b_one / b_two
    a1 = b_second - a_second
    b1 = a_first - b_first
    c1 = a1 * a_first + b1 * a_second
    a2 = d_second - c_second
    b2 = c_first - d_first
    c2 = a2 * c_first + b2 * (c_second)

    determinant = a1 * b2 - a2 * b1

    if (determinant == 0):
        return []
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        #if s_a >= 0 and s_a <= 1 and s_b >= 0 and s_b <= 1:
        if s_a >= 0 and s_a <= 1 and s_b>=0 and s_b<=1:
            return x,y
        else:
            return []
def iou(poly1, poly2):
    # your code here
    # To find the area of intersection and the total area, I first find the area of the given polygons
    # IOU = Area of intersection / Area of Polygon 1 + Area of Polygon 2 - Area of intersection

    # We have to find the intersection points
    int_points = []
    len1 = len(poly1)
    # print(len1)
    len2 = len(poly2)
    # print(len2)
    i = len1 - 1
    j = len2 - 1
    for t in range(0, len1):
        line1 = (poly1[t], poly1[i])
        i = t
        # print("in iou outer loop")
        # print(line1,i)
        for u in range(0, len2):
            line2 = (poly2[u], poly2[j])
            j = u
            # print("In iou inner loop")
            # print(line2,j)
            if line1 is line2:
                int_points.append(line1[0], line1[1])
            temp = line_intersection(line1, line2)
            if len(temp) is not 0:
                int_points.append(temp)
            # print("int point")
            # print(int_points)
    if len(int_points) <= 2:  # in these cases,there is no intersection area
        return 0
    # Copied partially and adapted from Stack exchange for ordering the points
    # Now for intersection area - Ordering the points according to angle
    center = tuple(
        map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), int_points), [len(int_points)] * 2))
    int_points1 = (sorted(int_points, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360))
    int_area = area_poly(int_points1)

    p1_area = area_poly(poly1)  # Area of polygon 1 found here
    # print("P1 area",p1_area)
    p2_area = area_poly(poly2)  # Area of polygon 2 found above
    # print("P2 area",p2_area)
    union_area = p1_area + p2_area - int_area
    iou = int_area / union_area  # The required area
    # print("iou",iou)
    return iou


# --------------------------------------------------------

if __name__ == "__main__":

    cases = []
    """
    # Case 1: a vanilla case (see https://imgur.com/a/dSKXHPF for a diagram)
    poly1 = [
        (0, 1),
        (2, 1),
        (1, 0),
    ]
    poly2 = [
        (0, 0),
        (1, 2),
        (2, 1),
    ]
    cases.append((poly1, poly2, "simple case", 0.5))
    """
    # Case 2: another simple case
    poly1 = [
        (1, 0),
        (0, 1),
        (-0.7071067811865476, -0.7071067811865476),
    ]
    
    poly2 = [
        (-0.1736481776669303, 0.984807753012208),
        (-1, 0),
        (0, -1),
    ]
    cases.append((poly1, poly2, "simple case 2", 0.1881047657147776))
    # Case 3: yet another simple case, note the duplicated point
    poly1 = [
        (0, -1),
        (-1, 0),
        (-1, 0),
        (0, 1),
    ]
    poly2 = [
        (0.7071067811865476, 0.7071067811865476),
        (-0.7071067811865476, 0.7071067811865476),
        (-0.7071067811865476, -0.7071067811865476),
        (0.7071067811865476, -0.7071067811865476),
        (0.7071067811865476, -0.7071067811865476),
    ]
    cases.append((poly1, poly2, "simple case 3", 0.38148713966109243))

    # Case 4: shared edge
    poly1 = [
        (-1, 0),
        (-0.7071067811865476, -0.7071067811865476),
        (0.7071067811865476, -0.7071067811865476),
        (1, 0),
    ]
    poly2 = [
        (0, 1),
        (-1, 0),
        (1, 0),
    ]
    cases.append((poly1, poly2, "shared edge", 0.0))

    # Case 5: same polygon
    poly1 = [
        (0, -1),
        (-1, 0),
        (1, 0),
    ]
    poly2 = [
        (0, -1),
        (-1, 0),
        (1, 0),
    ]
    cases.append((poly1, poly2, "same same", 1.0))

    # Case 6: polygons do not intersect
    poly1 = [
        (-0.7071067811865476, 0.7071067811865476),
        (-1, 0),
        (-0.7071067811865476, -0.7071067811865476),
    ]
 
    poly2 = [
        (0.7071067811865476, 0.7071067811865476),
        (1, 0),
        (0.7071067811865476, -0.7071067811865476),
    ]
    cases.append((poly1, poly2, "no intersection", 0.0))

    import time

    t0 = time.time()

    for poly1, poly2, description, expected in cases:
        computed = iou(poly1, poly2)
        print('-' * 20)
        print(description)
        print("computed:", computed)
        print("expected:", expected)
        print("PASS" if abs(computed - expected) < 1e-8 else "FAIL")

    # details here don't matter too much, but this shouldn't be seconds
    dt = (time.time() - t0) * 1000
    print("done in %.4fms" % dt)
