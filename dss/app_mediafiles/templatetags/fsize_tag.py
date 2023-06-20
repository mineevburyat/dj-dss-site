from django import template

register = template.Library()
T = 1099511627776
G = 1073741824
M = 1048576
K = 1024

@register.filter()
def filesize(fsize):
    if isinstance(fsize, (int, float)):
        if fsize >= G:
            return f"{round(fsize/G, 1)} Гбайт"
        elif G > fsize >= M:
            return f"{round(fsize/M, 1)} Мбайт"
        elif M > fsize >= K:
            return f"{round(fsize/K, 1)} Кбайт"
        else:
            return f"{fsize} байт"

# register.filter('filesize', filesize)