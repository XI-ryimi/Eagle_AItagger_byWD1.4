# Eagle_AItagger_byWD1.4

**debug中**/**可能的计划：对秋叶lora训练器其他功能的裁剪**

基于[秋叶lora训练器](https://github.com/Akegarasu/lora-scripts)WD1.4前端为Eagle开发的AI标签器

适用于大量图片的初次批量AI标记，或习惯囤积一堆图片后为图片分类的人

如果只是有少量图片抓取到eagle中后立刻分类AI标记，可以看看[jtydhr88/eagle-ai-tagger: A custom plugin for Eagle to generate tags by local AI model (github.com)](https://github.com/jtydhr88/eagle-ai-tagger)这个项目

### 代码使用

下载秋叶的lora训练器

将标签器内mikazuki文件夹复制到秋叶lora训练器文件夹下，全部替换文件

打开lora训练器的WD1.4标签界面

初次使用可直接复制资源库目录路径到WD1.4标签界面，并打开递归搜寻子目录（需本项目的文件替换后，否则会对缩略图进行处理。）

初次或新增少量图片（几千）需要AI标记，从Eagle内选中需要AI标记的图片，ctrl+alt+c或右键复制文件路径到WD1.4标签界面。

对于大型资源库，每次处理的图片数量不建议超过1W

在lora训练器中的WD1.4页面，将复制的路径粘贴到第一项图片文件夹路径的文本框内

在文本框的末尾添加两个英文逗号",,"

取消勾选使用空格代替下划线，选择合适的阈值与模型（推荐阈值0.6，模型swinv2_v3，因为需要精度而不是速度）

运行main.py,按照指示将标签汉化写入Eagle。
