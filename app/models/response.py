from pydantic import BaseModel, Field

   
    
def ResponseModel(data , message):
    return{
        "data":data,
        "code":200,
        "message": message
    }
    
def ErrorResponseModel(error, code):
    return {"error": error, "code": code}
