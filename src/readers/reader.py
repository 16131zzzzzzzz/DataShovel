class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.format_reader = self._create_format_reader()
        self.read()

    def _create_format_reader(self):
        file_extension = self.file_path.split('.')[-1].lower()

        format2class = {
            'pdf': 'PdfReader',
            'xlsx': 'XlsxReader',
            'rst': 'RstReader',
        }

        if file_extension in format2class:
            reader_class_name = format2class[file_extension]
            reader_module = f"readers.{file_extension.lower()}reader.{file_extension.lower()}_reader"
            
            reader_class = getattr(__import__(reader_module, fromlist=[reader_class_name]), reader_class_name)
            
            return reader_class()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def read(self, args):
        '''
          read the document and save it into folder
        '''
        if hasattr(self.format_reader, 'read'):
            return self.format_reader.read(self.file_path, args)
        else:
            raise NotImplementedError(f"Format reader {self.format_reader.__class__.__name__} does not have read method")
    

        
