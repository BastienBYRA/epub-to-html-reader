import logging
from pathlib import Path
import uuid
import xml.etree.ElementTree as ET

from html_modifier import add_select_to_pages
from models.NcxBook import NcxBook
from models.NcxChapter import NcxChapter

logger = logging.getLogger(__name__)

def ncx_parser(book_uuid: uuid.UUID, output_directory: str):
    """
    The parser role is to parse a toc.ncx file.
    These are files used by EPUB files to know the hierachical order of the book
    (e.g: Order of the chapter, link to their HTML pages)

    Example of a toc.ncx file in `example/toc.ncx` (Some toc.ncx aren't well formated, the one here is).
    """

    # Try to find the toc.ncx file
    toc_ncx_filepath: Path = get_ncx_file(output_directory)

    # Replace every mention of .xhtml to .html
    replace_xhtml_mention_to_html(toc_ncx_filepath)
    
    tree = ET.parse(toc_ncx_filepath)
    root = tree.getroot()

    book: NcxBook = NcxBook(book_uuid)
    book.set_namespace(root.tag)
    
    for element in root:
        tag = remove_namespace_from_tag(element.tag)
        
        # Get the navMap that contains every navPoint
        if tag == "navMap":
            for nav_point in element:
                parse_nav_point(nav_point, book)
    
    # Sort the Book based on the number attributed to each chapters
    book.sort()

    # Go through the book object to get the first chapter associated with each HTML page
    #
    # Basically, chapter, and their subchapter might share the same HTML page (depend of the book), 
    # if it the case, then it mean the HTML page will have multiple chapter in it.
    #
    # We need to get that data so we don't put multiple `select` HTML code in a same HTML page
    html_curated_book = book.get_first_chapter_per_html_page()

    # For each HTML page, apply a select with each chapter name and their link in it.
    add_select_to_pages(html_curated_book, output_directory)


def parse_nav_point(nav_point: any, book: NcxBook, chapter_parent: NcxChapter = None):
    """Parse recursively a navPoint and its children"""
    chapter_name = nav_point.find(f"{book.get_namespace_with_brace()}navLabel")[0].text
    chapter_file = nav_point.find(f"{book.get_namespace_with_brace()}content").get("src")
    chapter_number = int(nav_point.get("playOrder"))

    book.add_chapter(chapter_name, chapter_file, chapter_number, chapter_parent)

    sub_nav_point = nav_point.findall(f"{book.get_namespace_with_brace()}navPoint")
    if sub_nav_point is not None:
        for sub_sub_nav_point in sub_nav_point:
            parse_nav_point(sub_sub_nav_point, book)


def get_ncx_file(output_directory: str) -> Path:
    """
    Get the .ncx file, which is a XML used by .epub file to know how the book is organised
    """
    toc_ncx_filepath = Path(f"{output_directory}/toc.ncx")
    if not toc_ncx_filepath.exists():
        toc_ncx_filepath = Path(f"{output_directory}/OEBPS/toc.ncx")
        if not toc_ncx_filepath.exists():
            logger.error(f"NCX file not found (expected either '{output_directory}/toc.ncx' or '{output_directory}/OEBPS/toc.ncx')")
            exit(1)
    return toc_ncx_filepath

def parse_ncx_file():
    return True

def remove_namespace_from_tag(tag: str) -> str:
    # ugly way to remove the namespace from the xml tag
    return tag.split('}')[-1]

def replace_xhtml_mention_to_html(toc_ncx_filepath: Path):
    with open(toc_ncx_filepath, 'r') as file:
        data = file.read()
        data = data.replace(".xhtml", ".html")

    with open(toc_ncx_filepath, 'w') as file:
        file.write(data)