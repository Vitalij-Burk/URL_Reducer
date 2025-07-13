import uvicorn
from api.routes.auth import auth_router
from api.routes.link import link_router
from api.routes.redirect import redirect_router
from api.routes.user import user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(link_router, prefix="/link", tags=["Link"])
app.include_router(redirect_router, tags=["Redirect"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
