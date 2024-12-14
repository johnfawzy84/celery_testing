from fastapi import FastAPI, BackgroundTasks
from uuid import UUID
from tasks import add, subtract, chain

app = FastAPI()

@app.post("/tasks/add")
async def add_task(x: int, y: int, background_tasks: BackgroundTasks):
    task = add.apply_async(args=[x, y])
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}

@app.post("/tasks/subtract")
async def subtract_task(x: int, y: int, background_tasks: BackgroundTasks):
    task = subtract.apply_async(args=[x, y])
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}

@app.post("/tasks/chain")
async def chain_task(tasks: list, background_tasks: BackgroundTasks):
    task_chain = chain(*tasks)
    task = task_chain.apply_async()
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}

@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: UUID):
    task = add.AsyncResult(str(task_id))
    return {"task_id": task.id, "status": task.status}

@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: UUID):
    task = add.AsyncResult(str(task_id))
    if task.status == "SUCCESS":
        return {"task_id": task.id, "result": task.result}
    return {"task_id": task.id, "status": task.status}
