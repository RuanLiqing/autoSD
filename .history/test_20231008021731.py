import deepl

#测试 文档翻译
deepl.docx_zh2en('/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/小说集/最后的真相.docx')




# #测试数组
# chinese_sentences = ["你好", "我爱编程", "这是一个测试"]

# print(deepl.array_zh2en(chinese_sentences))




# #测试 deepl.extract_sentences_from_docx_zh 函数
# file_path = '/Users/ruanliqing/Library/Mobile Documents/com~apple~CloudDocs/startup/推文/小说集/最后的真相.docx'

# sentences = deepl.extract_sentences_from_docx_zh(file_path)

# for sentence in sentences[:10]:
#     print(sentence)
