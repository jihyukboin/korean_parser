"""
Requirements: `pip install pymupdf` to import fitz
"""
 
import os
import fitz
 
def split_pdf(input_file, batch_size):
    # Open input_pdf
    input_pdf = fitz.open(input_file)
    num_pages = len(input_pdf)
    print(f"Total number of pages: {num_pages}")
 
    # Split input_pdf
    for start_page in range(0, num_pages, batch_size):
        end_page = min(start_page + batch_size, num_pages) - 1
 
        # Write output_pdf to file
        input_file_basename = os.path.splitext(input_file)[0]
        output_file = f"{input_file_basename}_{start_page}_{end_page}.pdf"
        print(output_file)
        with fitz.open() as output_pdf:
            output_pdf.insert_pdf(input_pdf, from_page=start_page, to_page=end_page)
            output_pdf.save(output_file)
 
    # Close input_pdf
    input_pdf.close()
 
# Input arguments
input_file = "asset/총론_초등_교육과정_400_499.pdf"  # Replace with a file of your own
batch_size = 50  # Maximum available value is 100
split_pdf(input_file, batch_size)