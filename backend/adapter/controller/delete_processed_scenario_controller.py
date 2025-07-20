from typing import Dict, Union
from usecase.delete_processed_scenario import (
    DeleteProcessedScenarioUseCase,
    DeleteProcessedScenarioInput,
    DeleteProcessedScenarioOutput,
)


class DeleteProcessedScenarioController:
    def __init__(self, uc: DeleteProcessedScenarioUseCase):
        self.uc = uc

    def execute(
        self, input_data: DeleteProcessedScenarioInput
    ) -> Dict[str, Union[int, DeleteProcessedScenarioOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
