import random

# 作成したモジュールから必要な関数をインポート
from file_manager import get_json_file, load_and_prepare_env
from audio_manager import play_word_audio

def main():
    # 1. ファイルの選択と環境準備
    filename = get_json_file()
    audio_dir, words = load_and_prepare_env(filename)

    total_words = len(words)
    if total_words == 0:
        print("単語が登録されていません。")
        return

    # 2. 出題回数の入力
    while True:
        try:
            num_questions = int(input(f"出題回数を入力してください (1〜{total_words}): "))
            if 1 <= num_questions <= total_words:
                break
            else:
                print(f"エラー: 1から{total_words}の範囲で入力してください。")
        except ValueError:
            print("エラー: 有効な数値を入力してください。")

    # 3. 出題ループ
    question_indices = random.sample(range(total_words), num_questions)
    asked_words = [] 
    
    print("\n--- 出題開始 ---")
    for i, idx in enumerate(question_indices, 1):
        word = words[idx]
        asked_words.append((i, word))
        
        print(f"問題 {i}:")
        
        # モジュールを呼び出して音声を再生（必要に応じてダウンロードされる）
        play_word_audio(audio_dir, idx + 1, word['zh'])
        
        if i < num_questions:
            input("Enterキーを押すと次の問題へ進みます...")
        else:
            input("Enterキーを押すと答え合わせに進みます...")

    # 4. 答え合わせの出力
    print("\n--- 答え合わせ ---")
    for i, word in asked_words:
        print(f"問題 {i}")
        print(f"ピンイン: {word['pinyin']}")
        print(f"中国語: \033[1m\033[93m【 {word['zh']} 】\033[0m")
        print(f"日本語: {word['ja']}")
        print("-" * 25)

if __name__ == "__main__":
    main()