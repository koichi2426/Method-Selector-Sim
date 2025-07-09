# Node.jsの公式イメージをベースにする
FROM node:18-alpine

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存ライブラリをインストール
RUN npm install

# アプリケーションのコードをコピー
COPY . .

# 開発サーバーを起動
CMD ["npm", "run", "dev"]