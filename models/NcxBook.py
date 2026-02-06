from operator import attrgetter
import uuid
from models.NcxChapter import NcxChapter


class NcxBook():
    chapters: list[NcxChapter] = []
    namespace: str
    id: uuid.UUID

    def __init__(self, book_uuid: uuid.UUID):
        self.id = book_uuid

    def add_chapter(self, chapter_name: str, chapter_file: str, chapter_number: int, parent_chapter: NcxChapter | None = None):
        """
        Add a `NcxChapter` to either the `NxcBook` object, or another `NcxChapter` object as a subchapter.
        """

        # Strip the chapter_file of it anchor (#) if it has one
        chapter_file_no_anchor = chapter_file.split("#")[0]

        chapter: NcxChapter = NcxChapter(chapter_name, chapter_number, chapter_file_no_anchor, parent_chapter)

        def add_sub_chapter(sub_chapter: NcxChapter, parent_chapter_uuid: uuid.UUID):
            '''
            Iterate through the `NxcBook` object to get the parent chapter associated to the subchapter to add.
            '''

            for chapter in self.chapters:
                if chapter.uuid == parent_chapter_uuid:
                    chapter.sub_chapter.append(sub_chapter)

        if parent_chapter is None:
            self.chapters.append(chapter)
        else:
            add_sub_chapter(chapter, parent_chapter.uuid)


    def sort(self) -> None:
        """
        Sort the `NcxBook` object based on the attribute `number` of each `NcxChapter`, 
        and apply the sorted `NcxBook` to self.
        """

        def sort_chapters(chapters: list[NcxChapter]) -> list[NcxChapter]:
            """
            Recursive function of sort each subchapter of every `NcxChapter`
            """
            chapters = sorted(chapters, key=attrgetter("number"))

            for chapter in chapters:
                if chapter.sub_chapter:
                    chapter.sub_chapter = self._sort_chapters(chapter.sub_chapter)

            return chapters
        
        self.chapters = sort_chapters(self.chapters)
    

    def get_first_chapter_per_html_page(self) -> dict[str, NcxChapter]:
        """
        Return a mapping of HTML page -> first chapter appearing on that page

        Based on the smallest chapter.number for each page.
        """
        chapter_by_page: dict[str, NcxChapter] = {}

        def get_smallest_chapter(chapters: list[NcxChapter]):
            for chapter in chapters:
                page = chapter.filepath

                # If the page is not yet registered OR
                # the current chapter has a smaller number than the current one
                if (page not in chapter_by_page or chapter.number < chapter_by_page[page].number):
                    chapter_by_page[page] = chapter

                # Recurse into subchapters
                if chapter.sub_chapter:
                    get_smallest_chapter(chapter.sub_chapter)

        get_smallest_chapter(self.chapters)
        
        return chapter_by_page


    def set_namespace(self, namespace: str):
        """
        Strip the braces and useless stuff out of the namespace name, and set it to the object.
        """

        self.namespace = namespace.split('}')[0].strip('{') if '}' in namespace else ''


    def get_namespace_with_brace(self):
        """
        Return the book namespace with the brace, required for the `find` function

        :Example:

        The `namespace` value is "http://www.daisy.org/z3986/2005/ncx/"
        >>> get_namespace_with_brace()
        {http://www.daisy.org/z3986/2005/ncx/}
        """
        return "{" + self.namespace + "}"