"""API Routes Module"""
from api.routes.job_routes import router as job_router
from api.routes.agent_routes import router as agent_router

__all__ = ["job_router", "agent_router"]

