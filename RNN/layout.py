from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import portrait


font_path = '/System/Library/Fonts/STHeiti Medium.ttc' 
pdfmetrics.registerFont(TTFont('STHeiti', font_path))


page_size = (800, 1067)#Adjust

c = canvas.Canvas("output.pdf", pagesize=page_size)


from reportlab.lib import utils

def auto_wrap_text(text, font, font_size, max_width):

    from reportlab.pdfbase.pdfmetrics import stringWidth
    wrapped_lines = []  
    paragraphs = text.split('\n') 

    for paragraph in paragraphs:
        lines = [] 
        words = paragraph.split()
        current_line = []
        current_width = 0

        for word in words:
            word_width = stringWidth(word, font, font_size) + stringWidth(" ", font, font_size)  
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:  
            lines.append(" ".join(current_line))

        wrapped_lines.extend(lines)
        wrapped_lines.append("")  
    return wrapped_lines[:-1]  

def create_pdf(images, texts_zh, texts_en, output='bn_ZH&EN.pdf'):
    c = canvas.Canvas(output, pagesize=page_size)
    width, height = page_size

    current_dir = os.path.dirname(os.path.abspath(__file__)) 

    for i, (image_name, text_zh, text_en) in enumerate(zip(images, texts_zh, texts_en)):

        image_path = os.path.join(current_dir, image_name)


        img = Image.open(image_path)
        img_w, img_h = img.size
        target_height = height * 0.8  # Adjust
        aspect_ratio = img_w / img_h
        new_width = target_height * aspect_ratio
        img = img.resize((int(new_width), int(target_height)), Image.Resampling.LANCZOS)


        temp_path = f"bn_zh_{i}.jpg"
        img.save(temp_path)

        c.drawImage(temp_path, (width - new_width) / 2, height - target_height - 10, width=new_width, height=target_height)  #Adjust

        font_size = 15  # Adjust
        # if i == 6:
        #     font_size = 12
        max_width = width / 2 - 60  # Adjust max_width as needed
        
        wrapped_text_zh = auto_wrap_text(text_zh, 'STHeiti', font_size, max_width)
        wrapped_text_en = auto_wrap_text(text_en, 'Helvetica', font_size, max_width)

        text_obj_zh = c.beginText(60, height - target_height - 30) #数字越小越靠上
        text_obj_zh.setFont('STHeiti', font_size)
        for line in wrapped_text_zh:
            text_obj_zh.textLine(line)
        c.drawText(text_obj_zh)

        text_obj_en = c.beginText(width / 2 + 60, height - target_height - 30)
        text_obj_en.setFont('Helvetica', font_size)
        for line in wrapped_text_en:
            text_obj_en.textLine(line)
        c.drawText(text_obj_en)

        c.showPage()

        os.remove(temp_path)

    c.save()
def create_pdf2(images, texts_en, output='batch normalizaton_EN.pdf'):
    c = canvas.Canvas(output, pagesize=page_size)
    width, height = page_size

    current_dir = os.path.dirname(os.path.abspath(__file__))

    for i, (image_name, text_en) in enumerate(zip(images, texts_en)):
        image_path = os.path.join(current_dir, image_name)
        img = Image.open(image_path)
        img_w, img_h = img.size
        target_height = height * 0.8  # Adjusted for image to text ratio
        aspect_ratio = img_w / img_h
        new_width = target_height * aspect_ratio
        img = img.resize((int(new_width), int(target_height)), Image.Resampling.LANCZOS)

        temp_path = f"bn_en_{i}.jpg"
        img.save(temp_path)

        c.drawImage(temp_path, (width - new_width) / 2, height - target_height - 10, width=new_width, height=target_height)

        font_size = 12
        max_width = new_width  
        
        wrapped_text_en = auto_wrap_text(text_en, 'Helvetica', font_size, max_width)


        text_start_position = (width - new_width) / 2
        text_obj_en = c.beginText(text_start_position, height - target_height - 170) 
        text_obj_en.setFont('Helvetica', font_size)
        for line in wrapped_text_en:
            text_obj_en.textLine(line)
        c.drawText(text_obj_en)

        c.showPage()
        os.remove(temp_path)

    c.save()


