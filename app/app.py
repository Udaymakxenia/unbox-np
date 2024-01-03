from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from app.activities.activity_file_route import router as ActivityRouter
from app.ota.ota_route import router as OTARouter
from app.users.user_route import router as UserRouter

main = FastAPI()



main.include_router(ActivityRouter, tags=["Activities"], prefix="/api/activities")
main.include_router(OTARouter, tags=["OTA"], prefix="/api/ota")
main.include_router(UserRouter, tags=["Users"], prefix="/api/users")


@main.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    raise HTTPException(status_code=404, detail="not found")
    return "{}"

#def custom_openapi():
#    if main.openapi_schema:
#        return main.openapi_schema
#    openapi_schema = get_openapi(
#        title="Custom title",
#        version="2.5.0",
#        summary="This is a very custom OpenAPI schema",
#        description="Here's a longer description of the custom **OpenAPI** schema",
#        routes=main.routes,
#        scheme_name={OAuth2PasswordBearer(
#            tokenUrl="/api/users/login",
#            scheme_name="admin_oauth2_schema"
#        )}
#    )

#    openapi_schema["info"]["x-logo"] = {
#        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#    }
#    main.openapi_schema = openapi_schema
#    return main.openapi_schema