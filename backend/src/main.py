import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI, Request,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
from api.schemas.response import ResponseModel
from api.router import (
    agent_router,
    user_router,
    auth_router
)
load_dotenv()
app = FastAPI(description='特色风格智能体接口')
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(agent_router, prefix="/api", tags=["agent"])
app.include_router(user_router, prefix="/api", tags=["user"])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 Tortoise ORM
register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),
    modules={"models": ["api.models"]},
    generate_schemas=False,
    add_exception_handlers=True
)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    拦截 HTTPException，将返回值统一封装为 ResponseModel
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(code=exc.status_code, msg=exc.detail).dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    参数校验失败也统一封装
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseModel(code=status.HTTP_422_UNPROCESSABLE_ENTITY, msg=str(exc)).dict()
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
