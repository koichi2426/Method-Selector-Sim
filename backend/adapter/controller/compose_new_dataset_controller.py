from typing import Dict, Union
from usecase.compose_new_dataset import (
    ComposeNewDatasetUseCase,
    ComposeNewDatasetInput,
    ComposeNewDatasetOutput,
)


class ComposeNewDatasetAction:
    def __init__(self, uc: ComposeNewDatasetUseCase):
        self.uc = uc

    def execute(
        self, input_data: ComposeNewDatasetInput
    ) -> Dict[str, Union[int, ComposeNewDatasetOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 201, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}