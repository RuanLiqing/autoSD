# autoSD
根据故事文本自动批量生成故事插图

目前仅限Mac M系列芯片，其他系统尚未开发

# 代码逻辑：
- 1、入口是 en2autosdpro.py，需提供英文文本。该代码将会调用核心代码 autoSDterminal2.py 进行自动生成图片
- 2、然后可以挑选图片后用 folder2mov.py 生成视频。视频由各个图片淡入淡出串联而成。
