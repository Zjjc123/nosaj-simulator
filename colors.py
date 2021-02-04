import colorsys

def distinct_colors(n):
    HSV_tuples = [(x/n, 1, 1) for x in range(n)]
    print(HSV_tuples)
    rgb = []
    for c in HSV_tuples:
        rgb.append(list(map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*c))))
    return rgb
