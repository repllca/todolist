from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
app = FastAPI()
router = APIRouter()
# PostgreSQL 接続設定
def get_db_connection():
    return psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

# タスク作成用のリクエストモデル
class TaskCreate(BaseModel):
    name: str
    points: int
    room_id: int
    creator_id: int

# タスク更新用のリクエストモデル
class TaskUpdate(BaseModel):
    completed: bool

# タスク情報の取得用レスポンスモデル
class Task(BaseModel):
    id: int
    name: str
    points: int
    creator_id: int
    assignee_id: int
    room_id: int
    completed: bool

@app.post("/api/tasks", response_model=Task)
def create_task(task: TaskCreate):
    """タスク作成 API"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            sql.SQL("INSERT INTO tasks (name, points, creator_id, room_id) VALUES (%s, %s, %s, %s) RETURNING id, name, points, creator_id, room_id, completed"),
            [task.name, task.points, task.creator_id, task.room_id]
        )
        conn.commit()
        task_data = cursor.fetchone()
        return Task(
            id=task_data[0],
            name=task_data[1],
            points=task_data[2],
            creator_id=task_data[3],
            assignee_id=None,  # Assignee is not set yet
            room_id=task_data[4],
            completed=task_data[5]
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="タスク作成に失敗しました")
    finally:
        cursor.close()
        conn.close()

@app.patch("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """タスクの完了状態を更新する API"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            sql.SQL("UPDATE tasks SET completed = %s WHERE id = %s RETURNING id, name, points, creator_id, assignee_id, room_id, completed"),
            [task_update.completed, task_id]
        )
        conn.commit()
        task_data = cursor.fetchone()
        if not task_data:
            raise HTTPException(status_code=404, detail="タスクが見つかりません")
        return Task(
            id=task_data[0],
            name=task_data[1],
            points=task_data[2],
            creator_id=task_data[3],
            assignee_id=task_data[4],
            room_id=task_data[5],
            completed=task_data[6]
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="タスク更新に失敗しました")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/tasks/{room_id}", response_model=List[Task])
def get_tasks(room_id: int):
    """指定されたルームのタスク一覧を取得する API"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            sql.SQL("SELECT id, name, points, creator_id, assignee_id, room_id, completed FROM tasks WHERE room_id = %s"),
            [room_id]
        )
        tasks_data = cursor.fetchall()
        tasks = [
            Task(
                id=task_data[0],
                name=task_data[1],
                points=task_data[2],
                creator_id=task_data[3],
                assignee_id=task_data[4],
                room_id=task_data[5],
                completed=task_data[6]
            )
            for task_data in tasks_data
        ]
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail="タスク取得に失敗しました")
    finally:
        cursor.close()
        conn.close()
