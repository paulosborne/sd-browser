from fastapi import APIRouter

from app.api.v1.endpoints import auth, sd, guide, search, favourites, rules, notifications, calendar, exports, admin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(sd.router, prefix="/sd", tags=["Schedules Direct"])
api_router.include_router(guide.router, prefix="/guide", tags=["Guide"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(favourites.router, prefix="/favourites", tags=["Favourites"])
api_router.include_router(rules.router, prefix="/rules", tags=["Rules"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(exports.router, prefix="/exports", tags=["Exports"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])