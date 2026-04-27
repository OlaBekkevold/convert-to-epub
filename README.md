# convert-to-epub

A tool for generating epubs from different formats using Tesseract OCR 

## Project Status

This project is still a very early work-in-progress. As of now it only supports converting images and there are
many edge cases (and normal cases) that won't work. The main focus right now is to get image conversion working properly
and later expand the scope to other formats.

The language support is limited to the languages supported by Tesseract

The generated epub is a mess

## Usage

### Requirements

- uv
- Tesseract

### Installation

1. Clone the repository and enter the directory
2. `uv sync`
3. `uv run img_epub input/dir output/dir <Unique identifier> <Book title> <Book author> <ISO 639-1 language>`
4. Hopefully you will end up with some sort of epub