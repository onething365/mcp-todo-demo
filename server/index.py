from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI()

# 模拟数据库存储
todos = []

# 数据模型
class TodoItem(BaseModel):
    name: str
    priority: str

class TodoItemResponse(TodoItem):
    id: str
    created_time: str

class TodoListResponse(BaseModel):
    code: int = 1000
    data: List[TodoItemResponse]
    msg: str = ""

class AddTodoResponse(BaseModel):
    code: int = 1000
    data: TodoItemResponse
    msg: str = ""

# 获取待办列表
@app.get("/todo/list", response_model=TodoListResponse)
async def get_todo_list(length: int = 5):
    # 按创建时间降序排序并获取前length条
    sorted_todos = sorted(todos, key=lambda x: x["created_time"], reverse=True)
    result = sorted_todos[:length]
    
    return {
        "code": 1000,
        "data": result,
        "msg": ""
    }

# 新增待办
@app.post("/todo/add", response_model=AddTodoResponse)
async def add_todo(todo: TodoItem):
    new_todo = {
        "id": str(uuid.uuid4()),
        "name": todo.name,
        "priority": todo.priority,
        "created_time": datetime.now().isoformat()
    }
    todos.append(new_todo)
    
    return {
        "code": 1000,
        "data": new_todo,
        "msg": ""
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001,reload=True)