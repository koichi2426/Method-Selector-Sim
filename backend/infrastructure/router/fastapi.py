import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import time

# --- プレースホルダとなる各層のモジュール ---
# 実際のアプリケーションではこれらは別々のファイルに存在し、
# 依存性注入コンテナなどによって解決されます。

class SQL:
    # データベースハンドラのダミー
    pass

# --- Usecase / Presenter / Repository / Action のプレースホルダ ---
# これらは実際には各ファイルからインポートされます
from usecase.find_all_scenario import FindAllScenarioUseCase, FindAllScenarioOutput, FindAllScenarioPresenter
from usecase.create_scenario import CreateScenarioUseCase, CreateScenarioInput, CreateScenarioOutput, CreateScenarioPresenter
from adapter.repository.scenario_mysql import ScenarioMySQL
from adapter.api.action.find_all_scenario_action import FindAllScenarioAction
from adapter.api.action.create_scenario_action import CreateScenarioAction


# --- FastAPIサーバーエンジン ---

class FastAPIEngine:
    """
    GoのginEngine構造体に相当する、サーバー全体を管理するクラス。
    """
    def __init__(
        self,
        db: SQL,
        port: int,
        timeout_sec: float,
    ):
        self.router = FastAPI(title="Clean Architecture API")
        self.db = db
        self.port = port
        self.ctx_timeout = timeout_sec
        self._set_app_handlers()

    def listen(self):
        """
        サーバーを起動する。GoのListenメソッドに相当。
        UvicornがGraceful Shutdownを処理する。
        """
        print(f"INFO: Starting HTTP Server port={self.port}")
        uvicorn.run(self.router, host="0.0.0.0", port=self.port)

    def _set_app_handlers(self):
        """
        APIエンドポイントをルーターに登録する。
        GoのsetAppHandlersメソッドに相当。
        """
        self.router.get("/v1/scenarios")(self._build_find_all_scenario_action())
        self.router.post("/v1/scenarios")(self._build_create_scenario_action())
        self.router.get("/v1/health")(self._healthcheck())

    def _build_find_all_scenario_action(self):
        """
        FindAllScenarioの依存性を解決し、ハンドラ関数を構築する。
        GoのbuildFindAllAccountActionメソッドに相当。
        """
        def handler():
            # リクエストごとに依存性を解決
            repo = ScenarioMySQL(self.db)
            presenter = FindAllScenarioPresenter()
            usecase = FindAllScenarioUseCase(repo, presenter)
            action = FindAllScenarioAction(usecase)

            # アクションを実行し、レスポンスを生成
            response_dict = action.execute()
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_create_scenario_action(self):
        """
        CreateScenarioの依存性を解決し、ハンドラ関数を構築する。
        GoのbuildCreateAccountActionメソッドに相当。
        """
        async def handler(request: Request):
            # リクエストごとに依存性を解決
            repo = ScenarioMySQL(self.db)
            presenter = CreateScenarioPresenter()
            usecase = CreateScenarioUseCase(repo, presenter)
            action = CreateScenarioAction(usecase)

            # アクションを実行し、レスポンスを生成
            request_body = await request.body()
            response_dict = action.execute(request_body)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _healthcheck(self):
        """ヘルスチェック用のハンドラ関数を返す"""
        def handler():
            return {"status": "ok"}
        return handler


def new_fastapi_server(
    db: SQL,
    port: int,
    timeout_sec: float,
) -> FastAPIEngine:
    """
    FastAPIEngineのインスタンスを生成するファクトリ関数。
    GoのnewGinServerに相当。
    """
    return FastAPIEngine(
        db=db,
        port=port,
        timeout_sec=timeout_sec,
    )


# --- アプリケーションのエントリーポイント ---

if __name__ == "__main__":
    # 実際のアプリケーションでは、ここで環境変数などから設定を読み込む
    db_handler = SQL() # ここで実際のDBハンドラを初期化
    port = 8000
    timeout = 10.0

    # サーバーエンジンを生成し、起動
    server = new_fastapi_server(
        db=db_handler,
        port=port,
        timeout_sec=timeout,
    )
    server.listen()