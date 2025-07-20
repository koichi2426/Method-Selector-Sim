from typing import Dict, Union
from backend.usecase.delete_dataset import (
    DeleteDatasetUseCase,
    DeleteDatasetInput,
    DeleteDatasetOutput,
)


class DeleteDatasetController:
    def __init__(self, uc: DeleteDatasetUseCase):
        self.uc = uc

    def execute(
        self, input_data: DeleteDatasetInput
    ) -> Dict[str, Union[int, DeleteDatasetOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}