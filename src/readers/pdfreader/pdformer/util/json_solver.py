import os
import json
import copy

from .util import *

class JsonSolver():
    def __init__(self, output_dir, temp_dir):
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.alayout2 = None
        self.alayout3 = None

    def range_boxes(self, dictionary, new_dict):
        if "content" in dictionary:
            content = dictionary["content"]
            new_sub_dict = {}
            for sub_box in content:
                if (len(sub_box)>5):
                    ssection = sub_box[4]
                    sub_box.pop(4)
                    new_sub_dict.setdefault(ssection, []).append(sub_box)
            new_dict["content"] = new_sub_dict
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.range_boxes(value, new_dict[key])

    def tranform_json(self,main_instance):
        with open(os.path.join(self.temp_dir, 'alayout.json'), "r") as f:
            alayout = json.loads(f.read())
        alayout2 = copy.deepcopy(alayout)
        self.range_boxes(alayout, alayout2)

        json_data = json.dumps(alayout2, indent=2)
        with open(os.path.join(self.temp_dir, 'alayout2.json'), "w") as f:
            f.write(json_data)
        self.alayout2 = alayout2
        main_instance.alayout2 = alayout2

    def split_string(self, dictionary, new_dict):
        for key, value in dictionary.items():
            if key in ["text", "image","list","table","isolated formula"]:
                new_value = {}
                for index, item in enumerate(value):
                    position = tuple(item[:4])
                    if len(item) < 6:
                        content = ""
                    else:
                        content = item[5]
                    new_item = {"position": position, "content": content}
                    new_value[str(index)] = new_item
                new_dict[key] = new_value
            elif isinstance(value, dict):
                self.split_string(value, new_dict[key])

    def split_json(self, main_instance):
        with open(os.path.join(self.temp_dir, 'alayout2.json'), "r") as f:
            self.alayout2 = json.loads(f.read())

        alayout3 = copy.deepcopy(self.alayout2)
        self.split_string(self.alayout2,alayout3)
        with open(os.path.join(self.temp_dir, 'alayout3.json'), "w") as f:
            json.dump(alayout3, f, indent=2)
        self.alayout3 = alayout3
        main_instance.alayout3 = alayout3

    def get_json(self, main_instance):
        self.tranform_json(main_instance)
        self.split_json(main_instance)