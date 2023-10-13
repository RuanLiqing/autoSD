import requests

def array_translator(sentences):
    translated_array = []

    for sentence in sentences:


#测试API
def translate_with_deepl(text, target_language, auth_key):
    url = "https://api-free.deepl.com/v2/translate"
    
    payload = {
        "text": text,
        "target_lang": target_language,
        "auth_key": auth_key
    }
    
    response = requests.post(url, data=payload)
    result = response.json()
    
    translated_text = result['translations'][0]['text']
    
    return translated_text

# 使用
auth_key = "916ea6b7-7638-e520-0440-a4c49a4873af:fx" # 请替换为你的 API 密钥
text_to_translate = "我爱编程"
target_language = "EN"  # 英语

translated_text = translate_with_deepl(text_to_translate, target_language, auth_key)
print(translated_text)
