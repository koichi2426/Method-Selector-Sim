# Pythonの公式イメージをベースにする
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存ライブラリのリストをコピー
COPY requirements.txt .

# 依存ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# コンテナ起動時にAPIサーバーを実行（0.0.0.0を指定するのが重要）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]