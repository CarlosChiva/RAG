from http.client import HTTPException
from tempfile import TemporaryDirectory
import tempfile
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
import os
from langchain.schema import Document

from pypdf import PdfReader
model=os.getenv("MODEL")
import pymupdf
from PIL import Image
import pytesseract
import io
#-------------------------------------
# To read the PDF
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# To extract text from tables in PDF
import pdfplumber
# To extract the images from the PDFs
from PIL import Image
from pdf2image import convert_from_path
# To perform OCR to extract text from images 
import pytesseract 
# To remove the additional created files
import os
# Create function to extract text

def text_extraction(element):
    # Extracting the text from the in line text element
    line_text = element.get_text()
    
    # Find the formats of the text
    # Initialize the list with all the formats appeared in the line of text
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Iterating through each character in the line of text
            for character in text_line:
                if isinstance(character, LTChar):
                    # Append the font name of the character
                    line_formats.append(character.fontname)
                    # Append the font size of the character
                    line_formats.append(character.size)
    # Find the unique font sizes and names in the line
    format_per_line = list(set(line_formats))
    
    # Return a tuple with the text in each line along with its format
    return (line_text, format_per_line)
# Extracting tables from the page

def extract_table(pdf_path, page_num, table_num):
    # Open the pdf file
    pdf = pdfplumber.open(pdf_path)
    # Find the examined page
    table_page = pdf.pages[page_num]
    # Extract the appropriate table
    table = table_page.extract_tables()[table_num]
    
    return table

# Convert table into appropriate fromat
def table_converter(table):
    table_string = ''
    # Iterate through each row of the table
    for row_num in range(len(table)):
        row = table[row_num]
        # Remove the line breaker from the wrapted texts
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        # Convert the table into a string 
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
    # Removing the last line break
    table_string = table_string[:-1]
    return table_string

# Create a function to check if the element is in any tables present in the page
def is_element_inside_any_table(element, page ,tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False

# Function to find the table for a given element
def find_table_for_element(element, page ,tables):
    x0, y0up, x1, y1up = element.bbox
    # Change the cordinates because the pdfminer counts from the botton to top of the page
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i  # Return the index of the table
    return None  
# Create a function to crop the image elements from PDFs
def crop_image(element, pageObj):
    # Get the coordinates to crop the image from PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1] 
    # Crop the page using coordinates (left, bottom, right, top)
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    # Save the cropped page to a new PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    # Save the cropped PDF to a new file
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Create a function to convert the PDF to images
def convert_to_images(input_file,):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = 'PDF_image.png'
    image.save(output_file, 'PNG')

# Create a function to read text from images
def image_to_text(image_path):
    # Read the image
    img = Image.open(image_path)
    # Extract the text from the image
    text = pytesseract.image_to_string(img)
    return text


def new_mode_extraction(pdf_path):
    # Create a pdf file object
    pdfFileObj = open(file=pdf_path, mode='rb')
    # Create a pdf reader object
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)



    # Create the dictionary to extract text from each image
    text_per_page = {}
    # Create a boolean variable for image detection
    image_flag = False
    # We extract the pages from the PDF
    for pagenum, page in enumerate(extract_pages(pdf_path)):

        # Initialize the variables needed for the text extraction from the page
        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        line_format = []
        text_from_images = []
        text_from_tables = []
        page_content = []
        # Initialize the number of the examined tables
        table_in_page= -1
        # Open the pdf file
        pdf = pdfplumber.open(pdf_path)
        # Find the examined page
        page_tables = pdf.pages[pagenum]
        # Find the number of tables in the page
        tables = page_tables.find_tables()
        if len(tables)!=0:
            table_in_page = 0
        print("Tables: ",tables)

        # Extracting the tables of the page
        for table_num in range(len(tables)):
            # Extract the information of the table
            table = extract_table(pdf_path, pagenum, table_num)
            # Convert the table information in structured string format
            table_string = table_converter(table)
            # Append the table string into a list
            text_from_tables.append(table_string)

        # Find all the elements
        page_elements = [(element.y1, element) for element in page._objs]
        # Sort all the element as they appear in the page 
        page_elements.sort(key=lambda a: a[0], reverse=True)

        # Find the elements that composed a page
        for i,component in enumerate(page_elements):
            # Extract the element of the page layout
            element = component[1]

            # Check the elements for tables
            if table_in_page == -1:
                pass
            else:
                if is_element_inside_any_table(element, page ,tables):
                    table_found = find_table_for_element(element,page ,tables)
                    if table_found == table_in_page and table_found != None:    
                        page_content.append(text_from_tables[table_in_page])
                        page_text.append('table')
                        line_format.append('table')
                        table_in_page+=1
                    # Pass this iteration because the content of this element was extracted from the tables
                    continue

            if not is_element_inside_any_table(element,page,tables):

                # Check if the element is text element
                if isinstance(element, LTTextContainer):
                    # Use the function to extract the text and format for each text element
                    (line_text, format_per_line) = text_extraction(element)
                    # Append the text of each line to the page text
                    page_text.append(line_text)
                    # Append the format for each line containing text
                    line_format.append(format_per_line)
                    page_content.append(line_text)


                # Check the elements for images
                if isinstance(element, LTFigure):
                    # Crop the image from PDF
                    crop_image(element, pageObj)
                    # Convert the croped pdf to image
                    convert_to_images('cropped_image.pdf')
                    # Extract the text from image
                    image_text = image_to_text('PDF_image.png')
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    # Add a placeholder in the text and format lists
                    page_text.append('image')
                    line_format.append('image')
                    # Update the flag for image detection
                    image_flag = True


        # Create the key of the dictionary
        dctkey = 'Page_'+str(pagenum)
        # Add the list of list as value of the page key
        text_per_page[dctkey]= [line_format,page_text , text_from_images,text_from_tables, page_content]

    print("pdffileobj",pdfFileObj)
    # Close the pdf file object
    pdfFileObj.close()
    # Delete the additional files created if image is detected
    if image_flag:
        os.remove('cropped_image.pdf')
        os.remove('PDF_image.png')
    # Display the content of the page
    unique_lines = set()
    test=""
    for key in text_per_page:
      #  print(text_per_page[key][2],text_per_page[key][3],text_per_page[key][4])

    #    page_text = ''.join(text_per_page[key][1])
          # Convertir a string el contenido del texto con formato
        text_from_images = ''.join(text_per_page[key][2]) 
        text_from_tables = ''.join(text_per_page[key][3])  
        page_content = ''.join(text_per_page[key][4])
        unique_lines.update(' '.join([text_from_images, text_from_tables, page_content]).splitlines())
    result = ''.join(unique_lines)

    print("Resultado de la extracción:----->", result)
    
    return result     
