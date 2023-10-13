import os
import shutil

def rename_files_in_order(source_folder, dest_folder):
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 获取源文件夹中的所有文件
    files = [os.path.join(source_folder, file) for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]

    # 按照修改时间对文件进行排序
    files.sort(key=lambda x: os.path.getmtime(x))

    # 复制并重命名文件到目标文件夹
    for idx, file in enumerate(files):
        ext = os.path.splitext(file)[1]  # 获取文件的扩展名，例如.jpg
        new_name = os.path.join(dest_folder, f"{idx:05}{ext}")  # 格式化新名称为00000, 00001, ...
        shutil.copy(file, new_name)

# 使用方法
source_folder = "/Users/ruanliqing/autoSD/最后的真相/images"  # 替换为您的源图片文件夹路径
dest_folder = source_folder + "Sbtime"  # 替换为您想要存放重命名图片的新文件夹路径
rename_files_in_order(source_folder, dest_folder)
