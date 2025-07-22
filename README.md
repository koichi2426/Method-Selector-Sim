# Method-Selector-Sim

> メソッド選択エンジンのためのシミュレーション環境

## 概要 (Overview)

このリポジトリは、**軽量なメソッド選択エンジン**の開発・検証を行うためのWebベースのシミュレーション環境です。
状態ログの生成からモデルの検証まで、一連のデータパイプラインを視覚的に確認し、各モジュールを個別に操作・管理することを目的としています。

## UIプレビュー (Screenshot)

アプリケーションを起動すると、以下のようなパイプラインのホーム画面が表示されます。

<img width="3420" height="1958" alt="image" src="https://github.com/user-attachments/assets/e8d34a30-af59-4d03-8e5a-e76b07bb0c2c" />



## 起動方法 (Getting Started)

DockerとDocker Composeがインストールされていれば、以下の簡単なステップでアプリケーションを起動できます。

1.  **リポジトリをクローン**

    ```bash
    git clone https://github.com/koichi2426/Method-Selector-Sim.git
    ```

2.  **プロジェクトディレクトリに移動**

    ```bash
    cd Method-Selector-Sim/frontend
    ```

3.  **Dockerコンテナをビルドして起動**

    ```bash
    docker-compose up --build -d
    ```
    開発用なら以下
    ```bash
    docker-compose -f docker-compose.dev.yml up --build
    ```

      * `--build`: イメージを再ビルドします（初回起動時やDockerfile変更時に必要）。
      * `-d`: バックグラウンドでコンテナを起動します（デタッチモード）。

4.  **ブラウザでアクセス**
    起動後、ブラウザで以下のURLにアクセスしてください。
    [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)

5.  **コンテナの停止**
    アプリケーションを停止する場合は、以下のコマンドを実行します。

    ```bash
    docker-compose down
    ```


## データベースのマイグレーション手順 (Alembic)

`infrastructure/database/models.py`のテーブル定義を変更した際に、その変更をデータベースに反映させるための手順です。

1.  **マイグレーションファイルを作成**

    `models.py`の変更内容と現在のデータベースの状態を比較し、差分を適用するためのスクリプトを自動生成します。
    ```bash
    docker-compose -f docker-compose.dev.yml run --rm backend python -m alembic revision --autogenerate -m "変更内容のコメント"
    ```

2.  **データベースに変更を適用**

    ```bash
    docker-compose -f docker-compose.dev.yml run --rm backend python -m alembic upgrade head
    ```


## データベースの確認方法

データベースに正しくテーブルが作成され、データが保存されているかを確認する手順です。

1.  **MySQLコンテナに入る**

    ```bash
    docker-compose -f docker-compose.dev.yml exec db /bin/sh
    ```

2.  **MySQLにログインする**

    ```bash
    mysql -u root -p
    ```

3.  **使用するデータベースを選択する**

    ```bash
    USE method_selector_db;
    ```

4.  **テーブル一覧を表示する**
    ```bash
    SHOW TABLES;
    ```

5.  *テーブルの中身を確認する**
    （例として`datasets`テーブルを表示します。他のテーブル名に変えても使えます）
    ```bash
    SELECT * FROM datasets;
    ```


## アーキテクチャ
<img width="16384" height="14581" alt="image" src="https://github.com/user-attachments/assets/31190525-7a0e-4948-b4ba-de669b0882ee" />

