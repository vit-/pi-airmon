from io import BytesIO

from matplotlib import pyplot


def draw_png(data, predictions=None):
    pyplot.plot(data, color='blue')
    if predictions is not None:
        pyplot.plot(predictions, color='blue', linestyle='dashed')
    pyplot.xlabel('time')
    pyplot.ylabel('$CO_2$')
    pyplot.grid(True)

    img = BytesIO()
    pyplot.savefig(img, format='png')
    pyplot.clf()
    img.seek(0)
    return img
