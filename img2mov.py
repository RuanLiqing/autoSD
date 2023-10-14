import ffmpeg
import os
import shutil

def img2mov(input_folder):
    temp_folder = input_folder + "_temp"
    output_folder = input_folder + "_output"

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_images = [img for img in os.listdir(input_folder) if img.endswith('.png')]
    all_images.sort()

    video_paths = []

    for index, image in enumerate(all_images):
        # 为每张图片创建一个4秒的静态视频
        static_video_path = os.path.join(temp_folder, f"static_{index}.mp4")
        (
            ffmpeg
            .input(os.path.join(input_folder, image), loop=1, t=4, framerate=25)
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
    final_video_path = os.path.join(input_folder, "final_output.mp4")
    (
        ffmpeg
        .input(list_file, format='concat', safe=0)
        .output(final_video_path, c='copy')
        .run(overwrite_output=True)
    )

    # 删除临时文件夹
    shutil.rmtree(temp_folder)
    shutil.rmtree(output_folder)