import requests

def translate_sentences_with_deepl(sentences, api_key):
    """
    将给定的中文句子数组翻译为英文使用DeepL API。
    
    参数:
        sentences (list): 待翻译的中文句子数组。
        api_key (str): DeepL API 密钥。
        
    返回:
        list: 翻译后的英文句子数组。
    """
    translated_sentences = []

    base_url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    for sentence in sentences:
        payload = {
            "text": sentence,
            "target_lang": "EN",
            "source_lang": "ZH"
        }
        response = requests.post(base_url, headers=headers, data=payload)
        translation = response.json()["translations"][0]["text"]
        translated_sentences.append(translation)

    return translated_sentences

# 使用示例：
api_key = "YOUR_DEEPL_API_KEY"  # 替换为你的DeepL API密钥
chinese_sentences = ["你好", "我爱编程", "这是一个测试"]
english_sentences = translate_sentences_with_deepl(chinese_sentences, api_key)
print(english_sentences)


#