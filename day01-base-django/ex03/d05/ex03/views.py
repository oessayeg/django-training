from django.shortcuts import render


def generate_lighter_shades(base_color, iterator, steps):
    r, g, b = base_color

    factor = iterator / (steps - 1)

    new_r = int(r + (255 - r) * factor)
    new_g = int(g + (255 - g) * factor)
    new_b = int(b + (255 - b) * factor)

    return (new_r, new_g, new_b)


def table_shades(request):
    steps = 50
    color_table = []
    blue = (0, 0, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    dark = (0, 0, 0)

    for i in range(0, 50):
        row_colors = []
        row_colors.append(generate_lighter_shades(red, i, steps))
        row_colors.append(generate_lighter_shades(green, i, steps))
        row_colors.append(generate_lighter_shades(dark, i, steps))
        row_colors.append(generate_lighter_shades(blue, i, steps))
        color_table.append(row_colors)
    return render(request, "shades.html", {"color_table": color_table})
