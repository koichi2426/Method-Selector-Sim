from typing import Dict, Union, List
from usecase.find_all_scenario import (
    FindAllScenarioUseCase,
    FindAllScenarioOutput,
)


class FindAllScenarioController:
    def __init__(self, uc: FindAllScenarioUseCase):
        self.uc = uc

    def execute(
        self,
    ) -> Dict[str, Union[int, List[FindAllScenarioOutput], Dict[str, str]]]:
        try:
            output, err = self.uc.execute()
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}