# create-subseted-font

指定したTruTypeフォントをJSONに記載された文字からなるサブセットフォント(.woff2形式)に変換する。

## 準備

本プロジェクトは、`Python 3.11`を利用しています。
また、[Poetry](https://python-poetry.org/docs/)を利用してパッケージを管理しています。利用する場合は[事前に`poertry`をインストール](#poetryのインストール)してください。

1. 必要なパッケージをインストール

    ~~~shell
    poetry install
    ~~~

2. 動作確認

    ~~~shell
    $ poetry run python ./create-subsetted-font.py -h
    usage: create-subsetted-font.py [-h] -b BASE_JSON [-o OUTPUT_DIR] FONT_FILE [FONT_FILE ...]

    指定したフォントファイルのサブセットを作成する

    positional arguments:
    FONT_FILE             フォントファイル

    options:
    -h, --help            show this help message and exit
    -b BASE_JSON, --base-charset-json BASE_JSON
                            基準となる文字セット
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                            サブセット化したフォントの出力先ディレクトリ(デフォルト値: ./subsetted_fonts)
    ~~~

## 使い方

1. `base.json`を編集し、サブセットに必要な文字を記載する

    `base.json`内の`キー`は無視され、`値`のみがサブセットの対象文字にあんります。
    複数の`値`がある場合は、全ての`値`がサブセットの対象になります。

2. サブセット化したフォントと、`base.json`を指定して、サブセットフォントを作成する

    例として、`sample_fonts`からサブセットフォントを作成します。 [^1]

    ~~~shell
    $ poetry run python ./create-subsetted-font.py -b ./base.json ./sample_fonts/*.ttf
    number of charsets:  3472
    create ./subsetted_fonts/NotoSansJP-Bold.woff2...
    create ./subsetted_fonts/NotoSansJP-Regular.woff2...
    ~~~

3. `./subsetted_fonts`にサブセット化したフォントが`.woff2`形式で作成される

    元のフォントファイルとサイズを比較すると大幅にサイズを削減できている。

    ~~~shell
    $ du -h sample_fonts/*.ttf subsetted_fonts/*.woff2
    5.5M    sample_fonts/NotoSansJP-Bold.ttf
    5.5M    sample_fonts/NotoSansJP-Regular.ttf
    628K    subsetted_fonts/NotoSansJP-Bold.woff2
    616K    subsetted_fonts/NotoSansJP-Regular.woff2
    ~~~

## JSONファイルの更新

`base.json`は、[人名用漢字 - Wikipedia](https://ja.wikipedia.org/wiki/%E4%BA%BA%E5%90%8D%E7%94%A8%E6%BC%A2%E5%AD%97)を参考に手作業で作成しています。
必要に応じて各自修正してください。

また、自サイトで使用している文字セットを確認するためのツール`compare-charsets.py`も用意しています。
本ツールで、`base.json`の文字セットと、自サイトのコンテンツで使用されている文字の差異を確認できます。

使い方は以下になります。

~~~shell
poetry run python compare-charsets.py -h
usage: compare-charsets.py [-h] -b BASE_CHARS_FILE INPUT_FILE [INPUT_FILE ...]

基準文字集合ファイル(JSON)の文字集合と引数のファイルの文字集合の差異をチェックする

positional arguments:
  INPUT_FILE            チェック対象のテキストファイル

options:
  -h, --help            show this help message and exit
  -b BASE_CHARS_FILE, --base-chars-json BASE_CHARS_FILE
                        基準となる文字集合を記載したJSONファイル
~~~

例として、`base.json`と、この`README.md`で使用されている文字集合の差異をチェックする場合は、以下を実行します。

~~~shell
$ poetry run python compare-charsets.py -b base.json README.md
基準文字集合ファイルの文字セット数:  3472
引数で指定したファイルの文字セット数:  213
基準文字集合の文字セットは全ファイルの文字セットを含みますか?:  False
記事文字集合に含まれない文字セットの数:  1

1 :
 - 0xa
~~~

今回は、`LF(0xa)`(改行)のみが差異として検出されました。改行は表示される文字ではないので無視して良いです。
もし、表示される文字が差異として検出された場合は、必要に応じて、`base.json`に含めてください。

## poetryのインストール

[Introduction | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/#installation) に従い、
事前に`poetry`をインストールしてください。

[^1]: [Noto Sans Japanese - Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+JP)の`Regular`と`Bold`フォントをサンプルとして格納
