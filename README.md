# Epub to HTML Reader
Etohr (Epub TO Html Reader) is a simple program that aim to turn a EPUB / .epub file into a collection of HTML files that can be read easily.

# State of the project
As of today, this project is a CLI, that turn a EPUB file into a collection of HTML.

The goal is, later on, to be a website in which you can drag & drop a EPUB file, and it turn it into a collection of HTML files.

# Install
**CURRENTLY, THE APPLICATION WORKS, BUT IT REQUIRES THE FOLLOWING**
- The repository cloned in your filesystem
- Python (3.12)
- An epub file at the root of the cloned repository (named book.epub)

**TO LAUNCH IT, RUN THE MAIN.PY FILE**

**NOTE: A DOCKER IMAGE IS BEING PREPARED, BUT IT IS NOT YET COMPLETE. IT SHOULD BE READY FOR VERSION 1.0.0.**

# Want to help
Feel free to open an issue if you have an idea or want to do something on this project, every contribution is appreciated!

# Problem / Error
Open an issue with your issue, provide logs and what you've done step by step to encounter the issue.

# Roadmap
- [ ] 1.0.0 : First Release
    - Create the application
        - [x] The logic to decompress the epub file and get the HTML files
        - [x] NCX parser to we can identify the HTML files and reading order
        - [x] HTML modifier to add custom HTML in HTML page
        - [ ] CLI part with argument and the docs associated
    - [ ] Create the Dockerfile to ship the project
    - [x] Create a BOOK_NOTICE.txt + some after decompiling the EPUB so the user know which file is the first page of the book (+ in BOOK_NOTICE.txt which file refer to which chapter)
    - [ ] Create all the logging stuff so user can know if it's good or if there is a problem (setup DEBUG env)
    - [ ] Create the doc of the app in the README.md

- [ ] 1.1.0 : Responsive patch
    - [ ] Add code so user can change the size of all texts + override default size text, adapt the text size for all kind of device (computer, tablet, phone)

- [ ] 1.2.0 : Website patch
    - [ ] Create an API to interact with the CLI
    - [ ] Create a webpage that can accept drag&drop epub
    - [ ] Implement a storage of decompressed epub in filesystem so user can have in the webpage a list of all his decompressed epub that he can easily read and jump into
    - [ ] Add a file / storage so the application remember which chapter the user was reading

- [ ] 1.2.0 or 1.3.0 : Public website
    - [ ] Check if it possible to store the data client side so I can publish the website to the public, so their can use it without having to setting this up on their side (using IndexedDB or similar thing)

- [ ] 1.3.0 or 1.4.0 : Desktop application patch (Might not happen)
    - [ ] Check if possible to create a desktop app to act like the website