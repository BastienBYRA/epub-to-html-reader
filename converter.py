import logging
import os
from pathlib import Path
import shutil
import uuid
from zipfile import ZipFile

from html_modifier import convert_xhtml_to_html
from parsers.ncx_parser import ncx_parser

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

def converter(filepath: str, output_directory: str | None):
    '''
    Convert an EPUB file to a collection of HTML files with some additionnal HTML/CSS for easier navigation
    '''
    
    book_uuid: uuid.UUID = uuid.uuid4()
    
    # Check the file exist
    path = Path(filepath)
    if not path or not path.exists():
        logger.error(f"The file '{filepath}' doesn't exist")
        exit(1)

    # Ensure it a .epub file
    if path.suffix != ".epub":
        logger.error("The file extension is not .epub, use the flag --ignore-extension if you still want to pass it")
        exit(1)

    # Convert the file in a .zip file (because .epub file are basically .zip with specification)
    filename = str(path).split(path.suffix)[0]
    zip_filename = filename + ".zip"

    if output_directory is None:
        output_directory = str(book_uuid)

    # Create the output folder if it doesn't exist
    if not Path(output_directory).exists():
        try:
            os.mkdir(output_directory)
            logger.debug(f"Directory '{output_directory}' created successfully.")
        except FileExistsError:
            logger.info(f"Directory '{output_directory}' already exists.")
        except PermissionError:
            logger.error(f"Permission denied: Unable to create '{output_directory}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    output_filepath = Path(f"{output_directory}/{zip_filename}")

    # Create the ZIP file
    shutil.copy2(path, output_filepath)

    # Extract the ZIP file and remove it
    with ZipFile(output_filepath, 'r') as zFile:
        zFile.extractall(Path(output_directory))
    os.remove(output_filepath)

    # Convert xhtml file to html cause xhtml can be quite boring as it has verification and stuff
    # not allowing us to add HTML after <html> tag for example
    #
    # (Because we will later add code in the HTML files, having to deal with XHTML verification and check
    # will be troublesome, some we just convert it to HTML)
    convert_xhtml_to_html(output_directory)

    # ncx parser
    ncx_parser(book_uuid, output_directory)