from PIL import Image
import logging

from debug import draw
from domain.models import CountResponse
from domain.ports import ObjectDetector, ObjectCountRepo
from domain.predictions import over_threshold, count


class CountDetectedObjects:
    def __init__(self, object_detector: ObjectDetector, object_count_repo: ObjectCountRepo):
        self.__object_detector = object_detector
        self.__object_count_repo = object_count_repo
        self.logger = logging.getLogger(__name__)

    def execute(self, image, threshold) -> CountResponse:
        try:
            predictions = self.__find_valid_predictions(image, threshold)
            object_counts = count(predictions)
            self.__object_count_repo.update_values(object_counts)
            total_objects = self.__object_count_repo.read_values()
            return CountResponse(current_objects=object_counts, total_objects=total_objects)
        except Exception as e:
            self.logger.exception(
                "Error occurred in executing object detection.")
            raise e

    def __find_valid_predictions(self, image, threshold):
        try:
            predictions = self.__object_detector.predict(image)
            self.__debug_image(image, predictions, "all_predictions.jpg")
            valid_predictions = list(over_threshold(
                predictions, threshold=threshold))
            self.__debug_image(
                image, valid_predictions, f"valid_predictions_with_threshold_{threshold}.jpg")
            return valid_predictions
        except Exception as e:
            self.logger.exception(
                "Error occurred in finding valid predictions.")
            raise e

    @staticmethod
    def __debug_image(image, predictions, image_name):
        if __debug__ and image is not None:
            try:
                image = Image.open(image)
                draw(predictions, image, image_name)
            except Exception as e:
                logging.getLogger(__name__).exception(
                    f"Error occurred in drawing predictions on image {image_name}.")
                raise e
