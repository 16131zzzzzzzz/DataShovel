from .pdformer.pdformer import Pdformer

class PdfReader():
    def __init__(self, file_path):
        former = Pdformer(file_path)

    def read(self):
        '''
          read the document and save it into folder
        '''
        self.former.pdf2json()