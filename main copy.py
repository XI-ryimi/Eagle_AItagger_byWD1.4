import os

# 工作目录
work_dir = r'E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library'   
# work_dir = str from tk.
# 对来自图片的地址进行裁剪



# 待标签图片的列表
# 从剪切板获取路径列表
# 使用正则模式检查列表是否是合法路径
# 将错误路径从列表中移除print异常

import re


# 运行测试
from glob import glob
from pathlib import Path
from PIL import Image
from PIL import UnidentifiedImageError

image: Image
batch_input_glob: str
batch_input_recursive: bool
batch_output_dir: str
batch_output_filename_format: str

batch_input_glob = r"E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images"
# batch_input_glob = r"E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLT4C8B.info\1594047078060.jpg E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KKV8N0TLAP6UB.info\tb_image_share_1594047317053.jpg E:\GitHub\Eagle_AItagger_byWD1.4\Eagle_test.library\images\KIMT6M81GAYYH.info\005O0CJZly1gl7bm0ib57j30u01bwe81.png,,"

batch_output_dir =""
batch_input_glob = batch_input_glob.strip()
batch_output_dir = batch_output_dir.strip()
# batch_output_filename_format = batch_output_filename_format.strip()

# batch_input_recursive = False
batch_input_recursive = True

if batch_input_glob != '':
    # if there is no glob pattern, insert it automatically
    if not batch_input_glob.endswith('*'):
        if not batch_input_glob.endswith(os.sep):
            batch_input_glob += os.sep
        batch_input_glob += '*'

    if batch_input_recursive:
        batch_input_glob += '*'

    # get root directory of input glob pattern
    base_dir = batch_input_glob.replace('?', '*')
    base_dir = base_dir.split(os.sep + '*').pop(0)

    # check the input directory path


    # PIL.Image.registered_extensions() returns only PNG if you call too early
    supported_extensions = [
        e
        for e, f in Image.registered_extensions().items()
        if f in Image.OPEN
    ]
    print("调试信息batch_input_glob：", batch_input_glob)
    
    # Handle paths based on the new approach if batch_input_glob ends with \n
    if batch_input_glob.endswith(',,\*'):
        # base_dir = re.search(r'([a-zA-Z]:\\.*?\s)[a-zA-Z]:\\', batch_input_glob)
        # base_dir = base_dir.group(1)

        # print("调试信息base_dir：", base_dir)

        # batch_input_glob = batch_input_glob.replace(',,\*', ',,')
        # batch_input_glob = re.sub(r'\s([a-zA-Z]:\\)', r',,\1', batch_input_glob)
        # paths = [Path(p) for p in re.findall(r'([a-zA-Z]:\\.*?),,', batch_input_glob)]
        pass
    else:
        
        if not os.path.isdir(base_dir):
            print('input path is not a directory / 输入的路径不是文件夹，终止识别')
        
        paths = [
            Path(p)
            for p in glob(batch_input_glob, recursive=batch_input_recursive)
            if '.' + p.split('.').pop().lower() in supported_extensions
            and not p.rsplit('.', 1)[0].endswith('_thumbnail')
        ]

    print(f'found {len(paths)} image(s)')

    for path in paths:
        try:
            image = Image.open(path)
        except UnidentifiedImageError:
            # just in case, user has mysterious file...
            print(f'${path} is not supported image type')
            continue

        # guess the output path
        base_dir_last = ''
        base_dir_last = Path(base_dir).parts[-1]
        print("调试信息base_dir_last：", base_dir_last)
        base_dir_last_idx = path.parts.index(base_dir_last)
        output_dir = Path(batch_output_dir) if batch_output_dir else Path(base_dir)
        output_dir = output_dir.joinpath(*path.parts[base_dir_last_idx + 1:]).parent
        output_dir.mkdir(0o777, True, True)
        
        print("调试信息base_dir_last_idx：", base_dir_last_idx)

        print("调试信息output_dir：", output_dir)
