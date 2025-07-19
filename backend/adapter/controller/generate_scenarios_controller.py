from typing import Dict, Union, List
from usecase.generate_scenarios import (
    GenerateScenariosUseCase,
    GenerateScenariosInput,
    GenerateScenariosOutput,
)


class GenerateScenariosAction:
    def __init__(self, uc: GenerateScenariosUseCase):
        self.uc = uc

    def execute(
        self, input_data: GenerateScenariosInput
    ) -> Dict[str, Union[int, List[GenerateScenariosOutput], Dict[str, str]]]:
        try:
            output, err = self.uc.execute(input_data)
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 201, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
