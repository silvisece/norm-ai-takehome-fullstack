import fitz  # PyMuPDF
import os

pdf_file_path = 'docs/laws.pdf'
text_file_path = 'docs/laws_text.txt'

def extract_pdf_text(pdf_path: str, output_path: str) -> None:
    """
    Extract text from a PDF file and save it to a text file.

    Args:
        pdf_path: Path to the PDF file
        output_path: Path where to save the extracted text
    """
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)

        # Extract text from all pages
        text = ""
        for page in doc:
            text += page.get_text()

        # Save the text to a file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Successfully extracted text from {pdf_path} to {output_path}")

    except Exception as e:
        print(f"Error extracting text: {str(e)}")
    finally:
        if 'doc' in locals():
            doc.close()

if __name__ == "__main__":
    # Get the absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    pdf_path = os.path.join(project_root, pdf_file_path)
    output_path = os.path.join(project_root, text_file_path)

    # Extract and save the text
    extract_pdf_text(pdf_path, output_path) 
