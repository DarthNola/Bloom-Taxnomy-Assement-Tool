import re
import pypdfium2 as pdfium
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from pytesseract import image_to_string, pytesseract

# Specify the path to Tesseract executable if needed
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust if needed

def convert_pdf_to_images(file_path, scale=300/72):
    try:
        pdf_file = pdfium.PdfDocument(file_path)
        page_indices = range(len(pdf_file))

        renderer = pdf_file.render(
            pdfium.PdfBitmap.to_pil,
            page_indices=page_indices,
            scale=scale,
        )

        list_final_images = []

        for i, image in zip(page_indices, renderer):
            with BytesIO() as image_byte_array:
                image.save(image_byte_array, format='jpeg', optimize=True)
                list_final_images.append({i: image_byte_array.getvalue()})

        return list_final_images

    except Exception as e:
        print(f"An error occurred while converting PDF to images: {e}")
        return []

def display_images(list_dict_final_images):
    if not list_dict_final_images:
        print("No images to display.")
        return

    for index, image_bytes in enumerate(list(data.values())[0] for data in list_dict_final_images):
        image = Image.open(BytesIO(image_bytes))
        plt.figure(figsize=(image.width / 100, image.height / 100))
        plt.title(f"----- Page Number {index + 1} -----")
        plt.imshow(image)
        plt.axis("off")
        plt.show()

def extract_text_with_pytesseract(list_dict_final_images):
    if not list_dict_final_images:
        print("No images to extract text from.")
        return ""

    text_list = []
    for image_bytes in (list(data.values())[0] for data in list_dict_final_images):
        image = Image.open(BytesIO(image_bytes))
        text_list.append(image_to_string(image))

    return "\n".join(text_list)

def extract_questions_from_text(text):
    keywords = ['how', 'explain', 'describe', 'define', 'name', 
                'which', 'who', 'where', 'when', 'state', 'determine', 
                'illustrate']

    pattern = r'\b(?:' + '|'.join(keywords) + r')\b.*?[?.]'
    questions = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    
    return questions


path_to_pdf = r'Backend\digitalexam.pdf'
images_list = convert_pdf_to_images(path_to_pdf)
text_from_images = extract_text_with_pytesseract(images_list)

questions = extract_questions_from_text(text_from_images)

if questions:
    print("Found Questions:")
    for i, question in enumerate(questions, start=1):
        print(f"Question {i}: {question.strip()}")
else:
    print("No questions found in the PDF.")


