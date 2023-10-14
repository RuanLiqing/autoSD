import time
import os
import shutil
import ffmpeg
import argparse
import questionary
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from docx import Document
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime


#全局变量

parser = argparse.ArgumentParser(description='Automate SD tasks.')
parser.add_argument('--webui_addr', default=None, help='webui address')
parser.add_argument('--new_folder_name', default=None, help='name of the new folder')
parser.add_argument('--docx_file_path', default=None, help='path to docx file')
parser.add_argument('--start_index', type=int, default=0, help='start index for processing sentences')
parser.add_argument('--generate_video', default=None, help='Whether to generate video or not (yes/no)')
parser.add_argument('--checkpoint', default=None, help='Select a checkpoint from given options.')

args = parser.parse_args()

if args.webui_addr is None:
    print("Please provide the following inputs (press Enter to use the default value):")
    default_webui_addr = 'http://127.0.0.1:7860'
    webui_addr = input(f"Enter the webui_addr (default: {default_webui_addr}): ") or default_webui_addr
else:
    webui_addr = args.webui_addr

if args.new_folder_name is None:
    default_new_folder_name = "awesome推文"
    new_folder_name = input(f"Enter the new_folder_name (default: {default_new_folder_name}): ") or default_new_folder_name
else:
    new_folder_name = args.new_folder_name

if args.docx_file_path is None:
    default_docx_file_path = "/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/InCollege.docx"
    docx_file_path = input(f"Enter the docx_file_path (default: {default_docx_file_path}): ") or default_docx_file_path
else:
    docx_file_path = args.docx_file_path

if args.start_index is not None:
    start_index = args.start_index
else:
    start_index = 0

if args.generate_video is None:
    generate_video_input = input("Do you want to generate a video? (y/n, default: n): ").lower()
    generate_video = generate_video_input in ['y', 'yes']
else:
    generate_video = args.generate_video.lower() in ['y', 'yes']

def select_checkpoint():
    options = [
        "animeChangefulXL_v10ReleasedCandidate.safetensors",
        "4Guofeng4XL_v1125D.safetensors",
        "lzSDXL_v10.safetensors",
        "pixelwave_03.safetensors",
        "counterfeitxl_v10.safetensors",
        "juggernautXL_version5.safetensors",
        "sd_xl_base_1.0.safetensors",
        "brightprotonukeNo_v11.safetensors",
        "protovisionXLHighFidelity3D_release0620Bakedvae.safetensors",
        "nightvisionXLPhotorealisticPortrait_v0743ReleaseBakedvae.safetensors",
        "dynavisionXLAllInOneStylized_release0534bakedvae.safetensors"
    ]

    selected = questionary.select(
        "Please select a checkpoint:",
        choices=options
    ).ask()

    return selected

if args.checkpoint is None:
    checkpoint = select_checkpoint()
else:
    checkpoint = args.checkpoint
print(f"Selected checkpoint: {checkpoint}")


autosd_addr = '"/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/appDeveloping/autoSD/autoSDterminal2.py"'

neg_prompt = "words, bad hands, more fingers, less fingers, nude"

checkpoints_without_refiner = ["brightprotonukeNo_v11.safetensors",
    "protovisionXLHighFidelity3D_release0620Bakedvae.safetensors",
    "nightvisionXLPhotorealisticPortrait_v0743ReleaseBakedvae.safetensors",
    "dynavisionXLAllInOneStylized_release0534bakedvae.safetensors"
]
refiner_checkpoint = "sd_xl_refiner_1.0.safetensors"
txt2img_switch_at = "0.7"

upscale = "None"
upscale_by = "1"

sampling_steps = "30"
txt2img_width = "1024"
txt2img_height = "1024"

base_dir = "/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/autoSD"

# 定义新文件夹的路径
new_folder_path = os.path.join(base_dir, new_folder_name)
images_folder_path = os.path.join(new_folder_path, "images")

