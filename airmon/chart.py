from io import BytesIO

from matplotlib import pyplot


def draw_png(data, predictions):
    pyplot.plot(data)
    pyplot.plot(predictions, linestyle='dashed')
    pyplot.xlabel('time')
    pyplot.ylabel('co2')
    pyplot.grid(True)

    img = BytesIO()
    pyplot.savefig(img, format='png')
    img.seek(0)
    return img
