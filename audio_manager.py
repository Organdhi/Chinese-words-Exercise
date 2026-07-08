import os
import time
from gtts import gTTS
import pygame

def play_word_audio(audio_dir, word_id, word_zh):
    """音声ファイルが存在すれば再生、なければダウンロードしてから再生する"""
    filepath = os.path.join(audio_dir, f"{word_id}.mp3")

    # 1. オンデマンドダウンロード処理
    if not os.path.exists(filepath):
        print(f"  -> 音声ファイルをダウンロード中... ({word_zh})")
        try:
            clean_text = word_zh.replace('～', '')
            tts = gTTS(text=clean_text, lang='zh-cn')
            tts.save(filepath)
            # 連続でダウンロードが発生した場合のAPI制限対策
            time.sleep(0.3) 
        except Exception as e:
            print(f"  -> 音声の取得に失敗しました: {e}")
            return

    # 2. 再生処理
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.quit()