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


from img_epub.ocr import generate_hocr
from img_epub.to_epub import create_epub
from img_epub.utils import alpha2_to_alpha3
from pathlib import Path
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("input", help="Input directory")
parser.add_argument("data", help="Output directory")

parser.add_argument("id", help="Unique identifier")
parser.add_argument("title", help="Book title")
parser.add_argument("author", help="Author name")
parser.add_argument("language", help="Language")


args = parser.parse_args()

def main():

    if len(args.language) != 2:
        parser.error(f"Language should be in ISO 639-1(Two character) format: {args.language}")

    img_dir = Path(args.input)

    if not img_dir.exists():
        parser.error(f"Input directory does not exist: {img_dir}")
    if not img_dir.is_dir():
        parser.error(f"Input directory is not a directory: {img_dir}")

    img_dir = img_dir.resolve()

    out_dir = Path(args.data)

    if not out_dir.exists():
        parser.error(f"Output directory does not exist: {out_dir}")

    if not out_dir.is_dir():
        parser.error(f"Output directory is not a directory: {out_dir}")

    out_dir = out_dir.resolve()

    hocr_dir = Path(f"{out_dir}/hocr")

    hocr_dir.mkdir(exist_ok=True)


    files = sorted(img_dir.glob("*.jpg"), key=lambda x: x.name)
    for entry in files:
       if entry.is_file():
         hocr = generate_hocr(entry, alpha2_to_alpha3(args.language))

         with open(f"{hocr_dir}/{entry.name.split(".")[0]}.hocr", "wb") as f:
             f.write(hocr)

    create_epub(book_id=args.id, title=args.title, author=args.author, lang=args.language, out_dir=out_dir)

if __name__ == "__main__":
    main()