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
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OMP_THREAD_LIMIT"] = "1"
os.environ["TESSERACT_NUM_THREADS"] = "1"
from img_epub.ocr import generate_hocr
from img_epub.to_epub import create_epub
from img_epub.utils import alpha2_to_alpha3
from pathlib import Path
import argparse
import multiprocessing
from multiprocessing import Pool
from functools import partial

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

    results = []
    files = sorted(img_dir.glob("*.jpg"), key=lambda x: x.name)

    test = partial(generate_hocr, lang=alpha2_to_alpha3(args.language))
    with Pool(multiprocessing.cpu_count()-1) as p:
        print({multiprocessing.cpu_count()})
        results = list(p.imap_unordered(test, files))

    for result in results:
        print(result)
        name = result[0]
        hocr = result[1]

        with open(f"{hocr_dir}/{name}.hocr", "wb") as f:
            f.write(hocr)

    create_epub(book_id=args.id, title=args.title, author=args.author, lang=args.language, out_dir=out_dir)

if __name__ == "__main__":
    main()