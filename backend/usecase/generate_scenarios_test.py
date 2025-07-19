import unittest
import uuid
from unittest.mock import Mock, MagicMock
from typing import List

from domain import (
    Scenario,
    MethodProfile,
    Situation,
    LogGenerationConfig,
)
from .generate_scenarios import (
    GenerateScenariosInput,
    GenerateScenariosOutput,
    GenerateScenariosPresenter,
    GenerateScenariosInteractor,
    new_generate_scenarios_interactor,
)


class MockScenarioRepository:
    def __init__(self):
        self.created_scenarios = []
    
    def create(self, scenario: Scenario) -> Scenario:
        # 実際のリポジトリの動作をシミュレート
        self.created_scenarios.append(scenario)
        return scenario


class MockGenerateScenariosPresenter(GenerateScenariosPresenter):
    def __init__(self):
        self.output_calls = []
    
    def output(self, scenario: Scenario) -> GenerateScenariosOutput:
        self.output_calls.append(scenario)
        return GenerateScenariosOutput(
            ID=scenario.ID,
            state=scenario.state,
            method_group=scenario.method_group,
            target_method=scenario.target_method,
            negative_method_group=scenario.negative_method_group,
        )


class MockScenarioGeneratorDomainService:
    def __init__(self, scenarios_to_return: List[Scenario]):
        self.scenarios_to_return = scenarios_to_return
        self.generate_calls = []
    
    def generate_scenarios(self, config: LogGenerationConfig) -> List[Scenario]:
        self.generate_calls.append(config)
        return self.scenarios_to_return


class TestGenerateScenariosInput(unittest.TestCase):
    def test_create_input_with_valid_data(self):
        """有効なデータでGenerateScenariosInputを作成できることをテスト"""
        method_profile = MethodProfile(
            method_name="test_method",
            context_keywords=["test", "keyword"]
        )
        situation = Situation(
            user_information="test_user_info",
            environmental_information="test_env_info"
        )
        
        input_data = GenerateScenariosInput(
            output_count=5,
            method_pool=[method_profile],
            situations=[situation]
        )
        
        self.assertEqual(input_data.output_count, 5)
        self.assertEqual(len(input_data.method_pool), 1)
        self.assertEqual(len(input_data.situations), 1)
        self.assertEqual(input_data.method_pool[0].method_name, "test_method")
        self.assertEqual(input_data.situations[0].user_information, "test_user_info")


class TestGenerateScenariosOutput(unittest.TestCase):
    def test_create_output_with_valid_data(self):
        """有効なデータでGenerateScenariosOutputを作成できることをテスト"""
        test_id = uuid.uuid4()
        output = GenerateScenariosOutput(
            ID=test_id,
            state="active",
            method_group="test_group",
            target_method="test_method",
            negative_method_group="negative_group"
        )
        
        self.assertEqual(output.ID, test_id)
        self.assertEqual(output.state, "active")
        self.assertEqual(output.method_group, "test_group")
        self.assertEqual(output.target_method, "test_method")
        self.assertEqual(output.negative_method_group, "negative_group")


class TestGenerateScenariosPresenter(unittest.TestCase):
    def test_presenter_output(self):
        """プレゼンターが正しくScenarioをGenerateScenariosOutputに変換することをテスト"""
        presenter = MockGenerateScenariosPresenter()
        
        test_id = uuid.uuid4()
        scenario = Scenario(
            ID=test_id,
            state="active",
            method_group="test_group",
            target_method="test_method",
            negative_method_group="negative_group"
        )
        
        output = presenter.output(scenario)
        
        self.assertEqual(output.ID, test_id)
        self.assertEqual(output.state, "active")
        self.assertEqual(output.method_group, "test_group")
        self.assertEqual(output.target_method, "test_method")
        self.assertEqual(output.negative_method_group, "negative_group")
        self.assertEqual(len(presenter.output_calls), 1)
        self.assertEqual(presenter.output_calls[0], scenario)


