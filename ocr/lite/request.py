from dotenv import load_dotenv
from PIL import Image
import requests
import time
import json
import os


class Ocr():
    def __init__(self):
        self.url = "https://api.ocr.space/parse/image"  # POST METHOD ENDPOINT
        self.api_key = os.getenv("API_KEY_OCR")


    """
        This method will resize the image to specified dimensions.
        Original image will be overwritten with resized image in same file path.

        PARAMETERS
        ----------
        file_path : str
            The path to the image file to be resized.
        width : int
            The desired width of the resized image.
        height : int
            The desired height of the resized image.    
    """
    def resize_image(self, file_path: str, width: int, height: int) -> None:
        image = Image.open(file_path)
        image = image.resize((width, height))
        image.save(file_path)


    """
        This method will start the OCR process on the given image file.

        PARAMETERS
        ----------
        file_path : str
            The path to the image file to be processed.

    """
    def start_ocr(self, file_path: str) -> list[dict]:

        # resize image
        self.resize_image(file_path, 960, 540)

        # parameters for ocr
        payload = {
            "apikey": self.api_key,
            "language": "eng",
            "isOverlayRequired": True,
            "isTable": False,
            "OCREngine": 2
        }

        try:
            with open(file_path, "rb") as image_files:
                response = requests.post(
                    self.url,
                    files={"file": image_files},
                    data=payload
                )
        except Exception as e:
            print(f"Error: {e}")
            return []

        response = response.json()
        response = response["ParsedResults"][0]["TextOverlay"]["Lines"]
        print(type(response))
        return self.filter_json(response)

    """
    Filter the JSON response from the OCR API.

    This method will return a filtered list of dictionaries
    containing the line text and bounding box coordinates.
    
    PARAMETERS
    ----------
    lines : list[dict]
        A list of dictionaries containing the OCR results.

    """
    def filter_json(self, lines: list[dict]) -> list[dict]:
        results = []

        for line in lines:
            data = {}
            data["LineText"] = line["LineText"]
            x1 = min([word["Left"] for word in line["Words"]])
            y1 = min([word["Top"] for word in line["Words"]])
            x2 = max([word["Left"] + word["Width"] for word in line["Words"]])
            y2 = max([word["Top"] + word["Height"] for word in line["Words"]])
            data["BoundingBox"] = [x1, y1, x2, y2]
            results.append(data)

        return results


def main() -> None:
    load_dotenv()
    ocr = Ocr()
    file_path = "image\\image.jpg"
    result = ocr.start_ocr(file_path)

    for line in result:
        print(line)


if __name__ == "__main__":
    main()
