from typing import Dict, Union
from backend.usecase.evaluate_model import (
    EvaluateModelUseCase,
    EvaluateModelInput,
    EvaluateModelOutput,
)


class EvaluateModelController:
    def __init__(self, uc: EvaluateModelUseCase):
        self.uc = uc

    def execute(
        self, input_data: EvaluateModelInput
    ) -> Dict[str, Union[int, EvaluateModelOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 201, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
