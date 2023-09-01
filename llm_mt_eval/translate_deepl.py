from deepl import Translator
from utils import read_lines, write_text

def translate_text(text, src_lang, dest_lang):
    translator = Translator("288c37aa-e210-4fc9-57a1-f9f5ba7fdea1:fx")  # Replace with your DeepL API key
    translated = translator.translate_text(text, target_lang=dest_lang, source_lang=src_lang)
    return translated.text

def translate_file(src_lang: str, tgt_lang: str, src_file: str, experiment_name: str):
    
    text_to_translate = '\n'.join(read_lines(src_file))
    
    translated_text = translate_text(text_to_translate, src_lang, tgt_lang)+'\n'
    
    tgt_file = f"{experiment_name}"
    write_text(translated_text, tgt_file)