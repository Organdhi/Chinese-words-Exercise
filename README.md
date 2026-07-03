# Chinese-words-Exercise
ターミナル上で動作する，シンプルな中国語の単語学習ツールです．
JSONファイルに登録した単語データからランダムに出題し，合成音声による発音チェックが可能です．指定回数の出題完了後に，ピンイン・中国語（簡体字）・日本語の答え合わせを一覧表示します．
## 動作環境(作成された環境)
* Python 3.11
* Conda
* `gTTS`
* `pygame`
## 環境構築
1. リポジトリをクローンし，ディレクトリを移動する．
   ```bash
   git clone https://github.com/Organdhi/Chinese-words-Exercise.git
   cd Chinese-words-Exercise
   ```
2. Conda環境を新規で作成し，アクティベートする．
   ```bash
   conda create -n Environment-name python=3.11 -y
   conda activate Environment-name
   ```
3. 必要なPythonパッケージのインストールを行う．
    ```bash
    pip install gtts pygame
    ```
## 使い方
1. ディレクトリにある```words.json```を編集し，単語のリストを作成します．
```json
[
  {
    "pinyin": "nǐ hǎo",
    "zh": "你好",
    "ja": "こんにちは"
  },
  {
    "pinyin": "xiè xiè",
    "zh": "谢谢",
    "ja": "ありがとう"
  },
  {
    "pinyin": "zài jiàn",
    "zh": "再见",
    "ja": "さようなら"
  },
  {
    "pinyin": "duì bu qǐ",
    "zh": "对不起",
    "ja": "ごめんなさい"
  }
]
```
2. 実行する
    ``` bash
    python main.py
    ```

## ライセンス
MIT License