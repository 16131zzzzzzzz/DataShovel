import os
from PIL import Image
import subprocess
import json
import copy
from pix2text import Pix2Text, merge_line_texts
from pdf2image import convert_from_path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal
from tqdm import tqdm
# from PIL import ImageDraw

from .model.title_detecter import TitleDetecter
from .util.sort_and_group import SortGrouper
from .util.json_solver import JsonSolver
from .util.util import *

LCNET_PATH = "resources/pretrained_model/picodet_lcnet_x1_0_fgd_layout_infer"
current_directory = os.getcwd()
# 要创建的文件夹路径
output_directory = os.path.join(current_directory, 'output')

class Pdformer():
    def __init__(self, pdf_file, output_dir = output_directory, ):
        self.PDF_file = pdf_file  #  "test_files/papers/con5/weak.pdf"
        self.output_dir = output_dir

        self.pics_folder = os.path.join(self.output_dir, "pics")
        self.structurePath = os.path.join(self.output_dir, "structure")
        self.temp_folder = os.path.join(self.output_dir, "temp")
        self.textbox_file = os.path.join(self.temp_folder, "text_boxes.json")
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

        self.new_text_boxes = None
        self.bboxes = None

        self.new_bboxes = None
        self.layout = None

        self.new_layout = None
        self.final_layout = None
        self.left_boxes = None
        self.final_layout2 = None

        self.alayout = None
        self.alayout2 = None
        self.alayout3 = None

        self.text_boxes_from_miner = None


    def generate_pics(self):
        self.pics_folder = os.path.join(self.output_dir, "pics")
        if not os.path.exists(self.pics_folder):
            os.makedirs(self.pics_folder)
            print(self.PDF_file)
            images = convert_from_path(self.PDF_file)
            for i, image in enumerate(images):
                # 生成PNG文件的文件名
                filename = f"page-{i+1:06d}.png"  # 使用6位数字，左侧自动填充0
                # 保存PNG文件
                image_path = os.path.join(self.pics_folder, filename)
                image.save(image_path, "PNG")
                # image.save(pics_folder, "PNG")
        else:
            print("Pictures already generated")

    def generate_structured_pics(self):
        print("############################")
        if os.path.exists(self.structurePath):
            print("Structure already generated")
            return
        command = ["python", "structurer/infer.py",
                "--model_dir=" + LCNET_PATH,
                "--image_dir=" + self.pics_folder,
                "--output_dir=" +  self.structurePath,
                "--save_results"]
        # ! python structurer/infer.py --model_dir=pretrained_model/picodet_lcnet_x1_0_fgd_layout_infer --self.pics_folder --device=CPU --self.output_dir --save_results
        result = subprocess.run(command, capture_output=True, text=True)

#self.text_boxes & textbox_file
    def extract_box_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            pages = extract_pages(file)

            page_text_boxes = {}
            page_img_boxes = {}
            # 遍历每一页
            for i, page_layout in enumerate(pages):
                _, _, page_width, page_height = page_layout.bbox

                page_text_boxes[i] = []
                page_img_boxes[i] = []

                # 遍历每个元素
                for element in page_layout:
                    if isinstance(element, LTTextBoxHorizontal) or isinstance(element, LTTextLineHorizontal):
                        # 提取文本框位置信息
                        x0, y0, x1, y1 = element.bbox

                        # 提取文本内容
                        text = element.get_text().strip()

                        page_text_boxes[i].append(('text', text, x0, y0, x1, y1))

            return page_text_boxes, page_img_boxes

    def generate_test_boxes(self):
        page_text_boxes, page_img_boxes = self.extract_box_from_pdf(self.PDF_file)
        self.text_boxes_from_miner = page_text_boxes
        with open(os.path.join(self.temp_folder, 'text_boxes.json'), 'w') as f:
            json.dump(page_text_boxes, f)

