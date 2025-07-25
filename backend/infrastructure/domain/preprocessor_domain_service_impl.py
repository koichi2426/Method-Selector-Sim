from domain.preprocessor_domain_service import PreprocessorDomainService
from domain.scenario import Scenario
from domain.training_ready_scenario import TrainingReadyScenario, NewTrainingReadyScenario
from domain.custom_uuid import NewUUID
from datetime import datetime # datetimeをインポート

class PreprocessorDomainServiceImpl(PreprocessorDomainService):
    """
    PreprocessorDomainServiceの具体的な実装クラス。
    """
    def process_scenario(self, scenario: Scenario) -> TrainingReadyScenario:
        """
        Scenarioオブジェクトを受け取り、TrainingReadyScenarioオブジェクトに変換する。
        
        Args:
            scenario (Scenario): 処理対象のシナリオ。

        Returns:
            TrainingReadyScenario: 訓練に適した形式に変換されたシナリオ。
        """
        
        # 元のシナリオから情報を引き継ぎ、新しいIDを付与して
        # TrainingReadyScenarioオブジェクトを生成する。
        processed_scenario = NewTrainingReadyScenario(
            ID=NewUUID(),
            Scenario_ID=scenario.ID,
            state=scenario.state,
            method_group=scenario.method_group,
            negative_method_group=scenario.negative_method_group,
            created_at=datetime.now() # 現在時刻をcreated_atとして追加
        )
        
        return processed_scenario
