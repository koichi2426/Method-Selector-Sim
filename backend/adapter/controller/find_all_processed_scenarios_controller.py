from typing import Dict, Union, List
from usecase.find_all_processed_scenarios import (
    FindAllProcessedScenariosUseCase,
    FindAllProcessedScenariosOutput,
)


class FindAllProcessedScenariosController:
    def __init__(self, uc: FindAllProcessedScenariosUseCase):
        self.uc = uc

    def execute(
        self,
    ) -> Dict[str, Union[int, List[FindAllProcessedScenariosOutput], Dict[str, str]]]:
        try:
            output, err = self.uc.execute()
            if err:
                return {"status": 500, "data": {"error": str(err)}}

            return {"status": 200, "data": output}

        except Exception as e:
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}
