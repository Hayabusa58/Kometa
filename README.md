# Kometa

## 概要
軽量でシンプルな静的サイトジェネレータです。
"Kometa" とはイタリア語で「彗星」を表します。

## 機能
- Markdown 形式で執筆したページを指定したテンプレートで HTML へ変換
- 変換時、Markdown に埋め込んだ画像の Exif ファイルを自動削除

## 前提環境
- => Python 3.9.21

## インストール
```
$ pip install -r requirements.txt
```

## 開発経緯
作者の個人ページ docs.h4y4bus4.com の運営で使用していたシェルスクリプト群のメンテが大変だったので、Python で書き直しました。