#-------------------------------------

def extract_images_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    return images

def extract_text_from_images(images):
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image) + "\n"
    return text
def is_text_extractable(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return bool(text.strip())
    except Exception as e:
        print(f"Error: {e}")
        return False
# Función para cargar un documento PDF
import os

def obtener_extension(file) -> str:
    fileext = file.filename.split(".")[-1]
    return fileext
async def load_document(file: UploadFile):
    extension = obtener_extension(file)


    print("Extension: ",extension)
    match extension:
        case "txt":
            contenido = await file.read()
            documents= contenido.decode("utf-8")  # Leer como texto

        case "pdf":
            with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp_file:
                temp_file.write(await file.read())
                temp_path = temp_file.name
                documents = new_mode_extraction(temp_path)
        # import fitz
        # try:
        #     contenido_pdf = file.file.read()  # Evita consumir el stream más de una vez
        #     doc = fitz.open(stream=contenido_pdf, filetype="pdf")
        #     return " ".join([page.get_text() for page in doc])
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Error al procesar PDF: {str(e)}")


        case "docx":
            from docx import Document as Doc

            try:
                print("Leyendo archivo DOCX...")  # Depuración
                contenido_docx = await file.read()  # Leer contenido
                file_stream = io.BytesIO(contenido_docx)  # Convertir a stream de bytes
                doc = Doc(file_stream)  # Cargar documento en python-docx
                print("Documento cargado correctamente.")  # Depuración
                return " ".join([p.text for p in doc.paragraphs])
            except Exception as e:
                print(f"Error al procesar DOCX: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error al procesar DOCX: {str(e)}")

    # print("filename; ",filename)
    # if not is_text_extractable(filename):
    #     print("Found images")
    #     return extract_text_from_images(extract_images_from_pdf(filename))
    # else:
    #     print("Found text")
    #     loader = PyPDFLoader(filename)
    #     documents = loader.load()
    #     print(documents)
    print("Return??",documents)
    return documents

# Función para dividir el texto de los documentos
async def text_split(documents, chunk_size=1000, chunk_overlap=20):
# Supongamos que 'result' es el string que obtuviste previamente
    foc=documents
    # Crear una lista con un solo documento, ya que split_documents espera un iterable
    document = Document(page_content=documents, metadata={'source': 'pdf'})
    print("document: ",document)
    print("Document to split text",type(foc))

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents([document])
    return all_splits
# Función para inicializar el modelo y tokenizer de embeddings
def init_embedding_model():
    embedding_func = OllamaEmbeddings(model="mxbai-embed-large")
    return embedding_func
