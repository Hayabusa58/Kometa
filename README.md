# Kometa

## 概要
軽量でシンプルな静的サイトジェネレータです。
"Kometa" とはチェコ語で「彗星」を表します。

## 機能
- Markdown 形式での記事執筆
    - 執筆したページを指定したテンプレートで HTML へ変換
    - 簡易的に公開範囲を限定した記事の公開
- 変換時、Markdown に埋め込んだ画像の Exif ファイルを自動削除

## 前提環境
下記のインストールが必要です。

- Docker 
- Docker compose
- => Python 3.9.21
    - Python が動く環境なら問題ないと思いますが、Linux 環境以外の動作確認はしていません。

## インストール
Python 仮想環境（venv 等）を使用することを推奨します。

```
$ git clone https://github.com/Hayabusa58/Kometa.git your-site-name
$ cd your-site-name
$ pip install -r requirements.txt
```

## 初期設定

### ディレクトリの生成
```
$ python kometa.py init
```
上記コマンドは必要なディレクトリを作成します。
最初の一回だけ実行してください。

また、公開範囲の限定機能を使用する場合、作業ディレクトリ直下に .htpasswd ファイルを生成してください。

### 開発用サーバの設定
```
$ cp compose.yaml.sample compose.yaml
$ cp nginx.conf.sample nginx.conf
```
compose.yaml, nginx.conf の `sample.example.com` を公開するサイトのドメインに書き換えてください。

## 使い方

### 記事の作成
```
$ python kometa.py new article-title
```
上記コマンドは `./article/article-title` に執筆用 Markdown ファイルを生成します。
埋め込みの画像ファイルはすべて同じディレクトリにおいてください。

記事の公開範囲を限定する場合、`visibility: public` を `visibility: limited` に変更してください。
デフォルトでは `visibility: public` の記事は `./out/article/public` 以下へ、 `visibility: limited` の記事は `./out/article/limited` 以下へ出力されます。

### 記事の出力
```
$ python kometa.py build article-title
```
上記コマンドは指定した visibility に応じて適切なディレクトリに HTML ファイルを出力し、埋め込んだ画像ファイルをコピーします。
また画像ファイルの Exif 情報をすべて削除します。

### 動作確認
```
$ python kometa.py dev
```
上記コマンドで開発用 Web サーバが起動します。
localhost:8080 にアクセスするとWebサイトの動作確認ができます。

### 公開
publish コマンドを実装予定です。

## 開発経緯
作者の個人ページ docs.h4y4bus4.com の運営で使用していたシェルスクリプト群のメンテが大変だったので、Python で書き直しました。