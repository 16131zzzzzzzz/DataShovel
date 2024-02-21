# // {
# //     "f": "input/example/subgraph.pdf",
# //     "section": null,
# //     "mode": "text"
# // }
import os
import statistics
import csv
import codecs
import numpy as np

BERT_TITLE_MODEL_PATH = "resources/pretrained_model/bert-title/model_4epoch.h5"
PRE_TRAINED_MODEL_NAME = "resources/pretrained_model/bert-base-uncased"
INFER_PATH = "datashovel/readers/pdfreader/pdformer/structurer/infer.py"
LCNET_PATH = "resources/pretrained_model/picodet_lcnet_x1_0_fgd_layout_infer"

categories = ["text", "title", "list", "table", "figure"]
category_id2name = {0:"text", 1:"title", 2:"list", 3:"table", 4:"figure"}


#User
pdf_name = "subgraph"

current_directory = os.getcwd()
input_directory = os.path.join(current_directory, 'input')
output_directory = os.path.join(current_directory, 'output', pdf_name)
pics_directory = os.path.join(output_directory, 'pics')
structure_directory = os.path.join(output_directory, 'structure')
temp_directory = os.path.join(output_directory,'temp')
results_directory = os.path.join(output_directory, 'results')

pdf_file = os.path.join(input_directory, 'example', pdf_name + '.pdf')
result_file = os.path.join(results_directory, 'result.json')