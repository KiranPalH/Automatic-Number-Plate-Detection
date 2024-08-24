import cv2
import pytesseract as pt

# Extract text from number plate 
def extract_text(image, bbox): 
    x, y, w, h = bbox
    roi = image[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    text = pt.image_to_string(gray, Lang='eng', config='--psm 6') 
    return text



    