import numpy


default_colormap = {
    0: "█",
    1: "░",
}


def to_ascii(x, colormap=None) -> str:
    colormap = colormap or default_colormap
    if not isinstance(x, numpy.ndarray):
        x = numpy.array(x)
    printout = numpy.ndarray(x.shape, dtype=str)
    for k, v in colormap.items():
        printout = numpy.where(x == k, v, printout)
    return "\n".join("".join(l) for l in printout.tolist())


def coordinates_to_ascii(d, colormap=None) -> str:
    coordinates = numpy.array(list(d.keys()))
    m = coordinates.min(axis=0)
    coordinates -= m
    z = numpy.zeros(coordinates.max(axis=0) + 1)
    for a in coordinates:
        z[tuple(a)] = d[tuple(a + m)]
    return to_ascii(numpy.rot90(z), colormap=colormap)