#制作视频所需要的声明
temp_folder = os.path.join(new_folder_path, "temp_images")
output_folder = os.path.join(new_folder_path, "img_output")
output_video = os.path.join(new_folder_path, new_folder_name + ".mp4")

# 启动Safari浏览器
driver = webdriver.Safari()

# 导航到webUI
driver.get(webui_addr)

width = driver.execute_script("return screen.width;")
height = driver.execute_script("return screen.height;")

driver.set_window_size(width/1.5, height)

time.sleep(10)

# 如果新文件夹不存在，则创建它
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
    os.makedirs(images_folder_path)
    os.makedirs(temp_folder)
    os.makedirs(output_folder)

# 读取docx文件的内容并分割成句子
def extract_sentences_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    sentences = '. '.join(full_text).split('. ')
    
    # 去除每个句子末尾的句号
    return [sentence.rstrip('.') for sentence in sentences]

#checkpoint
driver.find_element(By.CSS_SELECTOR, "#setting_sd_model_checkpoint input.border-none").clear()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "#setting_sd_model_checkpoint input.border-none").send_keys(checkpoint, Keys.ENTER)

#负面提示词
driver.find_element(By.CSS_SELECTOR, '#txt2img_neg_prompt textarea[data-testid="textbox"]').send_keys(neg_prompt, Keys.ENTER)

#Hire
driver.find_element(By.CSS_SELECTOR, '#txt2img_hr .icon').click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '#txt2img_hr_upscaler svg.dropdown-arrow').click()
driver.find_element(By.CSS_SELECTOR, '#txt2img_hr_upscaler input.border-none').clear()
driver.find_element(By.CSS_SELECTOR, '#txt2img_hr_upscaler input.border-none').send_keys(upscale, Keys.ENTER)
driver.find_element(By.CSS_SELECTOR, '#txt2img_hr_scale input[data-testid="number-input"]').clear()
driver.find_element(By.CSS_SELECTOR, '#txt2img_hr_scale input[data-testid="number-input"]').send_keys(upscale_by)

#Refiner
if checkpoint not in checkpoints_without_refiner:
    driver.find_element(By.CSS_SELECTOR, '#txt2img_enable .icon').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#txt2img_checkpoint input.border-none').clear()
    driver.find_element(By.CSS_SELECTOR, '#txt2img_checkpoint input.border-none').send_keys(refiner_checkpoint, Keys.ENTER)
    driver.find_element(By.CSS_SELECTOR, '#txt2img_switch_at input[data-testid="number-input"]').clear()
    driver.find_element(By.CSS_SELECTOR, '#txt2img_switch_at input[data-testid="number-input"]').send_keys(txt2img_switch_at)

# sampling steps
driver.find_element(By.CSS_SELECTOR, '#txt2img_steps input[data-testid="number-input"]').clear()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '#txt2img_steps input[data-testid="number-input"]').send_keys(sampling_steps)
    
#text2img_width
driver.find_element(By.CSS_SELECTOR, "#txt2img_width input[data-testid='number-input']").clear()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "#txt2img_width input[data-testid='number-input']").send_keys(txt2img_width)

#text2img_height
driver.find_element(By.CSS_SELECTOR, "#txt2img_height input[data-testid='number-input']").clear()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "#txt2img_height input[data-testid='number-input']").send_keys(txt2img_height)

 

sentences = extract_sentences_from_docx(docx_file_path)

print(sentences)

#开始画图
info_div_selector = '#html_info_txt2img'
previous_info = driver.find_element(by="css selector", value=info_div_selector).text
previous_src = ""

