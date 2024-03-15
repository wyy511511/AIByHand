from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import portrait

# 注册字体（以San Francisco为例，确保路径正确）
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'  # 请根据实际情况调整路径
pdfmetrics.registerFont(TTFont('STHeiti', font_path))

# 设置PDF页面大小为800x1067点（假设72 DPI，直接使用像素值）
page_size = (800, 1067)
# page_size = (1000, 500)
c = canvas.Canvas("output.pdf", pagesize=page_size)

# 使用注册的字体和调整大小的页面
c.setFont('STHeiti', 12)
c.drawString(100, 1000, '这是使用macOS默认字体的文本')



def create_pdf(images, texts_zh, texts_en, output='output.pdf'):
    c = canvas.Canvas(output, pagesize=page_size)
    width, height = page_size  # 使用letter页面大小

    current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件夹路径

    for i, (image_name, text_zh, text_en) in enumerate(zip(images, texts_zh, texts_en)):
        # 构建图片的完整路径
        image_path = os.path.join(current_dir, image_name)

        # 加载图片并调整大小以符合3:4比例
        img = Image.open(image_path)
        img_w, img_h = img.size
        target_height = height * 0.9  # 图片占页面上半部
        aspect_ratio = 3/4
        new_width = target_height * aspect_ratio
        # img = img.resize((int(new_width), int(target_height)), Image.ANTIALIAS)
        # img = img.resize((int(new_width), int(target_height)))
        img = img.resize((int(new_width), int(target_height)), Image.Resampling.LANCZOS)


        # 保存临时图片用于reportlab
        temp_path = f"temp_{i}.jpg"
        img.save(temp_path)

        # 放置图片
        c.drawImage(temp_path, (width - new_width) / 2, height - target_height, width=new_width, height=target_height)

        # 绘制文本
        text_width = width / 2  # 将页面宽度分为两部分
        c.setFont('STHeiti', 12)
        # c.drawString(100, 800, '这是中文文本')




        c.drawString(10, height * 0.1, text_zh)  # 中文文本在左侧
        c.setFont('Helvetica', 12)

        c.drawString(text_width + 10, height * 0.1, text_en)  # 英文文本在右侧

        # 添加新页
        c.showPage()

        # 清理临时图片
        os.remove(temp_path)

    c.save()


images = [
    "BN_0000_Layer-7.png",
    "BN_0001_Layer-6.png",
    "BN_0002_Layer-5.png",
    "BN_0003_Layer-4.png",
    "BN_0004_Layer-3.png",
    "BN_0005_Layer-2.png",
    "BN_0006_Layer-1.png"
]

# 生成相应数量的中文文本数组
texts_zh = [
    "[1] 给定↳ 一个包含4个训练样本的小批量，每个样本有3个特征。",
    "[2] 线性层↳ 通过权重和偏置进行乘法操作以获得新的特征。",
    "[3] ReLU↳ 应用ReLU激活函数，该函数的效果是抑制负值。在此练习中，-2被设为0。",
    "[4] 批量统计↳ 计算这个小批量中四个样本的总和、均值、方差和标准差。↳ 注意，这些统计量是针对每一行（即每个特征维度）计算的。",
    "[5] 均值归零↳ 从每个训练样本的激活值中减去均值（绿色）↳ 目的是使每个维度中的4个激活值的平均值为零",
    "[6] 方差归一↳ 除以标准差（橙色）↳ 目的是使4个激活值的方差等于一。",
    "[7] 缩放与偏移↳ 将来自[6]的标准化特征乘以线性变换矩阵，并将结果传递给下一层↳ 目的是将标准化的特征值缩放和偏移至新的均值和方差，这些新的均值和方差是网络将要学习的↳ 对角线上的元素和最后一列是网络将要学习的可训练参数。"
]

# 生成相应数量的英文文本数组
texts_en = [
    "[1] Given↳ A mini-batch of 4 training examples, each has 3 features.",
    "[2] Linear Layer↳ Multiply with the weights and biases to obtain new features",
    "[3] ReLU↳ Apply the ReLU activation function, which has the effect of suppressing negative values. In this exercise, -2 is set to 0.",
    "[4] Batch Statistics↳ Compute the sum, mean, variance, and standard deviation across the four examples in this min-batch.↳ Note that these statistics are computed for each row (i.e., each feature dimension).",
    "[5] Shift to Mean = 0↳ Subtract the mean (green) from the activation values for each training example↳ The intended effect is for the 4 activation values in each dimension to average to zero",
    "[6] Scale to Variance = 1↳ Divide by the standard deviation (orange)↳ The intended effect is for the 4 activation values to have variance equal to one.",
    "[7] Scale & Shift↳ Multiply the normalized features from [6] by a linear transformation matrix, and pass the results to the next layer↳ The intended effect is to scale and shift the normalized feature values to a new mean and variance, which are to be learned by the network↳ The elements in the diagonal and the last column are trainable parameters the network will learn."
]



create_pdf(images, texts_zh, texts_en)



# 图片和文本列表
# images = ['img1.png', 'img2.png', 'img3.png']  # 你的图片文件名列表
# texts_zh = ['中文标题 1', '中文标题 2', '中文标题 3']  # 你的中文文本列表
# texts_en = ['Title 1', 'Title 2', 'Title 3']  # 你的英文文本列表
    
# 生成图片文件名列表
# images = [
#     'RLHF_0000_Layer 15.jpg', 'RLHF_0005_Layer 10.jpg', 'RLHF_0010_Layer 5.jpg',
#     'RLHF_0001_Layer 14.jpg', 'RLHF_0006_Layer 9.jpg', 'RLHF_0011_Layer 4.jpg',
#     'RLHF_0002_Layer 13.jpg', 'RLHF_0007_Layer 8.jpg', 'RLHF_0012_Layer 3.jpg',
#     'RLHF_0003_Layer 12.jpg', 'RLHF_0008_Layer 7.jpg', 'RLHF_0013_Layer 2.jpg',
#     'RLHF_0004_Layer 11.jpg', 'RLHF_0009_Layer 6.jpg', 'RLHF_0014_Layer 1.jpg'
# ]

# # 生成相应数量的文本数组
# texts_zh = [f'文字🦟 {i}' for i in range(1, len(images) + 1)]
# texts_en= [f'Text {i}' for i in range(1, len(images) + 1)]
