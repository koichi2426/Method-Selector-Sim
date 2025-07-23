import random
from typing import List

from domain.training_ready_scenario import TrainingReadyScenario
from domain.triplet import Triplet, NewTriplet
from domain.custom_uuid import NewUUID
from domain.triplet_former_domain_service import TripletFormerDomainService

class TripletFormerDomainServiceImpl(TripletFormerDomainService):
    """
    TripletFormerDomainServiceの具体的な実装クラス。
    """
    def form_triplets_from(self, scenario: TrainingReadyScenario) -> Triplet:
        """
        1つのTrainingReadyScenarioから、1つのTripletを生成する。
        ネガティブメソッドが複数ある場合は、その中からランダムに1つを選択する。
        """
        # 1. Anchor (アンカー) を設定
        anchor = scenario.state

        # 2. Positive (正例) を特定
        # .split(',') は空文字列の場合 [''] を返すので、filterで除去する
        all_methods = {method.strip() for method in scenario.method_group.split(',') if method.strip()}
        negative_methods_set = {method.strip() for method in scenario.negative_method_group.split(',') if method.strip()}

        positive_methods = all_methods - negative_methods_set
        
        if not positive_methods:
            raise ValueError(f"Could not determine a positive method for scenario ID {scenario.ID.value}")
        
        # 正例は1つであると仮定
        positive = positive_methods.pop()

        # 3. Negative (負例) をランダムに選択
        negative_methods_list = list(negative_methods_set)
        if not negative_methods_list:
            raise ValueError(f"No negative methods available for scenario ID {scenario.ID.value}")
        
        negative = random.choice(negative_methods_list)

        # 4. Tripletオブジェクトを生成して返す
        new_triplet = NewTriplet(
            ID=NewUUID(),
            TrainingReadyScenario_ID=scenario.ID,
            anchor=anchor,
            positive=positive,
            negative=negative
        )

        return new_triplet