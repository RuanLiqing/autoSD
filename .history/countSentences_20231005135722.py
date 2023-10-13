from docx import Document
import re

def count_sentences(docx_path):
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    text = '\n'.join(full_text)

    # 一个简单的句子拆分规则，考虑到句号、问号和感叹号
    sentences = re.split(r'[.!?]', text)

    # 过滤空句子或只包含空格的句子
    sentences = [s for s in sentences if s.strip() != ""]

    return len(sentences)

docx_path = "/Users/ruanliqing/Desktop/finalTruth.docx"
number_of_sentences = count_sentences(docx_path)
print(f"该文件中有 {number_of_sentences} 个句子。")

