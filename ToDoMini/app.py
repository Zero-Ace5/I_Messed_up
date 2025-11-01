from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="To-Do App but Smol")

todos = []


class Todo(BaseModel):
    id: int
    task: str
    done: bool = False
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.get("/")
def home():
    return {"message": "This probably the simplest route but it's HOME. Use /todos"}


@app.get("/todos")
def all_tasks():
    return {"count": len(todos), "data": todos}


@app.post("/todos")
def create_task(todo: Todo):
    for t in todos:
        if todo.id == t.id:
            raise HTTPException(
                status_code=400, detail="Duplicate ID for Task")
    todos.append(todo)
    return {"message": "Added", "todo": todo}


@app.put("/todos/{todo_id}")
def task_done(todo_id: int):
    for t in todos:
        if t.id == todo_id:
            t.done = True
            return {"message": f"Todo {todo_id} marked as completed", "todo": t}
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete(todo_id: int):
    for t in todos:
        if t.id == todo_id:
            todos.remove(t)
            return {"message": f"{todo_id} removed"}
    raise HTTPException(status_code=404, detail="Todo not found")

# Accessible at http://127.0.0.1:8000/docs
# Run via uvicorn app:app --reload
