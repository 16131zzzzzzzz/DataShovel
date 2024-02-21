import os
import json
import sys
import argparse
from input.config.conf import *
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

PROJECT_NAME = "DataShovel-main"
if not os.getcwd().endswith(PROJECT_NAME):
    os.chdir(os.path.join(os.getcwd()[:os.getcwd().find(PROJECT_NAME)], PROJECT_NAME))
sys.path.append(os.getcwd())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_name', default=pdf_name, help='input file')    
    parser.add_argument('--input_directory', default=input_directory, help='the input dir')
    parser.add_argument('--output_directory', default=output_directory, help='the output dir')
    # parser.add_argument('--section', default=None, help='Specify the section')
    # parser.add_argument('--mode', default='normal', help='output mode')

    args = parser.parse_args()

    # with open('input/config/conf.json', 'r') as file:
    #     config = json.load(file)

    # if args.f:
    #     args.file = config['f']
    # if args.section:
    #     args.section = config['section']
    # if args.mode:
    #     args.mode = config['mode']
    # filepath = config['f']
    # section = config['section']
    # mode =  config['mode']
    # anspath = args.anspath

    # pdf_object = Pdformer(filepath)
    # pdf_object.pdf2json()

    # with open('output/temp/alayout3.json', "r") as f:
    #     alayout3 = json.loads(f.read())

    # if section != None:
    #     alayout3 = find_content(alayout3, section)

    # os.makedirs(anspath, exist_ok=True)
    # with open(os.path.join(anspath,"ans_section.json"), "w") as f:
    #     json.dump(alayout3, f, indent=2)

    # part_list = ["text", "image","list","table","isolated formula"]
    # if mode != 'normal':  #text
    #     remove_elements_from_list(part_list, mode)
    #     remove_keys_from_nested_dict(alayout3, part_list)

    # with open(os.path.join(anspath,"ans.json"), "w") as file:
    #     json.dump(alayout3, file, indent=2)

if __name__ == '__main__':
    main()