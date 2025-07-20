import mysql.connector
from mysql.connector import pooling
from typing import Any, List, Optional

# --- 依存するインターフェースと設定クラスをインポート ---
# (ご指摘の通り、sqlインターフェースはadapter層から、configはinfrastructure層からインポート)
from adapter.repository.sql import SQL, Tx, Row, Rows, RowData
from infrastructure.database.config import MySQLConfig


# --- Rows / Row インターフェースのMySQL実装 ---

class MySQLRow(Row):
    """
    単一の結果行をラップするクラス。
    """
    def __init__(self, row_data: Optional[RowData]):
        self._row_data = row_data

    def scan(self, *dest: Any) -> None:
        """
        取得した行データを指定された変数に格納する。
        Pythonではこのパターンは稀で、直接タプルとして受け取るのが一般的。
        """
        if self._row_data is None:
            # Goのsql.ErrNoRowsに相当するエラー
            raise ValueError("行が見つかりません")
        
        if len(dest) != len(self._row_data):
            raise ValueError(f"引数の数({len(dest)})とカラムの数({len(self._row_data)})が一致しません")

        # この実装はGoのScanを模倣するためのもので、実際にはあまり使われない
        for i, val in enumerate(self._row_data):
            # 概念的な実装
            print(f"警告: scan()は概念的な実装です。dest[{i}]に{val}をセットしようとしました。")


class MySQLRows(Rows):
    """
    複数の結果行（カーソル）をラップするクラス。
    """
    def __init__(self, cursor):
        self._cursor = cursor
        self._current_row: Optional[RowData] = None

    def scan(self, *dest: Any) -> None:
        if self._current_row is None:
            raise ValueError("スキャンする行がありません。next()を先に呼び出してください。")
        
        if len(dest) != len(self._current_row):
             raise ValueError(f"引数の数({len(dest)})とカラムの数({len(self._current_row)})が一致しません")
        
        # MySQLRowと同様に概念的な実装
        print(f"警告: scan()は概念的な実装です。")

    def next(self) -> bool:
        self._current_row = self._cursor.fetchone()
        return self._current_row is not None

    def err(self) -> Optional[Exception]:
        # DB-API 2.0ではイテレーション中のエラーは即座に例外として発生するため、
        # このメソッドは通常Noneを返すか、未実装とする。
        return None

    def close(self) -> None:
        self._cursor.close()

    def fetchone(self) -> Optional[RowData]:
        return self._cursor.fetchone()

    def fetchall(self) -> List[RowData]:
        return self._cursor.fetchall()
    
    def __iter__(self):
        return self._cursor.__iter__()


# --- Transaction インターフェースのMySQL実装 ---

class MySQLTx(Tx):
    """
    トランザクションをラップするクラス。
    """
    def __init__(self, connection):
        self.conn = connection
        # MySQLではトランザクション開始を明示的に行う
        self.conn.start_transaction()
        self.cursor = self.conn.cursor()

    def execute(self, query: str, *params: Any) -> None:
        self.cursor.execute(query, params)

    def query(self, query: str, *params: Any) -> Rows:
        self.cursor.execute(query, params)
        return MySQLRows(self.cursor)

    def query_row(self, query: str, *params: Any) -> Row:
        self.cursor.execute(query, params)
        return MySQLRow(self.cursor.fetchone())

    def commit(self) -> None:
        self.conn.commit()
        self.cursor.close()

    def rollback(self) -> None:
        self.conn.rollback()
        self.cursor.close()


# --- Main SQL インターフェースのMySQL実装 ---

class MySQLHandler(SQL):
    """
    データベース接続全体を管理するハンドラ。
    """
    def __init__(self, config: MySQLConfig):
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mysql_pool",
                pool_size=10,
                user=config.user,
                password=config.password,
                host=config.host,
                port=config.port,
                database=config.database
            )
        except Exception as e:
            print(f"データベース接続に失敗しました: {e}")
            raise

    def _get_connection(self):
        return self.pool.get_connection()

    def _put_connection(self, conn):
        conn.close() # mysql-connector-pythonではclose()でプールに返却される

    def execute(self, query: str, *params: Any) -> None:
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self._put_connection(conn)

    def query(self, query: str, *params: Any) -> Rows:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        # 注意: このカーソルと接続は呼び出し元で閉じる必要がある
        return MySQLRows(cur)

    def query_row(self, query: str, *params: Any) -> Row:
        conn = self._get_connection()
        row_data = None
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                row_data = cur.fetchone()
        finally:
            self._put_connection(conn)
        return MySQLRow(row_data)

    def begin_tx(self) -> Tx:
        conn = self._get_connection()
        return MySQLTx(conn)

    def close_pool(self):
        """アプリケーション終了時にコネクションプールを閉じる"""
        # mysql-connector-pythonのプールには明示的なcloseallがない
        # アプリケーション終了時に自動的に処理される
        print("MySQLコネクションプールはアプリケーション終了時に自動的にクリーンアップされます。")


def NewMySQLHandler(config: MySQLConfig) -> MySQLHandler:
    """
    MySQLHandlerのインスタンスを生成するファクトリ関数。
    """
    return MySQLHandler(config)