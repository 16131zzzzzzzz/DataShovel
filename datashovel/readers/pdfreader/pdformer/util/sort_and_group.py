import os
import json
import copy
from PIL import Image

from readers.pdfreader.pdformer.util.util import *
from input.config.conf import *

class SortGrouper():
    def __init__(self, textbox_file, new_bboxes, layout):
        self.PDF_file = pdf_file
        self.pics_dir = pics_directory
        self.output_dir = output_directory
        self.temp_dir = temp_directory

        #TODO
        self.textbox_file = textbox_file
        self.new_bboxes = new_bboxes

        self.layout = layout
        self.new_layout = None
        self.final_layout = None
        self.left_boxes = None
        self.final_layout2 = None

    ######优先级排序
    def sort_and_group_boxes(self, box_list, ratio = 0.6):
        # 根据矩形框的左上角横坐标进行升序排序
        sorted_boxes = sorted(box_list, key=lambda box: box[0])

        # 创建空词典，用于存储分栏结果
        column_dict = {}

        num = -1
        # 遍历排好序的矩形框列表
        for i, box in enumerate(sorted_boxes):
            # 计算当前矩形框和前一个矩形框的重合度和重合系数
            if i > 0:
                prev_box = sorted_boxes[i - 1]
                overlap_x1 = max(prev_box[0], box[0])
                overlap_x2 = min(prev_box[2], box[2])
                overlap_width = max(0, overlap_x2 - overlap_x1)
                overlap_ratio = overlap_width / min(prev_box[2] - prev_box[0], box[2] - box[0])

                # 如果重合系数大于ratio，则将当前矩形框添加到前一个矩形框所在的栏中
                if overlap_ratio > ratio:
                    column_key = f"column{num}"
                    column_dict.setdefault(column_key, [])
                    column_dict[column_key].append(box)
                    continue

            # 如果当前矩形框没有被添加到前一个矩形框所在的栏中，则将其添加到新的栏中
            num=num+1
            column_key = f"column{num}"
            column_dict.setdefault(column_key, [])
            column_dict[column_key].append(box)

        # 根据矩形框的左上角纵坐标进行升序排序
        for column in column_dict:
            sorted_boxes2 = sorted(column_dict[column], key=lambda box: box[1])
            column_dict[column] = sorted_boxes2
        return column_dict

    def sort_and_group_boxes2(self, box_list, ratio = 0.6):
    # 根据矩形框的左上角横坐标进行升序排序
        sorted_boxes = sorted(box_list, key=lambda box: box[0])

        # 创建空词典，用于存储分栏结果
        column_dict = {}

        num = -1
        # 遍历排好序的矩形框列表
        for i, box in enumerate(sorted_boxes):
            # 计算当前矩形框和前一个矩形框的重合度和重合系数
            if i > 0:
                prev_box = sorted_boxes[i - 1]
                overlap_x1 = max(prev_box[0], box[0])
                overlap_x2 = min(prev_box[2], box[2])
                overlap_width = max(0, overlap_x2 - overlap_x1)
                overlap_ratio = overlap_width / min(prev_box[2] - prev_box[0], box[2] - box[0])

                # 如果重合系数大于ratio，则将当前矩形框添加到前一个矩形框所在的栏中
                if overlap_ratio > ratio:
                    column_key = f"column{num}"
                    column_dict.setdefault(column_key, [])
                    column_dict[column_key].append(box)
                    continue

            # 如果当前矩形框没有被添加到前一个矩形框所在的栏中，则将其添加到新的栏中
            num=num+1
            column_key = f"column{num}"
            column_dict.setdefault(column_key, [])
            column_dict[column_key].append(box)

        ans_sbox=[]
        columnum = len(column_dict)
        for k in range(columnum):
            sorted_boxes2 = sorted(column_dict[f"column{k}"], key=lambda box: box[1])
            for s_box in sorted_boxes2 :
                ans_sbox.append(s_box)
        return ans_sbox

    ########去除顶端+分栏排序
    def sort_and_group_boxes3(self, box_list, pic_width, mid_ratio = 0.5, ratio = 0.6):
        # 根据矩形框的左上角横坐标进行升序排序
        sorted_boxes = sorted(box_list, key=lambda box: box[0])

        # 创建空词典，用于存储分栏结果
        column_dict = {}
        num = -1
        column_dict.setdefault(f"column{num}", [])

        # 遍历排好序的矩形框列表
        for i, box in enumerate(sorted_boxes):
            # 单独归类中间框
            if (box[2]-box[0])>= mid_ratio * pic_width :
                column_dict["column-1"].append(box)
                continue
            elif i > 0:
                prev_box = sorted_boxes[i - 1]
                overlap_x1 = max(prev_box[0], box[0])
                overlap_x2 = min(prev_box[2], box[2])
                overlap_width = max(0, overlap_x2 - overlap_x1)
                overlap_ratio = overlap_width / min(prev_box[2] - prev_box[0], box[2] - box[0])

                # 如果重合系数大于ratio，则将当前矩形框添加到前一个矩形框所在的栏中
                if overlap_ratio > ratio:
                    column_key = f"column{num}"
                    column_dict.setdefault(column_key, [])
                    column_dict[column_key].append(box)
                    continue

            # 如果当前矩形框没有被添加到前一个矩形框所在的栏中，则将其添加到新的栏中
            num=num+1
            column_key = f"column{num}"
            column_dict.setdefault(column_key, [])
            column_dict[column_key].append(box)

        # 根据矩形框的左上角纵坐标进行升序排序
        ans_sbox=[]
        for column in column_dict:
            sorted_boxes2 = sorted(column_dict[column], key=lambda box: box[1])
            for s_box in sorted_boxes2 :
                ans_sbox.append(s_box)
        return ans_sbox

    def sort_boxes(self,main_instance):
        new_layout = copy.deepcopy(self.layout)
        pages = os.listdir(self.pics_dir)
        for i,page in enumerate(pages):
            new_layout[str(i)] = self.sort_and_group_boxes(self.layout[str(i)])

        self.new_layout= new_layout
        main_instance.new_layout = new_layout
        with open(os.path.join(self.temp_dir,'layout_title2.json'), "w") as f:
            json.dump(new_layout, f, indent=2)

    def possible_boxes(self, box_list, title_box, a=20):
        # 定义一个空列表，用于存储符合条件的矩形框
        filtered_boxes = []

        # 遍历box_list中的每个矩形框
        for box in box_list:
            # 获取矩形框的起点和终点坐标
            x1, y1, x2, y2 = box[:4]
            # 先加入本身
            if (x1==title_box[0] and y1==title_box[1]):
                filtered_boxes.append(box)
            # 判断起点和终点是否都在title_box右侧
            elif x1 > (title_box[2]-a) and x2 > (title_box[2]-a):
                filtered_boxes.append(box)
            # 判断起点是否在title_box起点的下方，并且中点在title_box起点右侧
            elif y1 > title_box[1] and (x1 + x2) / 2 > title_box[0] :
                filtered_boxes.append(box)

        # 返回符合条件的矩形框列表
        return filtered_boxes

