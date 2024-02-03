# from .pdformer.pdformer import Pdformer
from .paper_reader.src.pdf_reader import pdf_reader

class PdfReader():
    def __init__(self, file_path, output_path):
        # self.former = Pdformer(file_path)
        self.file_path = file_path
        self.output_path = output_path
        self.reader = pdf_reader(file_path, output_path, "lcnet", "CPU")

    def read(self):
        '''
          read the document and save it into folder
        '''
        # self.former.pdf2json()
        self.reader.pdf_to_txt()