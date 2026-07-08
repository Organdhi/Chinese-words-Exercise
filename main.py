import os
import sys
import json
import random
import time
import shutil
import glob
from gtts import gTTS
import pygame

def get_json_file():#JSONファイルの選択を行う
    """カレントディレクトリのJSONファイルを一覧表示し、ユーザーに選択させる"""
    json_files = glob.glob("*.json")
    if not json_files:
        print("カレントディレクトリにJSONファイルが見つかりません。")
        sys.exit(1)

    print("=== 利用可能な単語リスト ===")
    for f in json_files:
        print(f" - {f}")
    print("============================")

    while True:
        filename = input("単語リストのjsonファイル名を入力してください> ").strip()
        
        # ユーザーが「.json」を省いて入力した場合の対応
        if not filename.endswith('.json'):
            filename += '.json'
        
        if os.path.exists(filename):
            return filename
        else:
            print(f"エラー: {filename} が見つかりません。")

def check_and_download_audio(filename, words):
    """変更があれば音声をダウンロードし、なければローカルのものを利用する"""
    base_name = os.path.splitext(filename)[0] # 例: words.json -> words
    audio_dir = base_name
    log_dir = "log"
    log_file = os.path.join(log_dir, filename)

    # 必要なディレクトリを作成
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    needs_download = False

    # 1. ログディレクトリにファイルが存在しない場合はダウンロード
    if not os.path.exists(log_file):
        needs_download = True
    else:
        # 2. 存在する場合はJSONの中身を比較
        try:
            with open(filename, 'r', encoding='utf-8') as f1, \
                 open(log_file, 'r', encoding='utf-8') as f2:
                data_current = json.load(f1)
                data_log = json.load(f2)
                
                # JSONとしてパースして辞書/リスト同士で比較
                # (インデントなどのフォーマット変更だけでは再ダウンロードしない設計)
                if data_current != data_log:
                    needs_download = True
        except json.JSONDecodeError:
            # ログが壊れているなどの場合は安全のため再ダウンロード
            needs_download = True

    # 3. ダウンロード処理
    if needs_download:

        # 古いファイルが残るのを防ぐため、ディレクトリを一度削除して再作成する
        if os.path.exists(audio_dir):
            shutil.rmtree(audio_dir)
        os.makedirs(audio_dir, exist_ok=True)
        
        print(f"\n[{base_name}] の音声ファイルを準備（ダウンロード）しています...")
        # 1.mp3, 2.mp3... のように連番にするため start=1 で enumerate
        for i, word in enumerate(words, 1):
            mp3_path = os.path.join(audio_dir, f"{i}.mp3")
            print(f"ダウンロード中: {i}/{len(words)} ({word['zh']})")
            
            try:
                tts = gTTS(text=word['zh'], lang='zh-cn')
                tts.save(mp3_path)
            except Exception as e:
                print(f"音声の取得に失敗しました ({word['zh']}): {e}")
                
            # APIへの連続アクセス制限を避けるため少し待機
            time.sleep(5) 

        # 4. 実行に成功したら、現在のJSONをlogディレクトリにコピーして記録
        shutil.copy(filename, log_file)
        print("音声ファイルの準備が完了しました。\n")
    else:
        print(f"\n[変更なし] 既存の [{base_name}] ディレクトリの音声ファイルを使用します。\n")

    return audio_dir

def play_local_audio(filepath):#引数のファイル名の音声を再生する
    """ローカルの音声ファイルを再生する"""
    if not os.path.exists(filepath):
        print(f"(エラー: 音声ファイル {filepath} が見つかりません)")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.quit()

def main():
    # 1. 実行開始時にJSONファイルを選択
    filename = get_json_file()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            words = json.load(f)
    except json.JSONDecodeError:
        print("エラー: JSONファイルの形式が正しくありません。")
        return

    total_words = len(words)
    if total_words == 0:
        print("単語が登録されていません。")
        return

    # 2. 音声ファイルの準備（更新チェックとダウンロード）
    audio_dir = check_and_download_audio(filename, words)

    # 3. ターミナルから出題回数を入力
    while True:
        try:
            num_questions = int(input(f"出題回数を入力してください (1〜{total_words}): "))
            if 1 <= num_questions <= total_words:
                break
            else:
                print(f"エラー: 1から{total_words}の範囲で入力してください。")
        except ValueError:
            print("エラー: 有効な数値を入力してください。")

    # 4. 重複なしのランダムな出題順を決定
    # idx はJSONデータ上のインデックス(0から始まる)
    question_indices = random.sample(range(total_words), num_questions)
    
    asked_words = [] 
    
    print("\n--- 出題開始 ---")
    for i, idx in enumerate(question_indices, 1):
        word = words[idx]
        asked_words.append((i, word))
        
        print(f"問題 {i}: (音声再生中...)")
        
        # 保存されているファイル名は 1.mp3, 2.mp3... なので (idx + 1) を使用
        mp3_filepath = os.path.join(audio_dir, f"{idx + 1}.mp3")
        play_local_audio(mp3_filepath)
        
        if i < num_questions:
            input("Enterキーを押すと次の問題が再生されます...")
        else:
            input("Enterキーを押すと答え合わせに進みます...")

    # 5. 答え合わせの出力
    print("\n--- 答え合わせ ---")
    for i, word in asked_words:
        print(f"問題 {i}")
        print(f"ピンイン: {word['pinyin']}")
        print(f"中国語: {word['zh']}")
        print(f"日本語: {word['ja']}")
        print("-" * 25)

if __name__ == "__main__":
    main()