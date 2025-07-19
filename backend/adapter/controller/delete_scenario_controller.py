from typing import Dict, Union
from usecase.delete_scenario import (
    DeleteScenarioUseCase,
    DeleteScenarioInput,
    DeleteScenarioOutput,
)


class DeleteScenarioAction:
    def __init__(self, uc: DeleteScenarioUseCase):
        self.uc = uc

    def execute(
        self, input_data: DeleteScenarioInput
    ) -> Dict[str, Union[int, DeleteScenarioOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
