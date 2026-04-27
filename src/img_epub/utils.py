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

import sys

import pycountry

# TODO: pycountry should later be replaced by a full dictionary limited to the languages supported by Tesseract
# Support for macro languages (Currently just Norwegian) as Tesseract doesn't differentiate between them while epublib does
macro_dict = {
    "nb": "nor",
    "nn": "nor",
}

# The user is expected to input language in ISO 639-1 format, this will be converted to ISO 639-2 for use with Tesseract
def alpha2_to_alpha3(lang_code):
    alpha3 = ""
    if lang_code in macro_dict:
        alpha3 = macro_dict[lang_code]
    else:
        alpha3 = pycountry.languages.get(alpha_3=lang_code)

    if alpha3 is None:
        print(f"Error Unknown language: {lang_code}")
        sys.exit(1)

    return alpha3


