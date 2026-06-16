from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify

app = FastAPI(title="EU AI Act Compliance Checker")

class UseCase(BaseModel):
    use_case: str

@app.post("/check")
def check_use_case(payload: UseCase):
    return classify(payload.use_case)