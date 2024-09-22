# import os
# import re
# import pypdfium2 as pdfium
# from PIL import Image
# from io import BytesIO
# from pytesseract import image_to_string, pytesseract
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# tesseract_path = os.getenv('TESSERACT_PATH')
# if tesseract_path:
#     pytesseract.tesseract_cmd = tesseract_path
# else:
#     raise FileNotFoundError("Tesseract path is not set in environment variables or not found.")

# def convert_pdf_to_images(file_path, scale=300/72):
#     try:
#         pdf_file = pdfium.PdfDocument(file_path)
#         page_indices = range(len(pdf_file))
#         renderer = pdf_file.render(pdfium.PdfBitmap.to_pil, page_indices=page_indices, scale=scale)

#         list_final_images = []
#         for i, image in zip(page_indices, renderer):
#             with BytesIO() as image_byte_array:
#                 image.save(image_byte_array, format='jpeg', optimize=True)
#                 list_final_images.append({i: image_byte_array.getvalue()})

#         return list_final_images

#     except Exception as e:
#         print(f"An error occurred while converting PDF to images: {e}")
#         return []

# def extract_text_with_pytesseract(list_dict_final_images):
#     if not list_dict_final_images:
#         print("No images to extract text from.")
#         return ""

#     text_list = []
#     for image_bytes in (list(data.values())[0] for data in list_dict_final_images):
#         image = Image.open(BytesIO(image_bytes))
#         text_list.append(image_to_string(image))

#     return "\n".join(text_list)

# def extract_questions_from_text(text):
#     keywords = ['how', 'explain', 'describe', 'define', 'name', 
#                 'which', 'who', 'where', 'when', 'state', 'determine', 
#                 'illustrate']
#     pattern = r'\b(?:' + '|'.join(keywords) + r')\b.*?[?.]'
#     questions = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
#     return questions


import os
import re
import pypdfium2 as pdfium
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
from pytesseract import image_to_string, pytesseract
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter

# Load environment variables
load_dotenv()
tesseract_path = os.getenv('TESSERACT_PATH')
if tesseract_path:
    pytesseract.tesseract_cmd = tesseract_path
else:
    raise FileNotFoundError("Tesseract path is not set in environment variables or not found.")

def convert_pdf_to_images(file_path, scale=300/72):
    try:
        pdf_file = pdfium.PdfDocument(file_path)
        page_indices = range(len(pdf_file))
        renderer = pdf_file.render(pdfium.PdfBitmap.to_pil, page_indices=page_indices, scale=scale)

        list_final_images = []
        for i, image in zip(page_indices, renderer):
            with BytesIO() as image_byte_array:
                image.save(image_byte_array, format='jpeg', optimize=True)
                list_final_images.append({i: image_byte_array.getvalue()})

        return list_final_images

    except Exception as e:
        print(f"An error occurred while converting PDF to images: {e}")
        return []

def preprocess_image(image):
    # Convert to grayscale
    image = image.convert('L')
    # Apply image enhancements
    image = image.filter(ImageFilter.MedianFilter(size=3))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Adjust contrast
    return image

def extract_text_with_pytesseract(list_dict_final_images):
    if not list_dict_final_images:
        print("No images to extract text from.")
        return ""

    text_list = []
    for image_bytes in (list(data.values())[0] for data in list_dict_final_images):
        image = Image.open(BytesIO(image_bytes))
        image = preprocess_image(image)  # Preprocess the image
        text = image_to_string(image)
        text_list.append(text)

    return "\n".join(text_list)

def extract_questions_from_text(text):
    keywords = [
        'how', 'explain', 'describe', 'define', 'name', 
        'which', 'who', 'where', 'when', 'state', 
        'determine', 'illustrate'
    ]
    # Improved regex pattern
    pattern = r'\b(?:' + '|'.join(keywords) + r')\b.*?[?.]'
    questions = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    
    # Use LangChain for better text handling (e.g., splitting long texts)
    text_splitter = CharacterTextSplitter(separator=' ', chunk_size=1000)
    chunks = text_splitter.split_text(text)
    
    return questions




