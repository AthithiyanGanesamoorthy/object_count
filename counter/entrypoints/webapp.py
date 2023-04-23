

from io import BytesIO
from fastapi import FastAPI, UploadFile, File
import os
import sys
import uvicorn
import logging
# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
app = FastAPI(docs_url='/swagger')

count_action = config.get_count_action()

logger = logging.getLogger(__name__)


@app.post('/object-count')
async def object_detection(file: UploadFile = File(...), threshold: float = 0.5):
    """
    Endpoint that receives an uploaded image and returns a count of the objects detected in the image 
    above the given threshold.

    Args:
    - file: A file object containing the image data to be processed.
    - threshold: A float value between 0 and 1 indicating the minimum confidence threshold for 
    detecting objects in the image.

    Returns:
    - A list containing the count of objects detected in the image and total list of objects with its count above the given threshold.
    """
    try:
        contents = await file.read()
        image = BytesIO(contents)
        count_response = count_action.execute(image, threshold)
        return [count_response]
    except Exception as e:
        logger.error(
            f"An error occurred while processing the request: {str(e)}")
        return {"error": "Failed to process request"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("webapp:app", host="0.0.0.0", port=5014,
                log_level="info", reload=True)
