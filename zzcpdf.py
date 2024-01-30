import argparse
import fitz
import os
import numpy as np
from PIL import Image
from fpdf import FPDF

def print_flush(s):
    print(s);
    sys.stdout.flush();
    
class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

# 处理图片函数
def process_image(image, start, end,bstart,bend):
    # 转换为灰度图像
    gray_image = image.convert("L")

    # 将灰度图像转换为 NumPy 数组
    img_array = np.array(gray_image)

    # 将非文字部分变为白色，文字变为黑色
    if bstart == 1:
        img_array[img_array < start] = 0
    
    if bend == 1:
        img_array[img_array > end] = 254

    # 创建处理后的图像
    processed_image = Image.fromarray(img_array)

    return processed_image

# 将 PDF 页面保存为图片文件
def save_pages_as_images(input_pdf, output_folder,bstart,bend,start,end):
    print_flush("save_pages_as_images")
    doc = fitz.open(input_pdf)
    total_pages = len(doc)
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    for i, page in enumerate(doc):
        print_flush(f"page_{format(i+1, '05')}.jpg")
        pix = page.get_pixmap()
        # 将 Pixmap 转换为 PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        processed_image = process_image(image, start, end,bstart,bend)  # 传入合适的起始和结束阈值
        # 保存为图片文件
        img_path = os.path.join(output_folder, f"page_{format(i+1, '05')}.jpg")
        processed_image.save(img_path)

    doc.close()

# 将图片添加到 PDF
def add_images_to_pdf(directory, output_path):
    print_flush("add_images_to_pdf")
    # 创建一个PDF对象
    pdf = PDF(format="A4")

    # 获取目录中的图片文件列表
    image_files = [filename for filename in os.listdir(directory) if filename.endswith((".jpg", ".png", ".jpeg"))]
    total_images = len(image_files)

    # 确保输出文件夹存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 遍历图片文件列表并添加到PDF中
    for i, filename in enumerate(image_files):
        # 拼接文件路径
        filepath = os.path.join(directory, filename)

        # 添加一个空白页面
        pdf.add_page()

        # 获取PDF页面尺寸
        pdf_width = pdf.w
        pdf_height = pdf.h

        # 将图片添加到PDF中
        pdf.image(filepath, 0, 0, int(pdf_width), int(pdf_height))

    # 保存新的PDF文件
    pdf.output(output_path)

# 保存 PDF 页面为图片并处理
def save_pdf_pages(input_pdf, bstart, bend, start, end):
    print_flush("save_pdf_pages")
    # 获取输入文件的目录路径
    input_directory = os.path.dirname(input_pdf)

    # 获取输入文件的文件名和扩展名
    filename, extension = os.path.splitext(os.path.basename(input_pdf))

    # 创建一个子目录 "<filename>_pics" 来保存拆分出来的图片文件
    output_folder = os.path.join(input_directory, f"{filename}_pics")
    os.makedirs(output_folder, exist_ok=True)

    # 保存页面为图片并创建新的 PDF 文档
    save_pages_as_images(input_pdf, output_folder, bstart, bend, start, end)

    print_flush("save pages to pics.")

    # 生成输出的 PDF 文件路径
    output_pdf = os.path.join(input_directory, f"{filename}_output.pdf")

    # 添加图片到 PDF
    add_images_to_pdf(output_folder, output_pdf)



if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Process PDF file and add images.")
    parser.add_argument("input_pdf", help="Input PDF file path")
    parser.add_argument("--bstart", type=int, default=1, help="bstart value (0 or 1)")
    parser.add_argument("--bend", type=int, default=1, help="bend value (0 or 1)")
    parser.add_argument("--start", type=int, default=170, help="bstart value (0 or 254)")
    parser.add_argument("--end", type=int, default=200, help="bend value (0 or 254)")    
    args = parser.parse_args()
    
    print_flush(f"args.bstart:{args.bstart},args.bend:{args.bend},args.start:{args.start},args.bend:{args.end}");
    # 保存 PDF 页面为图片并处理
    save_pdf_pages(args.input_pdf, args.bstart, args.bend, args.start, args.end)
    
    print_flush("process over");