from typing import Dict, Union
from usecase.form_triplets_from import (
    FormTripletsFromUseCase,
    FormTripletsFromInput,
    FormTripletsFromOutput,
)


class FormTripletsFromController:
    def __init__(self, uc: FormTripletsFromUseCase):
        self.uc = uc

    def execute(
        self, input_data: FormTripletsFromInput
    ) -> Dict[str, Union[int, FormTripletsFromOutput, Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 201, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