# classify the bboxes
    def apply_structure_box(self):
        page_height, page_width = get_page_size(self.PDF_file)
        print (page_width)

        bboxes = {}
        with open(os.path.join(self.structurePath, "bbox.json"), "r") as f:
                    sbbox = json.load(f)
        pages = os.listdir(self.pics_folder)
        for i,page in enumerate(pages):
            for box in sbbox:
                pageNum = box["file_name"]
                if (pageNum == page):
                    x_min = box['bbox'][0]-5
                    y_min = box['bbox'][1]
                    x_max = box['bbox'][0]+box['bbox'][2]+5
                    y_max = box['bbox'][1]+box['bbox'][3]
                    y = []
                    y.append(x_min)
                    y.append(y_min)
                    y.append(x_max)
                    y.append(y_max)

                    category_id2name = {0:"text", 1:"title", 2:"list", 3:"table", 4:"figure"}
                    if (box["category_id"] in category_id2name):
                        y.append(category_id2name[box["category_id"]])
                    if (box["category_id"]!=1):
                        bboxes.setdefault(str(i), []).append(y)  #####不可忘记str化！！否则在txt中看不出来！！！！

        self.bboxes = bboxes
        with open(os.path.join(self.temp_folder, 'layout_bbox.json'), "w") as f:
            json.dump(bboxes, f, indent=2)


