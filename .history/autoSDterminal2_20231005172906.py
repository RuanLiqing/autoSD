import time
import os
import shutil
import ffmpeg
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from docx import Document
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#全局变量

# 在Python脚本开始处获取用户输入
print("Please provide the following inputs (press Enter to use the default value):")

# 设置并获取webui_addr的值，如果用户没有提供输入，则使用默认值
default_webui_addr = 'http://127.0.0.1:7860'
webui_addr = input(f"Enter the webui_addr (default: {default_webui_addr}): ")
if not webui_addr:
    webui_addr = default_webui_addr

# 设置并获取new_folder_name的值，如果用户没有提供输入，则使用默认值
default_new_folder_name = "awesome推文"
new_folder_name = input(f"Enter the new_folder_name (default: {default_new_folder_name}): ")
if not new_folder_name:
    new_folder_name = default_new_folder_name

# 设置并获取docx_file_path的值，如果用户没有提供输入，则使用默认值
default_docx_file_path = "/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/最后的真相e.docx"
docx_file_path = input(f"Enter the docx_file_path (default: {default_docx_file_path}): ")
if not docx_file_path:
    docx_file_path = default_docx_file_path

checkpoint = "animeChangefulXL_v10ReleasedCandidate.safetensors [8eb8642ab5]"

neg_prompt = "words, bad hands, more fingers, less fingers"

refiner_checkpoint = "sd_xl_refiner_1.0.safetensors [7440042bbd]"
txt2img_switch_at = "0.7"

upscale = "None"
upscale_by = "1"

sampling_steps = "30"
txt2img_width = "1024"
txt2img_height = "1024"

base_dir = "/Users/ruanliqing/autoSD"

# 定义新文件夹的路径
new_folder_path = os.path.join(base_dir, new_folder_name)
images_folder_path = os.path.join(new_folder_path, "images")

#制作视频所需要的声明
temp_folder = os.path.join(new_folder_path, "temp_images")
output_folder = os.path.join(new_folder_path, "img_output")
output_video = os.path.join(new_folder_path, new_folder_name + ".mp4")

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

# 启动Safari浏览器
driver = webdriver.Safari()

# 导航到webUI
driver.get(webui_addr)

width = driver.execute_script("return screen.width;")
height = driver.execute_script("return screen.height;")

driver.set_window_size(width/1.25, height)
#checkpoint
driver.find_element(By.CSS_SELECTOR, "#setting_sd_model_checkpoint input.border-none").clear()
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
driver.find_element(By.CSS_SELECTOR, '#txt2img_enable .icon').click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '#txt2img_checkpoint input.border-none').clear()
driver.find_element(By.CSS_SELECTOR, '#txt2img_checkpoint input.border-none').send_keys(refiner_checkpoint, Keys.ENTER)
driver.find_element(By.CSS_SELECTOR, '#txt2img_switch_at input[data-testid="number-input"]').clear()
driver.find_element(By.CSS_SELECTOR, '#txt2img_switch_at input[data-testid="number-input"]').send_keys(txt2img_switch_at)

# sampling steps
driver.find_element(By.CSS_SELECTOR, '#txt2img_steps input[data-testid="number-input"]').clear()
driver.find_element(By.CSS_SELECTOR, '#txt2img_steps input[data-testid="number-input"]').send_keys(sampling_steps)
    
#text2img_width
driver.find_element(By.CSS_SELECTOR, "#txt2img_width input[data-testid='number-input']").clear()
driver.find_element(By.CSS_SELECTOR, "#txt2img_width input[data-testid='number-input']").send_keys(txt2img_width)

#text2img_height
driver.find_element(By.CSS_SELECTOR, "#txt2img_height input[data-testid='number-input']").clear()
driver.find_element(By.CSS_SELECTOR, "#txt2img_height input[data-testid='number-input']").send_keys(txt2img_height)

 

sentences = extract_sentences_from_docx(docx_file_path)

print(sentences)

info_div_selector = '#html_info_txt2img'
previous_info = driver.find_element(by="css selector", value=info_div_selector).text
previous_src = ""

for sentence in sentences:

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
            # 如果在10秒内按钮没有出现，模拟键盘输入command+enter
            actions = ActionChains(driver)
            actions.key_down(Keys.COMMAND).send_keys(Keys.ENTER).key_up(Keys.COMMAND).perform()


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

    # 从previous_src中提取图片文件名
    img_file_name = os.path.basename(old_img_path)
    new_img_path = os.path.join(images_folder_path, img_file_name)

    # 移动图片
    shutil.move(old_img_path, new_img_path)
    
    previous_info = driver.find_element(by="css selector", value=info_div_selector).text

    print("----" + previous_info)

    time.sleep(1)

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
