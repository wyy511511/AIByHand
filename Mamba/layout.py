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
    "mamba_0015_Layer-1.png",
    "mamba_0014_Layer-2.png",
    "mamba_0013_Layer-3.png",
    "mamba_0012_Layer-4.png",
    "mamba_0011_Layer-5.png",
    "mamba_0010_Layer-6.png",
    "mamba_0009_Layer-7.png",
    "mamba_0008_Layer-8.png",
    "mamba_0007_Layer-9.png",
    "mamba_0006_Layer-10.png",
    "mamba_0005_Layer-11.png",
    "mamba_0004_Layer-12.png",
    "mamba_0003_Layer-13.png",
    "mamba_0002_Layer-14.png",
    "mamba_0001_Layer-15.png",
    "mamba_0000_Layer-16.png"
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
    "[1] 左侧：\n输入序列中的所有四个token\n都通过一个线性层处理，以计算一组权重。",
    "[2] 右侧：\n这些权重用于驱动一个类RNN网络。",
    "",
    "",
    "[3] 第一个输入[3]和隐藏状态[0, 0]\n使用权重B=[-1; 2]和A=[1, 0; 0, -1]线性组合，\n以计算新的隐藏状态 -> [-3, 6]。\n注意，没有涉及非线性激活函数。",
        "[3] 第一个输入[3]和隐藏状态[0, 0]\n使用权重B=[-1; 2]和A=[1, 0; 0, -1]线性组合，\n以计算新的隐藏状态 -> [-3, 6]。\n注意，没有涉及非线性激活函数。",


    "[4] 隐藏状态[-3, 6]使用权重C = [-2, -3]线性组合，以获得第一个输出[-12]。",
    "[5] 使用不同的权重集A，B，C重复步骤3和4。",
        "[5] 使用不同的权重集A，B，C重复步骤3和4。",

    "[5] 使用不同的权重集A，B，C重复步骤3和4。",

    "[5] 使用不同的权重集A，B，C重复步骤3和4。",
        "[5] 使用不同的权重集A，B，C重复步骤3和4。",

    "[5] 使用不同的权重集A，B，C重复步骤3和4。",

    "[5] 使用不同的权重集A，B，C重复步骤3和4。",

    "[5] 使用不同的权重集A，B，C重复步骤3和4。",
    "[5] 使用不同的权重集A，B，C重复步骤3和4。"
]

texts_en = [
    "[1] Left:\n All four tokens in the input sequence \nare processed by a linear layer to calculate a set of weights.",
    "[2] Right: These weights are used to drive an RNN-like network.",
    "",
    "",
    "[3] The first input [3] and hidden states [0, 0] \nare linearly combined using weights B=[-1; 2] and \n A=[1, 0; 0, -1] to calculate new hidden states -> [-3, 6].\n Note that NO non-linear activation function is involved.",
        "[3] The first input [3] and hidden states [0, 0] \nare linearly combined using weights B=[-1; 2] and \n A=[1, 0; 0, -1] to calculate new hidden states -> [-3, 6].\n Note that NO non-linear activation function is involved.",

    "[4] Hidden states [-3, 6] are linearly combined using weights C = [-2, -3] to obtain the first output [-12]",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
        "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C.",
    "[5] Repeats steps 3 and 4 using different sets of weights A, B, C."


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
