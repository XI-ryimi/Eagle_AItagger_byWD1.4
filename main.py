import os
import re
import sys
import csv
from pathlib import Path



def YorN(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("无效输入，请输入'Y'或'N'。")



# 工作目录
print('建议每次处理不超过1W张')
print("AI标记tags的前处理是否已完成？")
print("粘贴从[Eagle]获取的图片路径")
print("-"*50)
'''
while True:

    img_input_list = input()
    img_input_list = re.sub(r'([a-zA-Z]:\\)', r' \1',  img_input_list)
    img_input_list = re.sub(r'\s+([a-zA-Z]:\\)', r' \1',  img_input_list)
    img_input_list = img_input_list.strip()

    if img_input_list.endswith(',,'):
        img_input_list = img_input_list[:-2]
        print("怎么会有人从秋叶训练器的文本框中复制带[,,]的路径？")
        print("！！！路径已规格化！！！")

    re_work_dir = r'([a-zA-Z]:\\.*?\.library)\\.*?\.info\\'
    work_dir = re.search(re_work_dir, img_input_list)
    work_dir = work_dir.group(1)

    if work_dir.endswith('.library'):
        print("Eagle资源库路径：", work_dir)
        print("-"*50)
        break

    print("路径异常：", work_dir)
'''    

img_input_list = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KIMT6M81GAYYH.info\005O0CJZly1gl7bm0ib57j30u01bwe81.png E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLAP6UB.info\tb_image_share_1594047317053.jpg E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLT4C8B.info\1594047078060.jpg'
work_dir = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library'
print("Eagle资源库路径：", work_dir)
print("-"*50)

img_list = [Path(p.strip()) for p in img_input_list.split(" ")]

img_list_FatherPath = [Path(path).parent for path in img_list]

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

combined_list_deleted_groups = [
    item for item in combined_list 
    if None in item
]

# 打印这些组的第一个元素
for item in combined_list_deleted_groups: 
    print("txt或json文件缺失的图片文件路径：", item[0])
    print("-"*50)


# 从 combined_list 中删除包含 None 元素的组
combined_list = [item for item in combined_list if None not in item]
print(f'待处理{len(combined_list)}个图片')
print("-"*50)


# 多线程环境检测
if YorN("是否启用多线程？几百张图片不用开启。(Y/N):"):
    import multiprocessing
    if multiprocessing.cpu_count() > 1:
        print("CPU支持多线程")
        print("-"*50)
    else:
        print("CPU不支持多线程。")
        input("按回车键回到单线程")
        print("-"*50)

def A(file):
    # 这里实现处理文件的逻辑
    print(f"正在处理文件: {file}")

def process_files(file_list, use_multiprocessing):
    if use_multiprocessing:
        # 使用多线程处理
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(A, file_list)
    else:
        # 使用单线程处理
        for file in file_list:
            A(file)

# 使用示例
file_list = ['file1.txt', 'file2.txt', 'file3.txt']
use_multiprocessing = YorN("是否启用多线程？一千张以下的图片不用开启。(Y/N):")
process_files(file_list, use_multiprocessing)



# 汉化tags

if YorN("是否对tags进行汉化？(Y/N): "):
    print("开始汉化tags...")
    # 检查工作环境
    script_dir = os.path.dirname(os.path.abspath(__file__)) # 当前脚本所在目录
    TransDic_path = os.path.join(script_dir, 'Tags-zh.csv') # 翻译字典文件路径
    TransDic_data = {}
    try:
        with open(TransDic_path, 'r', encoding='utf-8-sig', newline='') as f:
            TransDic_ToRead = csv.reader(f)
        for row in TransDic_ToRead:
            if len(row) < 2:
                print(f"警告，值不足的行：{row}")
                continue
            key, value = row[0], row[1]
            TransDic_data[key] = value
    except Exception as e:
        print(f"读取翻译字典文件失败: {e}")

   

# EN_tags to CN_tags


combined_work = []  # combined_work 从 combined_list 获取一个组
img_working = combined_work[0]
txt_working = combined_work[1]
json_working = combined_work[2]

# 读取txt，从tags中删除不必要的标签
txt_working = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KIMT6M81GAYYH.info\005O0CJZly1gl7bm0ib57j30u01bwe81.txt'

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

        print("调试信息，txt_OriTags：", txt_OriTags)
        print("-"*50)
        print("调试信息，txt_CleanedTags：", txt_CleanedTags)
        print("-"*50)
        print("调试信息，txt_Tags_list：", txt_Tags_list)

except Exception as e:
    print(f"读取{txt_working}文件失败: {e}")

# 汉化tags

# tag写入json
# 处理进度条
# 异常文件报错

'''
#txt文件夹路径
txt_dir = os.path.join(script_dir, "_txt") #定位到根目录下_txt
print("txt文件夹路径：",txt_dir)

txt_list = []  # 存储txt文件名的列表

# 遍历目录
for root, dirs, files in os.walk(txt_dir):
    for file in files:
        if file.endswith('.txt'):  # 确保处理的是txt文件      
            txt_file = os.path.join(root, file)
            txt_name, ext = os.path.splitext(file)
            txt_list.append(txt_name)

if not txt_list:
            print("错误：未找到任何txt文件。")
            input("按回车键退出...")
            os._exit(0)
else:
    print(f"正在处理{txt_file}")    
    
   
# 查找同名图片
images_list = [] #存放被处理的图片
images_list = [filename for filename in img_names if filename in txt_list]
print("匹配的文件:",images_list)
images_paths = [os.path.normpath(img_data_str.get(filename)) for filename in images_list]
#print("匹配图片的路径：",images_paths)


# 遍历图片和标签
for img_name in txt_list:
    img_path = img_data_str.get(img_name)
    if img_path:
        metadata_path = os.path.join(img_path, 'metadata.json')
        if os.path.exists(metadata_path):
            try:
            # 尝试加载 JSON 数据
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    json_tags = data.get("tags", [])
                    #print("原始tag:", json_tags)
            except json.JSONDecodeError as e:
                # JSON 解析错误，打印错误信息和出错的文件路径
                print(f"JSON文件解析错误: {metadata_path}")
                print(f"错误信息: {str(e)}")
            
            # 获取图片对应的txt文件名
            txt_file_name = f"{img_name}.txt"
            txt_file_path = os.path.join(txt_dir, txt_file_name)
            
            # 读取标签序列
            with open(txt_file_path, 'r', encoding='utf-8') as f:
                txt_tags = f.read()
                Test = r"^.*(?:, .*)*$"
        
                #检查标签序列是否正确     
                if not re.match(Test,txt_tags):
                    print(f"{txt_name}.txt不是WD1.4标记的文件。")
                    input("按回车键退出...")
                    os._exit(0)
                else:
                    # 格式化标签
                    
                    print("tags:",txt_tags)

            # 合并tags并更新JSON数据
            new_tags = [tag for tag in txt_tags if tag not in json_tags]
            if new_tags:
                json_tags.extend(new_tags)
                data['tags'] = json_tags
                #print("JSON文件中的tags内容已更新：",json_tags)

                # 将更新后的JSON数据写回到文件中
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                # 在列表中移除已处理的图片
                images_list.remove(img_name)  
            else:
                print(f"跳过处理图片: {img_name}，没有新的标签需要添加。")
        else:
            print(f"在路径 {img_path} 下未找到 metadata.json 文件")
    else:
        print(f"未找到与 {img_name} 对应的文件夹路径")


# 检查列表是否为空并打印相应消息
if not images_list:
    print("没有跳过处理的图片")
else:
    print("跳过处理的图片列表:",images_list)

delete_imgdata = input("是否删除imgdata.json？建议删除这个文件，在Eagle中新增文件后再次运行会重新生成带有新文件信息的json。除非你还没有完成目前文件的标签导入 (y/n): ")
if delete_imgdata.lower() == 'y':
    os.remove(imgdatajson_path)
    print("imgdata.json已删除.")
else:
    print("imgdata.json被保留.")

delete_txt_files = input("是否删除txt？_txt文件夹将被保留 (y/n): ")
if delete_txt_files.lower() == 'y':
    for txt_file in txt_list:
        os.remove(os.path.join(txt_dir, f"{txt_file}.txt"))
    print("txt已删除.")
else:
    print("txt未删除.")


input("按回车键结束...")
os._exit(0)
'''