import json
import random
import os
import time
from gtts import gTTS
import pygame

def play_audio(text):
    """テキストから音声を生成し、再生する"""
    # gTTSで中国語(簡体字)の音声を生成
    tts = gTTS(text=text, lang='zh-cn')
    filename = "temp_audio.mp3"
    tts.save(filename)
    
    # pygameで音声を再生
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # 再生が終わるまで待機
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.quit()
    
    # 再生が終わった一時ファイルを削除
    if os.path.exists(filename):
        os.remove(filename)

def main():
    # 1. JSONファイルからデータを読み込み、単語の個数を取得
    try:
        with open('words.json', 'r', encoding='utf-8') as f:
            words = json.load(f)
    except FileNotFoundError:
        print("words.jsonが見つかりません。ファイルを作成してください。")
        return

    total_words = len(words)
    print(f"登録されている単語数は {total_words} 個です。")
    
    if total_words == 0:
        print("単語が登録されていません。")
        return

    # 2. ターミナルから出題回数を入力
    while True:
        try:
            num_questions = int(input(f"出題回数を入力してください (1〜{total_words}): "))
            if 1 <= num_questions <= total_words:
                break
            else:
                print(f"エラー: 1から{total_words}の範囲で入力してください。")
        except ValueError:
            print("エラー: 有効な数値を入力してください。")

    # 3. 重複なしのランダムな出題順を決定
    question_indices = random.sample(range(total_words), num_questions)
    
    # 答え合わせ用に、出題した単語をリストに保存（ファイルへのログ出力は廃止）
    asked_words = [] 
    
    print("\n--- 出題開始 ---")
    for i, idx in enumerate(question_indices, 1):
        word = words[idx]
        asked_words.append((i, word))
        
        print(f"問題 {i}: (音声再生中...)")
        
        # 音声を再生
        play_audio(word['zh'])
        
        # 次の問題へ進むための入力待ち
        if i < num_questions:
            input("Enterキーを押すと次の問題が再生されます...")
        else:
            input("Enterキーを押すと答え合わせに進みます...")

    # 4. 答え合わせの出力
    print("\n--- 答え合わせ ---")
    for i, word in asked_words:
        print(f"問題 {i}")
        print(f"ピンイン: {word['pinyin']}")
        print(f"中国語: {word['zh']}")
        print(f"日本語: {word['ja']}")
        print() # 問題ごとに改行

if __name__ == "__main__":
    main()