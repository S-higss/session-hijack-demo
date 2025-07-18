# session-hijack-demo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English version](README.md)

## 概要

`session-hijack-demo` は、HTTPクッキーを使用したセッション管理の基本的な動作と、その脆弱性の一つであるセッションハイジャック攻撃を簡易的に再現するためのデモンストレーション用リポジトリです。本リポジトリの目的は、学習目的のためにセッションセキュリティの重要性を理解することにあります。

**警告**: このコードは教育および研究目的のためにのみ提供されています。実際のシステムに対して許可なく使用したり、不正な目的で使用したりすることは**固く禁じられています**。

## 目的

このリポジトリは、以下の目的のために開発されました。

1. **HTTPセッション管理の理解**: HTTPクッキーを用いたサーバーサイドでのセッション管理の仕組みを学ぶ。
2. **セッションハイジャックの原理**: 攻撃者が有効なセッションクッキーを盗み出し、正規ユーザーになりすまして認証済みリソースにアクセスする原理を理解する。
3. **セキュリティ意識の向上**: Webアプリケーションにおけるセッションセキュリティの重要性と、クッキー保護の必要性を認識する。

## 機能

* **`http_server.py`**:
  * クッキーベースのセッション管理を実装した簡易HTTPサーバー。
  * ユーザー登録 (`/register`)、ログイン (`/login`) 機能を提供。
  * ログイン済みのユーザーのみがアクセスできる保護されたリソース (`/dashboard`) を提供。
  * セッションIDを `session_id` という名前のHTTPクッキーとして発行。
* **`login_client.py`**:
  * `http_server.py` に対してユーザー登録を行い、その後ログインを実行する正規ユーザーをシミュレートするクライアント。
  * ログイン成功時にサーバーから発行されたセッションクッキーを読み取り、`session_cookie.txt` ファイルに保存する。
  * 保存したクッキーを使用して、保護されたリソース (`/dashboard`) にアクセスし、自分の情報が表示されることを確認する。
* **`attack_client.py`**:
  * 攻撃者をシミュレートするクライアント。
  * `login_client.py` が保存した `session_cookie.txt` ファイルからセッションIDを不正に読み込む。
  * 読み込んだセッションIDクッキーをHTTPリクエストに含めて、`http_server.py` の保護されたリソース (`/dashboard`) にアクセスする。
  * これにより、正規ユーザーとして認証されることなく、そのユーザーのセッションを乗っ取り、情報を入手できることを実証する。

## ファイル構成

```tree
.
├── README.md
├── README_ja.md
└── session-hijack-demo
    ├── http_server.py
    ├── login_client.py
    └── attack_client.md
    ├── session_cookie.txt  # login_client.py 実行時に生成される
```

## セットアップ

### 前提条件

* Python 3.6+ がインストールされていること。
* `pip` パッケージマネージャーが利用可能であること。

### 必要なライブラリのインストール

`login_client.py` および `attack_client.py` は `requests` ライブラリを使用します。以下のコマンドを実行してインストールしてください。

```bash
pip install requests
```

## 各ツールの使用方法

### セッションハイジャックのシナリオ再現手順

以下の手順で各スクリプトを順番に実行し、セッションハイジャック攻撃を再現します。

1. **HTTPサーバーを起動する (`http_server.py`)**
    * 最初のターミナルを開き、以下のコマンドを実行します。

        ```bash
        python3 http_server.py
        ```

    * サーバーは `127.0.0.1:8000` でリッスンを開始します。
    * *サーバー出力例:*

        ```bash
        Serving HTTP on 127.0.0.1:8000...
        Press Ctrl+C to stop the server.
        ```

2. **ログイン用クライアントを実行する (`login_client.py`)**
    * サーバーが実行中の状態で、**別のターミナル**を開き、以下のコマンドを実行します。

        ```bash
        python3 login_client.py
        ```

    * このスクリプトは、ユーザー (`testuser`) の登録、ログイン、そしてダッシュボードへのアクセスを実行します。
    * ログイン成功時に、サーバーから受け取ったセッションIDが `session_cookie.txt` ファイルに保存されます。
    * *ログイン用クライアント出力例:* (セッションIDは実行ごとに変わります)

        ```bash
        Attempting to register user: testuser
        Registration response status: 201
        ...
        Login successful.
        Session ID obtained: [UNIQUE_SESSION_ID]
        Session ID saved to session_cookie.txt
        ...
        Successfully accessed dashboard.
        Login Client operations completed.
        Please check 'session_cookie.txt' for the saved session ID.
        ```

3. **攻撃用クライアントを実行する (`attack_client.py`)**
    * サーバーとログイン用クライアントが実行中の状態（またはログイン用クライアントが完了した直後で `session_cookie.txt` が存在する場合）で、**さらに別のターミナル**を開き、以下のコマンドを実行します。

        ```bash
        python3 attack_client.py
        ```

    * このスクリプトは `session_cookie.txt` からセッションIDを読み込み、それを使ってサーバーの保護されたリソースにアクセスします。
    * *攻撃用クライアント出力例:*

        ```bash
        --- Attempting Session Hijack ---
        Successfully read session ID from file: [UNIQUE_SESSION_ID]
        Accessing dashboard with hijacked session ID: [UNIQUE_SESSION_ID]
        Hijacked session access status: 200
        Hijacked session content:
        <h1>Welcome, testuser!</h1><p>This is your confidential information:</p><pre>{...}</pre><p><a href='/logout'>Logout</a></p>

        --- Session Hijack SUCCESSFUL! ---
        Successfully accessed the dashboard using the hijacked session ID.
        The attacker has gained access to 'testuser's confidential information.
        Attack Client operations completed.
        ```

### セッションハイジャックの成功確認

* `attack_client.py` の出力で「`--- Session Hijack SUCCESSFUL! ---`」というメッセージが表示され、**正規ユーザー (`testuser`) の情報が含まれるダッシュボードの内容が表示されれば、セッションハイジャックが成功したことになります。**

## 免責事項

このリポジトリのコードは、**教育およびデモンストレーション目的のみ**のために開発されました。

* 本コードを実際のシステムやネットワークに対して許可なく使用したり、不正な目的で使用したりすることは**固く禁じられています**。
* 開発者は、本コードの誤用または不正使用によって生じるいかなる損害についても責任を負いません。
* 本リポジトリは、セッションハイジャックの脅威を理解し、よりセキュアなWebアプリケーションを開発するための知識向上に貢献することを意図しています。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については `LICENSE` ファイルを参照してください。
