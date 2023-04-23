import os
import logging

from PIL import ImageDraw, ImageFont

logger = logging.getLogger(__name__)


def draw(predictions, image, image_name):
    draw_image = ImageDraw.Draw(image, "RGBA")

    image_width, image_height = image.size

    font = ImageFont.truetype("counter/resources/arial.ttf", 20)
    i = 0
    try:
        for prediction in predictions:
            box = prediction.box
            draw_image.rectangle(
                [(box.xmin * image_width, box.ymin * image_height),
                 (box.xmax * image_width, box.ymax * image_height)],
                outline='red')
            class_name = prediction.class_name
            draw_image.text(
                (box.xmin * image_width, box.ymin *
                 image_height - font.getsize(class_name)[1]),
                f"{class_name}: {prediction.score}", font=font, fill='black')
            i += 1
    except Exception as e:
        logger.error(f"Error drawing predictions: {e}")

    try:
        os.mkdir('tmp/debug')
    except OSError:
        pass

    try:
        image.save(f"tmp/debug/{image_name}", "JPEG")
    except Exception as e:
        pass
