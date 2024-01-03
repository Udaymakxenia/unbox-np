import uvicorn
import pydantic

if __name__ == "__main__":
    uvicorn.run("app.app:main", host="0.0.0.0", port=80, reload=True)
    