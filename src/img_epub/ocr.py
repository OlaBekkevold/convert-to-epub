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

import pytesseract
from pathlib import Path

def generate_hocr(img : Path, lang : str):
    print(f"Generating hocr for {img}")
    hocr = pytesseract.image_to_pdf_or_hocr(image=f"data/img/{img.name}", extension='hocr', lang=lang)

    return hocr
