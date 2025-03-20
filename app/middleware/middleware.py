"""
中间件配置模块，负责设置和配置应用程序的中间件
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.logger.logger import get_main_logger
from app.core.security import verify_auth_token
# from app.middleware.request_logging_middleware import RequestLoggingMiddleware
from app.core.constants import API_VERSION

logger = get_main_logger()

class AuthMiddleware(BaseHTTPMiddleware):
    """
    认证中间件，处理未经身份验证的请求
    """
    async def dispatch(self, request: Request, call_next):
        # 允许特定路径绕过身份验证
        if (request.url.path not in ["/", "/auth"] and 
            not request.url.path.startswith("/static") and
            not request.url.path.startswith("/gemini") and
            not request.url.path.startswith("/v1") and
            not request.url.path.startswith(f"/{API_VERSION}") and
            not request.url.path.startswith("/health") and
            not request.url.path.startswith("/hf")):
            
            auth_token = request.cookies.get("auth_token")
            if not auth_token or not verify_auth_token(auth_token):
                logger.warning(f"Unauthorized access attempt to {request.url.path}")
                return RedirectResponse(url="/")
            logger.debug("Request authenticated successfully")
            
        response = await call_next(request)
        return response

def setup_middlewares(app: FastAPI) -> None:
    """
    设置应用程序的中间件
    
    Args:
        app: FastAPI应用程序实例
    """
    # 添加认证中间件
    app.add_middleware(AuthMiddleware)
    
    # 添加请求日志中间件（可选，默认注释掉）
    # app.add_middleware(RequestLoggingMiddleware)
    
    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境建议配置具体的域名
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 明确指定允许的HTTP方法
        allow_headers=["*"],  # 生产环境建议配置具体的请求头
        expose_headers=["*"],  # 允许前端访问的响应头
        max_age=600,  # 预检请求缓存时间(秒)
    )
