import os
import re
import csv
import json
import sys
import multiprocessing
import concurrent.futures
from pathlib import Path

# 对单个文件的处理
def TagsToJson(file) -> None:
    img_working, txt_working, json_working = file
     
    print(f'正在处理文件: {img_working}')

    # 读取txt，从tags中删除不必要的标签
    re_tags_ToDel_1 = r'(?:\d|\d_|multiple|multiple_)(?:girl|boy|girls|boys)'
    re_tags_ToDel_2 = r'\b\w+_(?:quality|background)\b'
    re_tags_ToDel_3 = r'solo|masterpiece|illustration'
    re_tags_ToDel_4 = r'^[\s,]+|[\s,]+$'

    try:
        with txt_working.open(mode = 'r', encoding='utf-8') as f:
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

            # 汉化tags
            if TransIf is False:
                txt_CNTags = txt_Tags_list
            else:
                txt_CNTags = [
                    TransDic_data.get(tag, tag)
                    for tag in txt_Tags_list 
                ]
    except Exception as e:
        print(f'txt文件{txt_working}读取失败: {e}')
        txt_except_list.append(txt_working)
    
    # tag写入json
    try:
        with json_working.open(mode = 'r', encoding='utf-8') as f:
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
                    json.dump(json_working_data, f, ensure_ascii=False)
            else:
                print(f'{json_working}没有新tag需要写入')
    except json.JSONDecodeError as e:
        print(f'json文件{json_working}解析错误: {e}')
        json_except_list.append(json_working)

# 多线程 

# 工作目录
print('每次处理不建议超过1W张，根据你的电脑性能自行决定要处理的图片数量')
print('AI标记tags的前处理是否已完成？')
print(f'粘贴从[Eagle]获取的图片路径\n{"-"*50}')

txt_except_list = []
json_except_list = []
TransDic_data = {}
combined_list = []
use_multithread: bool
TransIf: bool

while True:
    img_input_list = input()
    img_input_list = re.sub(r'([a-zA-Z]:\\)', r' \1',  img_input_list)
    img_input_list = re.sub(r'\s+([a-zA-Z]:\\)', r' \1',  img_input_list)
    img_input_list = img_input_list.strip()

    if img_input_list.endswith(',,'):
        img_input_list = img_input_list[:-2]
        print('怎么会有人从秋叶训练器的文本框中复制带[,,]的路径？')
        print('----------路径已规格化----------')

    re_work_dir = r'([a-zA-Z]:\\.*?\.library)\\.*?\.info\\'
    work_dir = re.search(re_work_dir, img_input_list)
    work_dir = work_dir.group(1)

    if work_dir.endswith('.library'):
        print(f'\n{"-"*50}Eagle资源库路径：{work_dir}\n{"-"*50}')
        break

    print('路径异常：', work_dir)

img_list = [
    Path(p.strip()) 
    for p in img_input_list.split(" ")
]

img_list_FatherPath = [
    Path(path).parent 
    for path in img_list
]

txt_list = [
    file for directory in img_list_FatherPath
    for file in directory.glob('*.txt') or None
]
print(txt_list)
json_list = [
    file for directory in img_list_FatherPath
    for file in directory.glob('*.json') or None
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
    print(f'{item[0]}\n{"-"*50}')

# 从 combined_list 中删除包含 None 元素的组
combined_list = [
    item for item in combined_list 
    if None not in item
]

print(f'待处理{len(combined_list)}个图片\n{"-"*50}')

# 汉化tags
while True:
    user_input = input("是否对tags进行汉化？(Y/N): ").strip().lower()
    if user_input == 'y':
        TransIf = True
        break
    elif user_input == 'n':
        TransIf = False
        break
    else:
        print('无效输入，请输入 Y 或 N ')

if TransIf is True:
    # 检查工作环境
    script_dir = os.path.dirname(os.path.abspath(__file__)) # 当前脚本所在目录
    TransDic_path = os.path.join(script_dir, 'Tags-zh.csv') # 翻译字典文件路径
    TransDic_data = {}
    try:
        with open(TransDic_path, 'r', encoding='utf-8-sig') as f:
            TransDic_ToRead = csv.reader(f)
            for row in TransDic_ToRead:
                if len(row) < 2:
                    print(f'警告，字典翻译缺失不足的行：{row}')
                    continue
                key, value = row[0], row[1]
                TransDic_data[key] = value
    except Exception as e:
        print(f' 读取翻译字典文件失败: {e}')
        input('按回车键退出')
        sys.exit(0)

# 多线程环境检测
if multiprocessing.cpu_count() == 1:
    print(f'CPU不支持多线程，将使用单线程处理\n{"-"*50}')
    use_multithread = False
else:
    print(f'CPU支持多线程\n{"-"*50}')
    use_multithread = True

# 线程池
if use_multithread == False:
    # 使用单线程处理
    for file in combined_list:
        TagsToJson(file)
else:
    num_cores = os.cpu_count()
    executor_name = "MyThreadPool"
    # 创建线程池，线程数量等于CPU核心数的两倍
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores * 2) as executor:
        # 使用线程池提交任务
        results = [executor.submit(TagsToJson, file) for file in combined_list]
        concurrent.futures.wait(results)
if combined_list:
    if txt_except_list or json_except_list:
        except_list = txt_except_list + json_except_list
        print(f'{len(except_list)}个异常文件：\n{except_list}')
    print(f'文件处理完成\n{"-"*50}')
# 删除所有txt文件
for txt_file in txt_list:
    try:
        os.remove(txt_file)
        print(f'已删除文件: {txt_file}')
    except Exception as e:
        print(f'删除文件失败 {txt_file}: {e}')