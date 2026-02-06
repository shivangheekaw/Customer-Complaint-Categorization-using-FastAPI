from fastapi import FastAPI, Query
from chatbot import chatbot_logic

app = FastAPI()


@app.get("/predict")
def predict(
    complaint_text: str = Query(
        ...,
        description="User complaint text"
    )
):
    category = chatbot_logic(complaint_text)

    return {
        "complaint_text": complaint_text,
        "predicted_category": category
    }
