import os
import sys
import glob
import json
import shutil

def get_json_file():
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
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        if os.path.exists(filename):
            return filename
        else:
            print(f"エラー: {filename} が見つかりません。")

def load_and_prepare_env(filename):
    """JSONを読み込み、更新があれば音声ディレクトリをリセットして準備する"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            words = json.load(f)
    except json.JSONDecodeError:
        print("エラー: JSONファイルの形式が正しくありません。")
        sys.exit(1)

    base_name = os.path.splitext(filename)[0]
    audio_dir = os.path.join("audio",base_name)
    log_dir = "log"
    log_file = os.path.join(log_dir, filename)

    os.makedirs(log_dir, exist_ok=True)
    needs_clear = False

    # ログがない、または中身が違う場合はクリーンアップフラグを立てる
    if not os.path.exists(log_file):
        needs_clear = True
    else:
        try:
            with open(log_file, 'r', encoding='utf-8') as f_log:
                data_log = json.load(f_log)
                if words != data_log:
                    needs_clear = True
        except json.JSONDecodeError:
            needs_clear = True

    if needs_clear:
        print(f"\n[更新検知] {filename} の新規作成または更新を検知しました。音声データを初期化します。")
        if os.path.exists(audio_dir):
            shutil.rmtree(audio_dir) # 既存の音声をすべて削除
        os.makedirs(audio_dir, exist_ok=True)
        shutil.copy(filename, log_file) # 現在のJSONをログに記録
    else:
        # ディレクトリが手動で消されていた場合のための念の為の作成
        os.makedirs(audio_dir, exist_ok=True) 

    return audio_dir, words