#isolated公式引入 速度慢
    def isolated_formula(self):
        print("####################")
        print("isolated_formula start")
        new_bboxes=copy.deepcopy(self.bboxes)
        pages = os.listdir(self.pics_folder)
        p2t = Pix2Text(analyzer_config=dict(model_name='mfd'), device='gpu')
        for i,page in enumerate(pages):
            img_fp = os.path.join(self.pics_folder, pages[i])
            outs = p2t(img_fp, resized_shape=600)
        #####out的格式：左上角起顺时针 y为到图片上方的距离
        #####铭记：除了text_boxes y都为到图片上方的距离！！！！！！！！！

            for formula in outs:
                if (formula['type'] == 'isolated'):
                    new_box = formula['position']
                    new_box1 = new_box[[0, 2]].flatten().tolist()
                    new_box1.append('isolated formula')
                    new_bboxes[str(i)].append(new_box1)

        with open(os.path.join(self.temp_folder, 'layout_bbox2.json'), "w") as f:
            json.dump(new_bboxes, f, indent=2)

        self.new_bboxes = new_bboxes

    def Pix2Text_ocr(self):
        pages = os.listdir(self.pics_folder)
        p2t = Pix2Text(analyzer_config=dict(model_name='mfd'), device='gpu')
        all_image = [Image.open(os.path.join(self.pics_folder, pages[i])) for i in range(len(pages))]
        for i, box in tqdm(enumerate(pages)): ##某一页
            for fsection in self.final_layout2[str(i)]:
                for ffbox in fsection[1]:
                    left, top, right, bottom = ffbox[:4]
                    ybox = (left, top, right, bottom)
                    cropped_img = all_image[ffbox[5]].crop(ybox)
                    try:
                        outs = p2t(cropped_img, resized_shape=600)
                    except Exception as e:
                        print(f"Skipping box outside image bounds: {ffbox}")
                        continue
                    only_text = merge_line_texts(outs, auto_line_break=True)
                    ffbox.append(only_text)

        with open(os.path.join(self.temp_folder, 'final_layout2.json'), "w") as file:
            json.dump(self.final_layout2, file, indent=2)

    def check_overlap(self, boxa, boxb, threshold = 0.8):
        """
        检查两个框之间的重叠部分是否超过指定的阈值
        """
        left_a, top_a, right_a, bottom_a = boxa
        left_b, top_b, right_b, bottom_b = boxb
        overlap_left = max(left_a, left_b)
        overlap_top = max(top_a, top_b)
        overlap_right = min(right_a, right_b)
        overlap_bottom = min(bottom_a, bottom_b)
        
        overlap_width = max(0, overlap_right - overlap_left)
        overlap_height = max(0, overlap_bottom - overlap_top)
        
        overlap_area = overlap_width * overlap_height
        boxb_area = (right_b - left_b) * (bottom_b - top_b)
        overlap_ratio = overlap_area / boxb_area

        return overlap_ratio > threshold

    def Layout2Text(self):
        print("####################")
        print("Layout2Text start")
        if self.text_boxes_from_miner is None:
            with open(os.path.join(self.output_dir, 'text_boxes.json'), 'r') as f:
                temp_miner = json.load(f)
            for key, value in temp_miner.items():
                self.text_boxes_from_miner[int(key)] = value

        pages = os.listdir(self.pics_folder)
        print(pages)
        page2box2text = [{(box[2]*200/72, 2200-box[5]*200/72, box[4]*200/72, 2200-box[3]*200/72):box[1] for box in self.text_boxes_from_miner[i]} for i in range(len(pages))]
        for i, box in tqdm(enumerate(pages)): ##某一页
            ###############
            # img_fp = os.path.join(self.pics_folder, pages[i])
            # image = Image.open(img_fp)
            # draw = ImageDraw.Draw(image)
            # for bbox in box2text:
            #     draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline="red", width=2)
            ###############
            for idx_fsection, fsection in enumerate(self.final_layout2[str(i)]):
                for idx_ffbox, ffbox in enumerate(fsection[1]):
                    left, top, right, bottom = ffbox[:4]
                    ###############
                    # draw.rectangle([left, top, right, bottom], outline="blue", width=2)
                    # draw.text((left, top), str(idx_fsection) + ", "+ str(idx_ffbox), fill="black")
                    ###############
                    ybox = (left, top, right, bottom)
                    only_text = ""
                    box2text = page2box2text[ffbox[5]]
                    for box in box2text:
                        if self.check_overlap(ybox, box):
                            only_text += box2text[box]
                            only_text += "\n"
                    ffbox.append(only_text)
            ###############
            # image.save(f"output/pics_miner/boxed_image_{i}.png")
            ###############

        with open(os.path.join(self.temp_folder, 'final_layout2.json'), "w") as file:
            json.dump(self.final_layout2, file, indent=2)

    def supplement_title(self):
        with open(os.path.join(self.temp_folder, 'final_layout2.json'), "r") as file:
            json_data = file.read()
        self.final_layout2 = json.loads(json_data)
        alayout = {}
        temp_title = {}
        temp_title["0"] = ""
        temp_title["1"] = ""
        temp_title["2"] = ""
        temp_title["3"] = ""
        temp_title["4"] = ""
        ##4 更新了 但4.1没更新 导致错位3.4
        # titleset = []
        # for i, box in enumerate(pages): ##某一页
        #     for titlef in final_layout2[str(i)]:
        #         ptitle = titlef[0][4]
        #         titleset.append(ptitle)
        pages = os.listdir(self.pics_folder)
        for i, box in enumerate(pages): ##某一页
            for titlef in self.final_layout2[str(i)]:
                ptitle = titlef[0][4]
                title_level = get_title_level(ptitle)
                if (title_level==0):
                    temp_title[str(title_level)] = ptitle
                    alayout[ptitle]= {}
                    for pbox in titlef[1]:
                        alayout[ptitle].setdefault("content", []).append(pbox)
                else:
                    if temp_title[str(title_level-1)] != "":
                        temp_title[str(title_level)] = ptitle
                        parentl = alayout
                        for t in range(title_level):  ###找到上一级 导致错位
                            if temp_title[str(t)] in parentl:
                                parentl = parentl[temp_title[str(t)]]
                        parentl[ptitle]= {}
                        for pbox in titlef[1]:
                            parentl[ptitle].setdefault("content", []).append(pbox)

        self.alayout = alayout
        with open(os.path.join(self.temp_folder, 'alayout.json'), "w") as file:
            json.dump(alayout, file, indent=2)

    def pdf2json(self):
        self.generate_pics()
        self.generate_structured_pics()
        self.generate_test_boxes()

        TitleDetecter(self.PDF_file, self.textbox_file, self.pics_folder, self.output_dir, self.temp_folder).detector(self)
        # self.bert_title()
        # self.merge_title()
        
        self.apply_structure_box()
        self.isolated_formula()

        SortGrouper(self.PDF_file, self.textbox_file, self.pics_folder,self.new_bboxes,self.layout, self.output_dir, self.temp_folder).sort_and_group(self)
        # self.sort_boxes()
        # self.possible_section()
        # self.sort_boxes2()
        
        self.Pix2Text_ocr()
        # self.Layout2Text()
        self.supplement_title()
        
        JsonSolver(self.output_dir, self.temp_folder).get_json(self)
        # self.tranform_json()
        # self.split_json()

    def modify_dict(self, dictionary,new_dict):
        new_dict["content"] = {}