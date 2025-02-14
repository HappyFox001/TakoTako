from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import generate_smart_comment
import uvicorn

app = FastAPI(
    title="TakoTako评论API", description="一个能生成犀利评论的API服务", version="1.0.0"
)


class CommentRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    thinking_process: str
    final_comment: str


@app.post("/comment", response_model=CommentResponse)
async def create_comment(request: CommentRequest):
    if not request.content:
        raise HTTPException(status_code=400, detail="内容不能为空")

    result = generate_smart_comment(request.content)

    if "error" in result:
        raise HTTPException(status_code=500, detail=str(result["error"]))

    return CommentResponse(
        thinking_process=result["thinking_process"],
        final_comment=result["final_comment"],
    )


@app.get("/")
async def root():
    return {"message": "欢迎使用TakoTako评论API！"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
