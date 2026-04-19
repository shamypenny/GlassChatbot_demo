from .chat import router as chat_router
from .recipe import router as recipe_router
from .recommend import router as recommend_router

__all__ = ["chat_router", "recipe_router", "recommend_router"]
