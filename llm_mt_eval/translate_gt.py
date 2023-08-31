from googletrans import Translator, LANGUAGES
from utils import read_lines, write_text

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    try:
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Splitting the text into two parts and retrying...")
        lines = text.strip().split('\n')
        half = len(lines) // 2
        part1 = '\n'.join(lines[:half])
        part2 = '\n'.join(lines[half:])
        
        translated_part1 = translator.translate(part1, src=src_lang, dest=dest_lang).text
        translated_part2 = translator.translate(part2, src=src_lang, dest=dest_lang).text

        return translated_part1 + '\n' + translated_part2

def translate_file(src_lang: str, tgt_lang: str, src_file: str, experiment_name: str):
    text_to_translate = '\n'.join(read_lines(src_file))
    
    translated_text = translate_text(text_to_translate, src_lang, tgt_lang) + '\n'
    
    tgt_file = f"{experiment_name}"
    write_text(translated_text, tgt_file)