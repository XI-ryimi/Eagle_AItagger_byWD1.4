import os
import re
import sys
import csv
import json
from pathlib import Path

def YorN(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print('无效输入，请输入 Y 或 N 。')

# 工作目录
print('建议每次处理不超过1W张')
print('AI标记tags的前处理是否已完成？')
print('粘贴从[Eagle]获取的图片路径')
print("-"*50)
'''
while True:

    img_input_list = input()
    img_input_list = re.sub(r'([a-zA-Z]:\\)', r' \1',  img_input_list)
    img_input_list = re.sub(r'\s+([a-zA-Z]:\\)', r' \1',  img_input_list)
    img_input_list = img_input_list.strip()

    if img_input_list.endswith(',,'):
        img_input_list = img_input_list[:-2]
        print('怎么会有人从秋叶训练器的文本框中复制带[,,]的路径？')
        print('！！！路径已规格化！！！')

    re_work_dir = r'([a-zA-Z]:\\.*?\.library)\\.*?\.info\\'
    work_dir = re.search(re_work_dir, img_input_list)
    work_dir = work_dir.group(1)

    if work_dir.endswith('.library'):
        print('Eagle资源库路径：', work_dir)
        print("-"*50)
        break

    print('路径异常：', work_dir)
'''    



img_input_list = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KIMT6M81GAYYH.info\005O0CJZly1gl7bm0ib57j30u01bwe81.png E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLAP6UB.info\tb_image_share_1594047317053.jpg E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLT4C8B.info\1594047078060.jpg'
work_dir = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library'
print('Eagle资源库路径：', work_dir)
print("-"*50)




img_list = [
    Path(p.strip()) 
    for p in img_input_list.split(" ")
]

img_list_FatherPath = [
    Path(path).parent 
    for path in img_list
]

txt_list = [
    list(directory.glob('*.txt')) or None 
    for directory in img_list_FatherPath
]

json_list = [
    list(directory.glob('*.json')) or None 
    for directory in img_list_FatherPath
]

combined_list = [
    (img_path, txt_list[idx], json_list[idx])
    for idx, img_path in enumerate(img_list)
]

combined_list_DelGroups = [
    item for item in combined_list 
    if None in item
]

for item in combined_list_DelGroups: 
    print('txt或json文件缺失的图片文件路径：')
    print(item[0])
    print("-"*50)

# 从 combined_list 中删除包含 None 元素的组
combined_list = [item for item in combined_list if None not in item]
print(f'待处理{len(combined_list)}个图片')
print("-"*50)


# 多线程环境检测
if YorN("是否启用多线程？几百张图片不用开启。(Y/N):"):
    import multiprocessing
    if multiprocessing.cpu_count() > 1:
        print('CPU支持多线程')
        print("-"*50)
    else:
        print('CPU不支持多线程。')
        input('按回车键回到单线程')
        print("-"*50)



def TagsToJson(file):
    img_working = file[0]
    txt_working = file[1]
    json_working = file[2]
     
    print(f'(正在处理文件: {img_working})')
    
    # 汉化tags
    if YorN("是否对tags进行汉化？(Y/N): "):
        print('开始汉化tags...')
        # 检查工作环境
        script_dir = os.path.dirname(os.path.abspath(__file__)) # 当前脚本所在目录
        TransDic_path = os.path.join(script_dir, 'Tags-zh.csv') # 翻译字典文件路径
        TransDic_data = {}
        try:
            with open(TransDic_path, 'r', encoding='utf-8-sig') as f:
                TransDic_ToRead = csv.reader(f)
                for row in TransDic_ToRead:
                    if len(row) < 2:
                        print(f'(警告，值不足的行：{row})')
                        continue
                    key, value = row[0], row[1]
                    TransDic_data[key] = value
        except Exception as e:
            print(f'(读取翻译字典文件失败: {e})')

    # 读取txt，从tags中删除不必要的标签
    txt_working = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLT4C8B.info\1594047078060.txt'

    re_tags_ToDel_1 = r'(?:\d|\d_|multiple_)(?:girl|boy|girls|boys)'
    re_tags_ToDel_2 = r'\b\w+_(?:quality|background)\b'
    re_tags_ToDel_3 = r'solo|masterpiece|illustration'
    re_tags_ToDel_4 = r'^[\s,]+|[\s,]+$'

    try:
        with open(txt_working, 'r', encoding='utf-8') as f:
            txt_OriTags = f.read()
            txt_CleanedTags = re.sub(re_tags_ToDel_1, '', txt_OriTags)
            txt_CleanedTags = re.sub(re_tags_ToDel_2, '', txt_CleanedTags)
            txt_CleanedTags = re.sub(re_tags_ToDel_3, '', txt_CleanedTags)
            txt_CleanedTags = txt_CleanedTags.replace(' ,', '')
            txt_CleanedTags = re.sub(re_tags_ToDel_4, '', txt_CleanedTags)

            txt_Tags_list = [
                tag.strip() 
                for tag in txt_CleanedTags.split(', ') 
                if tag.strip()
            ]

    except Exception as e:
        print(f'(读取{txt_working}文件失败: {e})')
        txt_except_list.append(txt_working)

    # 汉化tags
    txt_CNTags = [
        TransDic_data.get(tag) 
        for tag in txt_Tags_list 
        if TransDic_data.get(tag) is not None
    ]

    # tag写入json
    try:
        with open(json_working, 'r', encoding='utf-8') as f:
            json_working_data = json.load(f)
            json_working_tags = json_working_data.get("tags",[])
            new_tags = [
                tag for tag in txt_CNTags 
                if tag not in json_working_tags
            ]
            if new_tags:
                json_working_tags.extend(new_tags)
                json_working_data['tags'] = json_working_tags
                with open(json_working, 'w', encoding='utf-8') as f:
                    json.dumo(json_working_data, f, ensure_ascii=False)
            else:
                print(f'({json_working}没有新tag需要写入)')
    except json.JSONDecodeError as e:
        print(f'(json文件{json_working}解析错误: {e})')
        json_except_list.append(json_working)

def process_files(file_list, use_multiprocessing):
    if use_multiprocessing:
        # 使用多线程处理
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(TagsToJson, file_list)
    else:
        # 使用单线程处理
        for file in file_list:
            TagsToJson(file)

# 使用示例
file_list = ['file1.txt', 'file2.txt', 'file3.txt']
use_multiprocessing = YorN("是否启用多线程？一千张以下的图片不用开启。(Y/N):")
process_files(file_list, use_multiprocessing)


txt_except_list = []
json_except_list = []

if combined_list:
    combined_work = combined_list[0]

except_list = txt_except_list + json_except_list
print('文件处理完成')
print(f'({len(except_list)}：\n{except_list})')


# 处理进度条
# 异常文件报错

