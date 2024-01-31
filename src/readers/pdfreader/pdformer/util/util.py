import re
import pdfplumber

def find_content(dictionary, title):
    if title in dictionary:
        return dictionary[title]
    else:
        for key, value in dictionary.items():
            if isinstance(value, dict):
                result = find_content(value, title)
                if result is not None:
                    return result
    return None

def remove_elements_from_list(lst, elements_to_remove):
    for element in elements_to_remove:
        if element in lst:
            lst.remove(element)

def remove_keys_from_nested_dict(dictionary, keys_to_remove):
    if isinstance(dictionary, dict):
        keys = list(dictionary.keys())  # 创建键的副本，以便在遍历时进行修改
        for key in keys:
            value = dictionary[key]
            if key in keys_to_remove:
                del dictionary[key]  # 删除当前键值对
            else:
                remove_keys_from_nested_dict(value, keys_to_remove)  # 递归调用处理嵌套的字典
    elif isinstance(dictionary, list):
        for item in dictionary:
            remove_keys_from_nested_dict(item, keys_to_remove)  # 递归调用处理嵌套的列表

def string_filter(s):
    """
    判断字符串是否以数字开头并且按空格切割后长度至少为2
    """
    # 判断字符串是否为空
    if not s:
        return False
    # 按空格切割字符串
    parts = s.split()
    # 判断切割后的长度是否至少为2
    if len(parts) < 2:
        return False
    # 判断第一个单词是否以数字开头
    first_word = parts[0]
    if not first_word[0].isdigit():
        return False
    # 字符串满足条件，返回True
    return True

def is_word(string):
    # 将字符串转换为小写，并去除空格
    string = string.lower().replace(" ", "")
    # 判断字符串是否为单词
    return string in ["introduction", "abstract", "reference", "references", "acknowledgments", "acknowledgment","acknowledgements", "acknowledgement"]

def split_string_to_boxes(box, new_list):
    # 将字符串按行拆分
    lines = box[1].split("\n")
    # 遍历每一行文本，将其存储在一个新的box中，并将该box添加到新的box列表中
    for line in lines:
        new_box = [line, box[2], box[3], box[4], box[5]]
        new_list.append(new_box)

###筛选text_box
def get_page_size(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page_1 = pdf.pages[0]
        return page_1.height, page_1.width

def box_compare(a,b):
  # print(a)
  # print(b)
  if (a[4]<=b[4] and a[1]>=b[1] and a[2]>=b[2] and a[3]<=b[3]):
    print(a)
    print(b)
    return 1
  elif (a[4]>=b[4] and a[1]<=b[1] and a[2]<=b[2] and a[3]>=b[3]):
    print(a)
    print(b)
    return 2
  else:
    return 0

def coder(i):
    section_str = "section{}".format(i)
    return section_str

def remove_elements(a, b):
    for item in b:
        if item in a:
            a.remove(item)
    return a

def get_title_level(title):
    count = 0
    # 按空格分割标题
    words = title.split()
    s = words[0]
    print (s)
    pattern = r"\.\d+"  # 匹配点+数字的组合
    matches = re.findall(pattern, s)

    return len(matches)
