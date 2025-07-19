from typing import Dict, Union
from usecase.train_new_model import (
    TrainNewModelUseCase,
    TrainNewModelInput,
    TrainNewModelOutput,
)


class TrainNewModelAction:
    def __init__(self, uc: TrainNewModelUseCase):
        self.uc = uc

    def execute(
        self, input_data: TrainNewModelInput
    ) -> Dict[str, Union[int, TrainNewModelOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 201, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