try:
    for current_index, sentence in enumerate(sentences[start_index:], start=start_index):
    
        MAX_RETRIES = 5
        retries = 0

        while retries < MAX_RETRIES:
            #正面提示词
            input_element = driver.find_element(by="css selector", value='#txt2img_prompt textarea[data-testid="textbox"]')
            input_element.clear()
            time.sleep(1)
            input_element.send_keys(sentence)

            generate_button = driver.find_element(by="css selector", value='#txt2img_generate')
            actions = ActionChains(driver)
            actions.move_to_element(generate_button).click().perform()

            #如果没有正常generate
            try:
                # 等待"Interrupt"或"Skip"按钮出现
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txt2img_interrupt')))
                break  # 如果按钮出现，退出循环
            except TimeoutException:
                actions.move_to_element(generate_button).click().perform()

        img_selector = 'img[data-testid="detailed-image"]'
        
        def image_src_changed(driver):
            img_element = driver.find_element(By.CSS_SELECTOR, img_selector)
            current_src = img_element.get_attribute("src")
            return (webui_addr + "/file=") in current_src and current_src != previous_src

        wait = WebDriverWait(driver, 300)  # 等待最多300秒
        wait.until(image_src_changed)

        # 更新 previous_src 为当前图片的 src
        previous_src = driver.find_element(By.CSS_SELECTOR, img_selector).get_attribute("src")

        # 从previous_src中提取完整的图片路径
        old_img_path = previous_src.split("file=")[-1]

        # 使用current_index命名图片文件名
        new_img_file_name = f"{current_index:05}.png"
        new_img_path = os.path.join(images_folder_path, new_img_file_name)

        # 移动图片
        shutil.move(old_img_path, new_img_path)
        
        previous_info = driver.find_element(by="css selector", value=info_div_selector).text

        print(f"---- Image {current_index:05}: {previous_info}")

        print('用时：' + driver.find_element(By.CSS_SELECTOR, '#html_log_txt2img .performance .time .measurement').text)

        time.sleep(1)
except (Exception, KeyboardInterrupt) as e:
    # 获取当前时间并格式化
    current_time = datetime.now().strftime("断点%Y%m%d%H%M%S")
    exception_script_path = os.path.join(new_folder_path, current_time + ".py")
    with open(exception_script_path, "w") as f:
        f.write(f"import os\n")
        f.write(f"os.system('python {autosd_addr} --webui_addr \"{webui_addr}\" --new_folder_name \"{new_folder_name}\" --docx_file_path \"{docx_file_path}\" --start_index {current_index} --generate_video {'yes' if generate_video else 'no'}')\n") # 替换/path_to_your_script/为autoSD.py脚本的真实路径
        print(f'\033[34m你可以运行以下命令来从断点继续程序：python \"{exception_script_path}\"\033[0m')
    sys.exit()  # 立即终止程序

if generate_video:
    # 获取所有的png文件并排序
    all_images = [img for img in os.listdir(images_folder_path) if img.endswith('.png')]
    all_images.sort()

    video_paths = []
    for index, image in enumerate(all_images):
        # 为每张图片创建一个4秒的静态视频
        static_video_path = os.path.join(temp_folder, f"static_{index}.mp4")
        (
            ffmpeg
            .input(os.path.join(images_folder_path, image), loop=1, t=4, framerate=25)
            .output(static_video_path, pix_fmt='yuv420p', r=25)
            .run(overwrite_output=True)
        )

        # 对静态视频应用淡入和淡出效果
        fade_video_path = os.path.join(output_folder, f"{index}.mp4")
        (
            ffmpeg
            .input(static_video_path)
            .filter_('fade', type='in', start_time=0, duration=0.5)
            .filter_('fade', type='out', start_time=3.5, duration=0.5)
            .output(fade_video_path, pix_fmt='yuv420p', r=25)
            .run(overwrite_output=True)
        )

        video_paths.append(fade_video_path)

    # 创建一个文件列表
    list_file = os.path.join(temp_folder, "list.txt")
    with open(list_file, 'w') as f:
        for video_path in video_paths:
            f.write(f"file '{video_path}'\n")

    # 使用 concat filter 连接视频
    final_video_path = os.path.join(new_folder_path, f"{new_folder_name}.mp4")
    (
        ffmpeg
        .input(list_file, format='concat', safe=0)
        .output(final_video_path, c='copy')
        .run(overwrite_output=True)
    )

# 删除临时文件夹
shutil.rmtree(temp_folder)
shutil.rmtree(output_folder)

# 可选：关闭浏览器
driver.quit()
