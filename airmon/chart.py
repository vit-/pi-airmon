from io import BytesIO

from matplotlib import pyplot


def draw_png(data, predictions):
    pyplot.plot(data, color='blue')
    pyplot.plot(predictions, color='blue', linestyle='dashed')
    pyplot.xlabel('time')
    pyplot.ylabel('co2')
    pyplot.grid(True)

    img = BytesIO()
    pyplot.savefig(img, format='png')
    pyplot.clf()
    img.seek(0)
    return img
