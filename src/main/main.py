import traceback
from fastapi import Body, FastAPI
from main.configuration import Context
from main.model.llama_models import InfillRequest, InfillResponse

app = FastAPI(title="Infill API")
logger = Context.get_logger()


@app.post("/infill")
def infill(body: InfillRequest = Body(...)):
    """
    This function is used to generate a completion for a given prompt.
    """
    service = Context.get_infill_service()
    result = service.process(body)
    if result.is_error():
        logger.error(''.join(traceback.format_tb(result.get_error().__traceback__)))
        return InfillResponse(content="")
    logger.info(f"Generated completion: \"{result.get_value()}\"")
    return InfillResponse(content=result.get_value())
