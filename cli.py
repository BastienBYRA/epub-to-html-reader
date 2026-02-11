from typing import Annotated
import typer

from converter import converter

app = typer.Typer(
    help="EPUB to HTML converter with some custom HTML/CSS so it's easy to navigate between chapters",
    short_help="EPUB to HTML converter",
    add_help_option=True,
    name="Etohr",
)

PROJECT_VERSION="0.1.0"

@app.command()
def convert(
    filepath: Annotated[str, typer.Option(
        "-f", "--filepath",
        help="Filepath to the EPUB file",
        envvar="ETOHR_BOOK")], 
    output_directory: Annotated[str | None, typer.Option(
        "-o", "--output-directory",
        help="Output folder for the EPUB file", 
        envvar="ETOHR_OUTPUT_DIRECTORY")] = "output"):
    '''
    Convert an EPUB file to a collection of HTML files with some additionnal HTML/CSS for easier navigation
    '''
    converter(filepath, output_directory)

@app.command()
def version():
    '''
    Show the version of the project
    '''
    print(f'''
Version: {PROJECT_VERSION}
''')
    
@app.command()
def info():
    '''
    Show information about the project
    '''
    print('''
Version: {PROJECT_VERSION}
Github: https://github.com/BastienBYRA/epub-to-html-reader
Issue: https://github.com/BastienBYRA/epub-to-html-reader/issues
Want to help: https://github.com/BastienBYRA/epub-to-html-reader/issues
''')

if __name__ == "__main__":
    app()