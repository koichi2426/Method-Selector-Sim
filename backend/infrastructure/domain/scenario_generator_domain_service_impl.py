import random
from typing import List
from datetime import datetime  # datetimeをインポート

from domain.log_generation_config import LogGenerationConfig
from domain.scenario import Scenario, NewScenario
from domain.custom_uuid import NewUUID  # 修正: 正しいファイルからインポート
from domain.scenario_generator_domain_service import ScenarioGeneratorDomainService

class ScenarioGeneratorDomainServiceImpl(ScenarioGeneratorDomainService):
    """
    ScenarioGeneratorDomainServiceの具体的な実装クラス。
    """
    def generate_scenarios(self, config: LogGenerationConfig) -> List[Scenario]:
        """
        設定に基づいて、指定された数のシナリオを生成する。
        この実装では、あらかじめ用意された固定のモックシナリオを返す。
        """
        
        # モックとして用意したシナリオのリスト (英語)
        mock_scenarios = [
            NewScenario(
                ID=NewUUID(),
                state="User is on the login page",
                method_group="emailLogin, googleLogin, appleLogin",
                target_method="emailLogin - Login with email and password",
                negative_method_group="googleLogin, appleLogin",
                created_at=datetime.now() # created_atを追加
            ),
            NewScenario(
                ID=NewUUID(),
                state="User pressed 'Add to Cart' on the product detail page",
                method_group="addToCart, viewCart, checkout",
                target_method="addToCart - Add product to the shopping cart",
                negative_method_group="viewCart, checkout",
                created_at=datetime.now() # created_atを追加
            ),
            NewScenario(
                ID=NewUUID(),
                state="User entered credit card information on the payment screen",
                method_group="validateCard, processPayment, showReceipt",
                target_method="processPayment - Execute the payment process",
                negative_method_group="validateCard, showReceipt",
                created_at=datetime.now() # created_atを追加
            ),
            NewScenario(
                ID=NewUUID(),
                state="User opened the profile edit page",
                method_group="updateProfile, changePassword, uploadAvatar",
                target_method="updateProfile - Update user information",
                negative_method_group="changePassword, uploadAvatar",
                created_at=datetime.now() # created_atを追加
            )
        ]

        # output_countの数だけモックシナリオを返す
        # 要求された数が多い場合は、用意したモックをすべて返す
        return mock_scenarios[:config.output_count]
