from glob import glob
import logging
import os
from pathlib import Path
import shutil
from models.NcxChapter import NcxChapter

logger = logging.getLogger(__name__)

def add_select_to_pages(selector: dict[str, NcxChapter], output_directory: str):
    """
    Add `select` bloc in HTML pages with the differents chapter and the good location
    """

    # HTML code for the `select` bloc, so user can easily switch between pages
    HTML_SELECT_START = "<select onchange=\"window.document.location.href=this.options[this.selectedIndex].value;\" id=\"epub_to_html_custom_selector\">"
    HTML_SELECT_END = "</select>"
    HTML_SELECT_CSS ='''
<style>
#epub_to_html_custom_selector {
  display: block;
  margin: 0px 20px;
  padding: 10px 14px;
  font-size: 16px;
  font-family: inherit;

  color: #333;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;

  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  cursor: pointer;

  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

#epub_to_html_custom_selector:hover {
  border-color: #999;
}

#epub_to_html_custom_selector:focus {
  outline: none;
  border-color: #5b9cff;
  box-shadow: 0 0 0 3px rgba(91, 156, 255, 0.25);
}

.epub_to_html_custom_div_wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 20px auto;
}

.epub_to_html_custom_btn {
  width: 42px;
  height: 42px;

  font-size: 20px;
  line-height: 1;

  color: #333;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 6px;

  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;

  transition: background-color 0.2s ease,
              border-color 0.2s ease,
              box-shadow 0.2s ease;
}

.epub_to_html_custom_btn:hover {
  background-color: #f5f5f5;
  border-color: #999;
}

.epub_to_html_custom_btn:active {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}
</style>
'''

    previous_chapter: int = 0
    book_notice_content: str = ""

    # Iterate through all the key;value to get the filepath for each chapter
    for filename, _ in selector.items():
        filepath: Path = get_html_file(filename, output_directory)
        filepath_html = str(filepath).replace("\\", "/")

        html_options = ""
        html_previous_button = ""
        html_next_button = ""

        count: int = 1

        # Create the option bloc for the select, 
        for _filename, chapter in selector.items():
            if filename == _filename:
                html_options += f"<option selected=\"true\" value=\"/{filepath_html}\">{chapter.title}</option>"
                book_notice_content += f"{chapter.title} -> {filepath_html}\n"
            else:
                _filepath: Path = Path(str(get_html_file(_filename, output_directory)).replace("\\", "/"))
                _filepath_html = str(_filepath).replace("\\", "/")

                if previous_chapter == count:
                    html_previous_button = f"<button class=\"epub_to_html_custom_btn\" onclick=\"location.href='/{_filepath_html}'\"> ‹ </button>"
                if previous_chapter+2 == count:
                    html_next_button = f"<button class=\"epub_to_html_custom_btn\" onclick=\"location.href='/{_filepath_html}'\"> › </button>"

                html_options += f"<option value=\"/{_filepath_html}\">{chapter.title}</option>"
            
            count+=1
        count = 1
        previous_chapter += 1
        
        html_full_select = f"{HTML_SELECT_START}{html_options}{HTML_SELECT_END}"
        html_div = f"<div class=\"epub_to_html_custom_div_wrapper\">{html_previous_button}{html_full_select}{html_next_button}</div>"

        # Add select at the start of the page
        #
        # Read the file first and copy it content, then add as the first line the select, then copy
        # back the content in the file
        file_content = ""
        with open(filepath, "r", encoding="utf-8") as chapter_file:
            file_content = chapter_file.readlines()
            file_content.insert(0, html_div)
        with open(filepath, "w", encoding="utf-8") as chapter_file:
            chapter_file.writelines(file_content)

        # Add select at the end of the page
        with open(filepath, "a", encoding="utf-8") as chapter_file:
            chapter_file.write(html_div)
            chapter_file.write(HTML_SELECT_CSS)

    # Create a BOOK_NOTICE.txt file with information about each chapter and the file related
    with open(f"{output_directory}/BOOK_NOTICE.txt", "w", encoding="utf-8") as book_notice_file:
        book_notice_file.write(book_notice_content)

    logger.info("The decompression of the EPUB fine is done!\n" \
    f"You can find the page related to every chapter in the {output_directory}/BOOK_NOTICE.txt file.")
    logger.info(f"The first chapter: [{book_notice_content.split("\n")[0]}]")


def get_html_file(filename: str, output_directory: str) -> Path:
    '''
    Get the filepath for a specific filename

    TODO: Maybe create a file_utils.py file or something similar, cause this is redundant with `get_ncx_file()`
    '''
    filepath = Path(f"{output_directory}/{filename}")
    if not filepath.exists():
        filepath = Path(f"{output_directory}/OEBPS/{filename}")
        if not filepath.exists():
            logger.error(f"HTML file {filename} not found (expected either '{output_directory}/{filename}' or '{output_directory}/OEBPS/{filename}')")
            exit(1)
    return filepath


def convert_xhtml_to_html(output_directory: str) -> None:
    '''
    Convert every .xhtml file to .html

    We do that because xhtml can be quite boring as it has verification and stuff
    not allowing us to add HTML after <html> tag for example
    
    (Because we will later add code in the HTML files, having to deal with XHTML verification and check
    will be troublesome, some we just convert it to HTML)
    '''
    xhtml_files = glob(f"{output_directory}/**.xhtml")
    xhtml_files += glob(f"{output_directory}/OEBPS/**.xhtml")
    
    for file in xhtml_files:
        filepath = Path(file)
        filename = str(file).split(filepath.suffix)[0]
        html_filename = filename + ".html"

        shutil.copy2(file, html_filename)
        os.remove(file)