from fastapi.responses import JSONResponse


def throw_custom_exception(status_code: int, content: dict):
    return JSONResponse(status_code=status_code, content=content)
