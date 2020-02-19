def area_poly(poly1):  # Finding area of the polygon using the endpoints

    area = 0.0
    n = len(poly1)
    j = n - 1
    for i in range(0, n):
        area += (poly1[j][0] + poly1[i][0]) * (poly1[j][1] - poly1[i][1])
        j = i
    return abs(area / 2.0)
    # The above is called the shoelace formula
    # REFER the link for more details: https://www.101computing.net/the-shoelace-algorithm/
