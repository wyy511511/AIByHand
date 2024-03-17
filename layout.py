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
        if i == 6:
            font_size = 12
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
    "BN_0006_Layer-1.png",
    "BN_0005_Layer-2.png",
    "BN_0004_Layer-3.png",
    "BN_0003_Layer-4.png",
    "BN_0002_Layer-5.png",
    "BN_0001_Layer-6.png",
    "BN_0000_Layer-7.png"
]



texts_zh = [
    "[1] 给定\n一个包含4个训练样本的小批量，每个样本有3个特征。",
    "[2] 线性层\n通过权重和偏置进行乘法操作以获得新的特征。",
    "[3] ReLU\n应用ReLU激活函数，该函数的效果是抑制负值。在此练习中，-2被设为0。",
    "[4] 批量统计\n计算这个小批量中四个样本的总和、均值、方差和标准差。\n注意，这些统计量是针对每一行（即每个特征维度）计算的。",
    "[5] 均值归零\n从每个训练样本的激活值中减去均值（绿色）\n目的是使每个维度中的4个激活值的平均值为零",
    "[6] 方差归一\n除以标准差（橙色）\n目的是使4个激活值的方差等于一。",
    "[7] 缩放与偏移\n将来自[6]的标准化特征乘以线性变换矩阵，并将结果传递给下一层\n目的是将标准化的特征值缩放和偏移至新的均值和方差，这些新的\n均值和方差是网络将要学习的\n对角线上的元素和最后一列是网络将要学习的可训练参数。"
]



# texts_en = [
#     "[1] Given↳ A mini-batch of 4 training examples, each has 3 features.",
#     "[2] Linear Layer↳ Multiply with the weights and biases to obtain new features",
#     "[3] ReLU↳ Apply the ReLU activation function, which has the effect of suppressing negative values. In this exercise, -2 is set to 0.",
#     "[4] Batch Statistics↳ Compute the sum, mean, variance, and standard deviation across the four examples in this min-batch.↳ Note that these statistics are computed for each row (i.e., each feature dimension).",
#     "[5] Shift to Mean = 0↳ Subtract the mean (green) from the activation values for each training example↳ The intended effect is for the 4 activation values in each dimension to average to zero",
#     "[6] Scale to Variance = 1↳ Divide by the standard deviation (orange)↳ The intended effect is for the 4 activation values to have variance equal to one.",
#     "[7] Scale & Shift↳ Multiply the normalized features from [6] by a linear transformation matrix, and pass the results to the next layer↳ The intended effect is to scale and shift the normalized feature values to a new mean and variance, which are to be learned by the network↳ The elements in the diagonal and the last column are trainable parameters the network will learn."
# ]
texts_en = [
    "[1] Given\nA mini-batch of 4 training examples, each has 3 features.",
    "[2] Linear Layer\nMultiply with the weights and biases to obtain new features",
    "[3] ReLU\nApply the ReLU activation function, which has the effect of suppressing negative values. In this exercise, -2 is set to 0.",
    "[4] Batch Statistics\nCompute the sum, mean, variance, and standard deviation across the four examples in this min-batch.\nNote that these statistics are computed for each row (i.e., each feature dimension).",
    "[5] Shift to Mean = 0\nSubtract the mean (green) from the activation values for each training example\nThe intended effect is for the 4 activation values in each dimension to average to zero",
    "[6] Scale to Variance = 1\nDivide by the standard deviation (orange)\nThe intended effect is for the 4 activation values to have variance equal to one.",
    "[7] Scale & Shift\nMultiply the normalized features from [6] by a linear transformation matrix, and pass the results to the next layer\nThe intended effect is to scale and shift the normalized feature values to a new mean and variance, which are to be learned by the network\nThe elements in the diagonal and the last column are trainable parameters the network will learn."
]



create_pdf(images, texts_zh, texts_en)
create_pdf2(images, texts_en)


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
