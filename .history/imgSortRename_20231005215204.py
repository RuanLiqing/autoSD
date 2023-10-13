import os
import shutil

def rename_files_in_order(folder_path):
    # 获取文件夹中的所有文件
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    # 按照修改时间对文件进行排序
    files.sort(key=lambda x: os.path.getmtime(x))

    # 重命名文件
    for idx, file in enumerate(files):
        ext = os.path.splitext(file)[1]  # 获取文件的扩展名，例如.jpg
        new_name = os.path.join(folder_path, f"{idx:05}{ext}")  # 格式化新名称为00000, 00001, ...
        shutil.move(file, new_name)

# 使用方法

rename_files_in_order(folder_path)
