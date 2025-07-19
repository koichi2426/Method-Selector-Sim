from typing import Dict, Union
from usecase.delete_triplets import (
    DeleteTripletsUseCase,
    DeleteTripletsInput,
    DeleteTripletsOutput,
)


class DeleteTripletsAction:
    def __init__(self, uc: DeleteTripletsUseCase):
        self.uc = uc

    def execute(
        self, input_data: DeleteTripletsInput
    ) -> Dict[str, Union[int, DeleteTripletsOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
