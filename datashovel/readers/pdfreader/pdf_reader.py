from .pdformer.pdformer import Pdformer
from input.config.conf import *
import json

class PdfReader():
    def __init__(self):
        self.result_file = result_file

    def read(self, file_path, args):
        '''
          read the document and save it into folder
        '''
        root_tree = Pdformer().pdf2json()
        with open(self.result_file, "w") as f:
            json.dump(root_tree, f, indent=2)