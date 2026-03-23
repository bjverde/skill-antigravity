"""
PDF to Markdown Extraction Tool

This script allows you to extract text from a specific range of pages in a PDF file
and save it as a Markdown file.

Usage:
    python pdf2md.py --input <path_to_pdf> --output <path_to_md> --start <start_page> --end <end_page>

Example:
    python pdf2md.py --input document/book.pdf --output document/summary.md --start 10 --end 15
"""

import pypdf
import os
import argparse

def extract_pages(reader, start_page, end_page):
    """
    Extracts text from a range of pages in a PDF reader object.

    Args:
        reader (pypdf.PdfReader): The PDF reader instance.
        start_page (int): The first page to extract (1-based index).
        end_page (int): The last page to extract (1-based index).

    Returns:
        str: The extracted text concatenated from all specified pages.
    """
    text = ""
    # Pypdf uses 0-based indexing internally
    # Ensure end_page does not exceed the total number of pages
    num_pages = len(reader.pages)
    if end_page > num_pages:
        end_page = num_pages
        print(f"Warning: Ending extraction at last page ({num_pages})")
    
    # Iterate through the range of pages and extract text
    for page_num in range(start_page - 1, end_page):
        page = reader.pages[page_num]
        text += page.extract_text() + "\n\n"
    return text

def main():
    """
    Main entry point for the script. Parses command-line arguments and handles the PDF extraction.
    """
    parser = argparse.ArgumentParser(description="Extract pages from a PDF and save to Markdown.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input PDF file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output Markdown file")
    parser.add_argument("--start", "-s", type=int, default=1, help="Start page (1-based, default: 1)")
    parser.add_argument("--end", "-e", type=int, help="End page (1-based, default: last page)")

    args = parser.parse_args()

    pdf_path = args.input
    output_path = args.output
    start_page = args.start

    # Check if the input file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    try:
        # Initialize the PDF reader
        reader = pypdf.PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        # Determine the end page (default to total pages if not provided)
        end_page = args.end if args.end is not None else num_pages

        # Basic validation of page ranges
        if start_page < 1 or start_page > num_pages:
            print(f"Error: Invalid start page {start_page}. PDF has {num_pages} pages.")
            return
        
        if end_page < start_page:
            print(f"Error: End page {end_page} must be greater than or equal to start page {start_page}.")
            return

        print(f"Extracting pages {start_page} to {end_page} from {pdf_path}...")
        
        # Prepare the Markdown content
        content = f"# Extração de {os.path.basename(pdf_path)}\n\n"
        content += f"## Páginas {start_page} a {end_page}\n\n"
        content += extract_pages(reader, start_page, end_page)
        
        # Save the extracted content to the output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Extraction successful! Saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
