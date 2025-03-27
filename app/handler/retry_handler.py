# app/services/chat/retry_handler.py

from functools import wraps
from typing import Callable, TypeVar

from app.config.config import settings
from app.log.logger import get_retry_logger

T = TypeVar("T")
logger = get_retry_logger()


class RetryHandler:
    """重试处理装饰器"""

    def __init__(self, max_retries: int = 1, key_arg: str = "api_key", model_arg: str = "model"):
        self.max_retries = max_retries
        self.key_arg = key_arg
        self.model_arg = model_arg

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None

            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"API call failed with error: {str(e)}. Trying SECOND_MODEL...")
                
                # Immediately switch to SECOND_MODEL on first failure
                if self.model_arg in kwargs and hasattr(settings, 'SECOND_MODEL'):
                    kwargs[self.model_arg] = settings.SECOND_MODEL
                    logger.info(f"Switching to {settings.SECOND_MODEL} model for retry")
                    
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        logger.error(f"SECOND_MODEL retry also failed with error: {str(e)}")

            logger.error(
                f"All retry attempts failed, raising final exception: {str(last_exception)}"
            )
            # Return error message instead of raising exception
            return {"error": "API call failed after retries", "details": str(last_exception)}

        return wrapper
