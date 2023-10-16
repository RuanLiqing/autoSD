import os
from moviepy.editor import VideoFileClip

def split_time(total_seconds):
    total_seconds = int(total_seconds)

    base_segment = 540
    
    # 计算基础段数和剩余秒数
    num_segments, remainder = divmod(total_seconds, base_segment)
    
    # 生成基础的段
    segments = [(i * base_segment, (i + 1) * base_segment) for i in range(num_segments)]
    
    index = 0
    while remainder > 0:
        for i in range(len(segments[index:])):
            start, end = segments[index:][i]

            if i == 0:
                segments[index + i] = (start, end + 1)
            elif i == len(segments[index:])-1 and end == total_seconds:
                segments[index + i] = (start + 1, end)
            else:
                segments[index + i] = (start + 1, end + 1)

        remainder -= 1
        index = (index + 1) % len(segments)
        if remainder == 0:  # 退出循环，如果所有剩余的秒数都已经分配
            break  
        
    # 调整其他段的起始时间，减去20秒，最后一段的结束时间为整个视频的结束时间
    for i in range(1, len(segments)):
        start, end = segments[i]
        segments[i] = (start - 20, end)
    if segments:
        start, end = segments[-1]
        segments[-1] = (start, total_seconds)
    
    print(segments)

    return segments


def split_mov(filename):
    # 定义输出文件夹的路径
    output_dir = "/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/分隔好的视频"

    # 加载视频文件
    clip = VideoFileClip(filename)
    
    # 获取视频时长（秒）
    total_seconds = round(clip.duration)
    
    # 获取时长分割
    segments = split_time(total_seconds)
    
    # 获取不带扩展名的文件名
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    
    # 确保输出文件夹存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 根据分割的时长来切割视频并保存
    for i, (start, end) in enumerate(segments):
        subclip = clip.subclip(start, end)
        output_file_path = os.path.join(output_dir, f"{base_filename}_segment_{i + 1}.mov")
        subclip.write_videofile(output_file_path, codec="libx264")
    
    clip.close()

def extract_segment(filename, start_time, end_time, output_file):
    # 加载视频文件
    clip = VideoFileClip(filename)
    
    # 提取指定片段
    subclip = clip.subclip(start_time, end_time)
    
    # 保存片段
    subclip.write_videofile(output_file, codec="libx264")
    
    clip.close()

def main():
    filename = input("请输入你的.mov文件：")

    split_mov(filename)

if __name__ == "__main__":
    # main()
    

    filename = "/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/autoSD/爱情200/10月15日/10月15日.mov"
    start_time = 2857
    end_time = 3451
    output_file = "/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/分隔好的视频/10月15日_segment_6.mov"  # 你可以根据需要更改这个输出文件名

    extract_segment(filename, start_time, end_time, output_file)