images = [
    'rnn_0012_Layer 1.jpg',
    'rnn_0011_Layer 2.jpg',
    'rnn_0010_Layer 3.jpg',
    'rnn_0009_Layer 4.jpg',
    'rnn_0008_Layer 5.jpg',
    'rnn_0007_Layer 6.jpg',
    'rnn_0006_Layer 7.jpg',
    'rnn_0005_Layer 8.jpg',
    'rnn_0004_Layer 9.jpg',
    'rnn_0003_Layer 10.jpg',
    'rnn_0002_Layer 11.jpg',
    'rnn_0001_Layer 12.jpg',
    'rnn_0000_Layer 13.jpg'
]




# texts_zh = [
#     "[1] ",
#     "[2] ",
#     "[3] ",
#     "[4] ",
  
# ]



# texts_en = [
#     "[1] ",
#     "[2]",
#     "[3]",
   
# ]


texts_zh = [
    "[1] 隐藏状态初始化为 [0, 0]。",
    "[2] 利用权重矩阵A和B将第一个输入x1和\n隐藏状态[0, 0]线性组合,然后通过ReLU非线性激活函数计算出新的隐藏状态 -> [3, 6]。",
    "[3] 利用权重矩阵𝘊将隐藏状态[3, 6]线性组合得到第一个输出y1 -> [3]。",
    "[3] 利用权重矩阵𝘊将隐藏状态[3, 6]线性组合得到第一个输出y1 -> [3]。",
    "[4] 将输入x2和新的隐藏状态[3, 6]线性组合并通过ReLU激活,得到新的隐藏状态 -> [1, 17]。",
    "[4] 将输入x2和新的隐藏状态[3, 6]线性组合并通过ReLU激活,得到新的隐藏状态 -> [1, 17]。",
    "[5] 利用权重矩阵𝘊将隐藏状态[1, 17]线性组合得到第二个输出y2 -> [16]。",
    "",
    "",
    "",
    "",
    "",
    "",

    


]

texts_en = [
    "[1] Hidden state are initialized to [0, 0].",
    "[2] The first input x1 and hidden states [0, 0] are linearly combined using weights A and B, followed by a non-linear activation function ReLu, to calculate the new hidden states -> [3, 6].",
    "[3] The hidden states [3, 6] are linearly combined using weights C to obtain the first output y1 -> [3].",
    "[3] The hidden states [3, 6] are linearly combined using weights C to obtain the first output y1 -> [3].",
    "[4] Input x2 and the new hidden states [3, 6] are linearly combined and passed through the ReLu activation to get the new hidden states -> [1, 17].",
    "",
    "[5] The hidden states [1, 17] are linearly combined using weights C to obtain the second output y2 -> [16].",
        "",
    "",
    "",
    "",
    "",
    "",


]


create_pdf(images, texts_zh, texts_en)
# create_pdf2(images, texts_en)


# 图片和文本列表
# images = ['img1.png', 'img2.png', 'img3.png'] 
# texts_zh = ['中文标题 1', '中文标题 2', '中文标题 3']  
# texts_en = ['Title 1', 'Title 2', 'Title 3']  
    
# 生成图片文件名列表
# images = [
#     'RLHF_0000_Layer 15.jpg', 'RLHF_0005_Layer 10.jpg', 'RLHF_0010_Layer 5.jpg',
#     'RLHF_0001_Layer 14.jpg', 'RLHF_0006_Layer 9.jpg', 'RLHF_0011_Layer 4.jpg',
#     'RLHF_0002_Layer 13.jpg', 'RLHF_0007_Layer 8.jpg', 'RLHF_0012_Layer 3.jpg',
#     'RLHF_0003_Layer 12.jpg', 'RLHF_0008_Layer 7.jpg', 'RLHF_0013_Layer 2.jpg',
#     'RLHF_0004_Layer 11.jpg', 'RLHF_0009_Layer 6.jpg', 'RLHF_0014_Layer 1.jpg'
# ]

# # 生成相应数量的文本数组, 测试emoji
# texts_zh = [f'文字🦟 {i}' for i in range(1, len(images) + 1)]
# texts_en= [f'Text {i}' for i in range(1, len(images) + 1)]
