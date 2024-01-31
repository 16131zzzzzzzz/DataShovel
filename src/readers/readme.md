# Document Readers
The readers are used to read the documents into a folder. One folder contains all elements in one corresponding file.
## Usage
```python
from readers.reader import Reader
reader = Reader("path/to/your_file.pdf")
reader.read()
```

## Adding new reader
1. Add the corresponding relationship between file suffix and readerclass in reader.py. For example:
```python
format2class = {
    # ... other formats
    'png': 'PngReader',
}
```

2. Add a dictionary in readers folder. The name should be `{file_extension.lower()}reader`.
```lua
reader/
|-- pngreader
```

3. Inside the new folder (`pngreader` in this case), create `__init__.py` and a new Python file (`png_reader.py`). Implement the reader class (`PngReader`). The file name should be `{file_extension.lower()}_reader`. For example:

   ```python
   # readers/pngreader/png_reader.py

   class PngReader:
       def read(self, file_path):
           # Implement the logic to read PNG files
           print(f"Reading PNG file: {file_path}")
           # ... specific reading logic for PNG
   ```

   Ensure that the filename and the class name follow the naming convention (`png_reader` for the file and `PngReader` for the class).

Feel free to follow these steps for any additional file formats you want to support. Contributions for new readers are welcome!