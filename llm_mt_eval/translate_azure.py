import requests, uuid
from utils import read_lines, write_text

key = "6c6bb439c4ad4a5391bba50fded0a81c"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "NorthEurope"

def translate_text(text, src_lang, dest_lang):
    path = '/translate'
    constructed_url = endpoint + path
    
    params = {
        'api-version': '3.0',
        'from': src_lang,
        'to': [dest_lang]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    # Assuming the first element contains the translation we need
    try:
        translated_text = response[0]['translations'][0]['text']
        return translated_text
    except Exception as e:
        print(f"An error occurred: {response}")
        return text

def translate_file(src_lang: str, tgt_lang: str, src_file: str, experiment_name: str):
    
    text_to_translate = '\n'.join(read_lines(src_file))
    
    translated_text = translate_text(text_to_translate, src_lang, tgt_lang)+'\n'
    
    tgt_file = f"{experiment_name}"
    write_text(translated_text, tgt_file)