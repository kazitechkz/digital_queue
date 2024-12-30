from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


async def validation_exception_handler(request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])  # Пропускаем "body"
        if field not in errors:
            errors[field] = []
        errors[field].append(error["msg"])
    return JSONResponse(
        status_code=422,
        content={"errors": errors},
    )
