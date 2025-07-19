from typing import Dict, Union, List
from usecase.find_all_models import (
    FindAllModelsUseCase,
    FindAllModelsOutput,
)


class FindAllModelsAction:
    def __init__(self, uc: FindAllModelsUseCase):
        self.uc = uc

    def execute(
        self,
    ) -> Dict[str, Union[int, List[FindAllModelsOutput], Dict[str, str]]]:
        try:
            output, err = self.uc.execute()
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
