from img2mov import img2mov
from imgSortByName import reorder_files_by_filename
import ffmpeg
import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog
import questionary

def get_folder_path():
    method = questionary.select(
        "请选择获取路径的方式：",
        choices=[
            "输入文件夹路径",
            "选择文件夹"
        ]
    ).ask()

    if method == "输入文件夹路径":
        folder_path = input("请输入文件夹路径：")
    elif method == "选择文件夹":
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        folder_path = filedialog.askdirectory()  # 弹出文件夹选择框并获取选择的文件夹路径
    else:
        print("无效的选择。")
        return None

    return folder_path

def main():
    print("请选择文件夹...")
    source_folder = get_folder_path()

    # 检查用户是否选择了文件夹
    if not source_folder:
        print("未选择文件夹，程序终止.")
        return
    
    print(f"选择的文件夹路径是: {source_folder}")
    
    img2mov(reorder_files_by_filename(source_folder))

if __name__ == "__main__":
    main()

