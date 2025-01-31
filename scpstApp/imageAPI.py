
import cv2
import os
from paddleocr import PaddleOCR

def cropImage(image_path, coordinates):
    # Read the image
    img = cv2.imread(image_path)
    
    # Extract coordinates
    left, top, width, height = coordinates['left'], coordinates['top'], coordinates['boxWidth'], coordinates['boxHeight']
    
    # Crop the image
    cropped_img = img[int(top):int(top)+int(height), int(left):int(left)+int(width)]
      
    # Generate a unique filename for the cropped image
    cropped_filename = "cropped.png"
    cropped_path = os.path.join('static/cropped', cropped_filename)
    
    # Save the cropped image
    cv2.imwrite(cropped_path, cropped_img)
    
    return cropped_path


def ocrImage(image_path):

    # Initialize PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    print("OCR initialized")

    # Perform OCR on the image
    result = ocr.ocr(image_path, cls=True)[0]
    print("OCR result: ", result)

    # Extract the text from the result
    text = ' '.join([text for bbox, (text, conf) in result])

    # Remove trailing space and return the text
    return text
