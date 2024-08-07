import re

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