#得到一个标题的可能区域
    def possible_section(self,main_instance):
        print(len(self.new_bboxes["0"])) ##为什么会被修改？？？
        final_layout = {}
        left_boxes = {}
        pages = os.listdir(self.pics_dir)
        for i, page in enumerate(pages):
            box_choosefrom = self.new_bboxes[str(i)]
            titles = self.new_layout[str(i)]
            final_layout.setdefault(str(i), [])

            for column in reversed(list(titles.keys())): #逆序得到column
                column_titles = self.new_layout[str(i)][column]
                for item in reversed(column_titles):  #### 针对某一列下某一标题
                    section_list=[]
                    section_list.append(item)
                    filtered_boxes = self.possible_boxes(box_choosefrom, item)
                    for bbox in filtered_boxes:
                        bbox.append(i)
                    section_list.append(filtered_boxes)

                    box_choosefrom = remove_elements(box_choosefrom, filtered_boxes) ##更新候选
                    final_layout[str(i)].insert(0, section_list)###每次都插入在最前
            ###遍历完一页的column 记录一下剩下的box
            left_boxes.setdefault(str(i), [])
            left_boxes[str(i)] = box_choosefrom

        with open(os.path.join(self.temp_dir,'final_layout.json'), "w") as f:
            json.dump(final_layout, f, indent=2)
        self.final_layout = final_layout
        main_instance.final_layout = final_layout

        with open(os.path.join(self.temp_dir,'left_boxes.json'), "w") as f:
            json.dump(left_boxes, f, indent=2)
        self.left_boxes = left_boxes
        main_instance.left_boxes = left_boxes

    def sort_boxes2(self,main_instance):
        with open(os.path.join(self.temp_dir,'final_layout.json'), "r") as f:
            final_layout = json.loads(f.read())

        final_layout2 = {}
        final_layout2 = copy.deepcopy(final_layout)
        pages = os.listdir(self.pics_dir)
        pnum = len(pages)
        for i, box in enumerate(pages): ##某一页
            for x, fsection in enumerate(final_layout[str(i)]):
                final_layout2[str(i)][x][1] = self.sort_and_group_boxes2(fsection[1])
            if (i+1)<pnum :
                img_fp = os.path.join(self.pics_dir, pages[i+1])
                #字典的键为当前页面的索引"i"，值为标题信息列表。
                image = Image.open(img_fp)
                pic_width = image.size[0]
                add_boxs = self.sort_and_group_boxes3(self.left_boxes[str(i+1)], pic_width)
                for bbox in add_boxs:
                    bbox.append(i+1)
                for a_box in add_boxs:
                    final_layout2[str(i)][-1][1].append(a_box)

        self.final_layout2 = final_layout2
        main_instance.final_layout2 = final_layout2
        with open(os.path.join(self.temp_dir,'final_layout2.json'), "w") as f:
            json.dump(final_layout2, f, indent=2)

    def sort_and_group (self, main_instance):
        self.sort_boxes(main_instance)
        self.possible_section(main_instance)
        self.sort_boxes2(main_instance)