class TestGenerateScenariosInteractor(unittest.TestCase):
    def setUp(self):
        """テストの前準備"""
        self.test_id = uuid.uuid4()
        self.test_scenario = Scenario(
            ID=self.test_id,
            state="active",
            method_group="test_group",
            target_method="test_method",
            negative_method_group="negative_group"
        )
        
        self.method_profile = MethodProfile(
            method_name="test_method",
            context_keywords=["test", "keyword"]
        )
        self.situation = Situation(
            user_information="test_user_info",
            environmental_information="test_env_info"
        )
        
        self.input_data = GenerateScenariosInput(
            output_count=2,
            method_pool=[self.method_profile],
            situations=[self.situation]
        )

    def test_execute_success(self):
        """正常な実行をテスト"""
        # モックオブジェクトの準備
        repo = MockScenarioRepository()
        presenter = MockGenerateScenariosPresenter()
        domain_service = MockScenarioGeneratorDomainService([self.test_scenario])
        
        interactor = GenerateScenariosInteractor(
            repo=repo,
            presenter=presenter,
            domain_service=domain_service,
            timeout_sec=10
        )
        
        # 実行
        outputs, error = interactor.execute(self.input_data)
        
        # 検証
        self.assertIsNone(error)
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0].ID, self.test_id)
        self.assertEqual(outputs[0].state, "active")
        
        # ドメインサービスが正しく呼ばれたことを確認
        self.assertEqual(len(domain_service.generate_calls), 1)
        config = domain_service.generate_calls[0]
        self.assertEqual(config.output_count, 2)
        self.assertEqual(len(config.method_pool), 1)
        self.assertEqual(len(config.situations), 1)
        
        # リポジトリが正しく呼ばれたことを確認
        self.assertEqual(len(repo.created_scenarios), 1)
        self.assertEqual(repo.created_scenarios[0], self.test_scenario)
        
        # プレゼンターが正しく呼ばれたことを確認
        self.assertEqual(len(presenter.output_calls), 1)
        self.assertEqual(presenter.output_calls[0], self.test_scenario)

    def test_execute_with_multiple_scenarios(self):
        """複数のシナリオを生成する場合をテスト"""
        # 複数のシナリオを準備
        scenario1 = Scenario(
            ID=uuid.uuid4(),
            state="active",
            method_group="group1",
            target_method="method1",
            negative_method_group="negative1"
        )
        scenario2 = Scenario(
            ID=uuid.uuid4(),
            state="inactive",
            method_group="group2",
            target_method="method2",
            negative_method_group="negative2"
        )
        
        repo = MockScenarioRepository()
        presenter = MockGenerateScenariosPresenter()
        domain_service = MockScenarioGeneratorDomainService([scenario1, scenario2])
        
        interactor = GenerateScenariosInteractor(
            repo=repo,
            presenter=presenter,
            domain_service=domain_service,
            timeout_sec=10
        )
        
        # 実行
        outputs, error = interactor.execute(self.input_data)
        
        # 検証
        self.assertIsNone(error)
        self.assertEqual(len(outputs), 2)
        self.assertEqual(outputs[0].method_group, "group1")
        self.assertEqual(outputs[1].method_group, "group2")
        
        # リポジトリとプレゼンターが2回呼ばれたことを確認
        self.assertEqual(len(repo.created_scenarios), 2)
        self.assertEqual(len(presenter.output_calls), 2)

    def test_execute_with_exception(self):
        """例外が発生した場合をテスト"""
        repo = MockScenarioRepository()
        presenter = MockGenerateScenariosPresenter()
        
        # 例外を発生させるドメインサービス
        domain_service = Mock()
        domain_service.generate_scenarios.side_effect = Exception("Test error")
        
        interactor = GenerateScenariosInteractor(
            repo=repo,
            presenter=presenter,
            domain_service=domain_service,
            timeout_sec=10
        )
        
        # 実行
        outputs, error = interactor.execute(self.input_data)
        
        # 検証
        self.assertIsNotNone(error)
        self.assertEqual(str(error), "Test error")
        self.assertEqual(len(outputs), 0)
        
        # リポジトリとプレゼンターは呼ばれていないことを確認
        self.assertEqual(len(repo.created_scenarios), 0)
        self.assertEqual(len(presenter.output_calls), 0)

    def test_execute_with_empty_scenarios(self):
        """空のシナリオリストを返す場合をテスト"""
        repo = MockScenarioRepository()
        presenter = MockGenerateScenariosPresenter()
        domain_service = MockScenarioGeneratorDomainService([])
        
        interactor = GenerateScenariosInteractor(
            repo=repo,
            presenter=presenter,
            domain_service=domain_service,
            timeout_sec=10
        )
        
        # 実行
        outputs, error = interactor.execute(self.input_data)
        
        # 検証
        self.assertIsNone(error)
        self.assertEqual(len(outputs), 0)
        
        # リポジトリとプレゼンターは呼ばれていないことを確認
        self.assertEqual(len(repo.created_scenarios), 0)
        self.assertEqual(len(presenter.output_calls), 0)


class TestNewGenerateScenariosInteractor(unittest.TestCase):
    def test_factory_function(self):
        """ファクトリ関数が正しくインターラクターを作成することをテスト"""
        repo = MockScenarioRepository()
        presenter = MockGenerateScenariosPresenter()
        domain_service = MockScenarioGeneratorDomainService([])
        
        interactor = new_generate_scenarios_interactor(
            repo=repo,
            presenter=presenter,
            domain_service=domain_service,
            timeout_sec=15
        )
        
        # 検証
        self.assertIsInstance(interactor, GenerateScenariosInteractor)
        self.assertEqual(interactor.repo, repo)
        self.assertEqual(interactor.presenter, presenter)
        self.assertEqual(interactor.domain_service, domain_service)
        self.assertEqual(interactor.timeout_sec, 15)


if __name__ == '__main__':
    unittest.main() 