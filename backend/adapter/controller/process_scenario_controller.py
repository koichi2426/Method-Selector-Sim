from typing import Dict, Union, List
from backend.usecase.process_scenario import (
    ProcessScenarioUseCase,
    ProcessScenarioInput,
    ProcessScenarioOutput,
)


class ProcessScenarioController:
    def __init__(self, uc: ProcessScenarioUseCase):
        self.uc = uc

    def execute(
        self, input_data: ProcessScenarioInput
    ) -> Dict[str, Union[int, List[ProcessScenarioOutput], Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 201, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
