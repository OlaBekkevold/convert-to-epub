# This file is part of convert-to-epub.
# Copyright (c) 2026 Ola Kirkaune Bekkevold <ola.k.bekkevold@gmail.com>
#
# convert-to-epub is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# convert-to-epub is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with convert-to-epub.  If not, see <http://www.gnu.org/licenses/>.

from ebooklib import epub
from pathlib import Path
from bs4 import BeautifulSoup


def create_epub(book_id : str, title : str, author : str, lang : str, out_dir : Path):
    book = epub.EpubBook()

    book.set_identifier(book_id)
    book.set_title(title)
    book.set_language(lang)
    book.add_author(author)

    path = Path(f"{out_dir}/hocr")
    files = sorted(path.glob("*.hocr"), key=lambda x: x.name)

    chapters = []

    for i, entry in enumerate(files):
        with open(entry, "r") as f:
            soup = BeautifulSoup(f, "html.parser")
            body = soup.find("body")
            content_html = str(body) if body else str(soup)


            chapter_id = f"c{i}"
            chapter = epub.EpubHtml(title=chapter_id, file_name=f"{chapter_id}.xhtml", lang=lang)
            chapter.content = f"<html><body>{content_html}</body></html>"

            book.add_item(chapter)
            chapters.append(chapter)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + chapters

    epub_dir = Path(f"{out_dir}/epub")

    epub_dir.mkdir(exist_ok=True)

    epub.write_epub(f"{epub_dir}/{title}.epub", book)
    print("done")

