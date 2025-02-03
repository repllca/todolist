from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
from typing import Set
from fastapi.middleware.cors import CORSMiddleware
from tasks import router as tasks_router

app = FastAPI()

# tasks.pyで定義したルータを登録
app.include_router(tasks_router)
# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（開発中はこれでOK、公開時は適切なオリジンを設定）
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# PostgreSQL 接続設定
def get_db_connection():
    """データベース接続を取得する関数"""
    return psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

# ルームの管理（メモリ上）
rooms: dict[str, Set[WebSocket]] = {}

# ルーム作成用のリクエストモデル
class RoomCreate(BaseModel):
    name: str
    user_name: str

# タスク作成用のリクエストモデル
class TaskCreate(BaseModel):
    name: str
    points: int
    creator_id: int
    assignee_id: int
    room_id: int

@app.post("/api/rooms")
def create_room(room: RoomCreate):
    """ルーム作成 API"""
    if not room.name or not room.user_name:
        raise HTTPException(status_code=400, detail="ルーム名とユーザー名を入力してください")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ユーザーを登録
        cursor.execute(
            sql.SQL("INSERT INTO users (name) VALUES (%s) RETURNING id"),
            [room.user_name]
        )
        user_id = cursor.fetchone()[0]

        # ルームを作成
        cursor.execute(
            sql.SQL("INSERT INTO rooms (title) VALUES (%s) RETURNING id, title"),
            [room.name]
        )
        conn.commit()
        room_data = cursor.fetchone()
        return {"id": room_data[0], "name": room_data[1], "user_id": user_id}

    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="そのルーム名は既に存在します")
    finally:
        cursor.close()
        conn.close()

@app.post("/api/tasks")
def create_task(task: TaskCreate):
    """タスク作成 API"""
    if not task.name or not task.creator_id or not task.room_id:
        raise HTTPException(status_code=400, detail="タスク名、作成者ID、ルームIDを入力してください")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            sql.SQL("""
                INSERT INTO tasks (name, points, creator_id, assignee_id, room_id) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING id, name, points, creator_id, assignee_id, room_id
            """),
            [task.name, task.points, task.creator_id, task.assignee_id, task.room_id]
        )
        conn.commit()
        task_data = cursor.fetchone()
        return {
            "id": task_data[0], 
            "name": task_data[1], 
            "points": task_data[2],
            "creator_id": task_data[3],
            "assignee_id": task_data[4],
            "room_id": task_data[5]
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"タスク作成に失敗しました: {e}")
    finally:
        cursor.close()
        conn.close()

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    """WebSocket でリアルタイム通信"""
    await websocket.accept()

    # ルームが存在しなければ作成
    if room_name not in rooms:
        rooms[room_name] = set()

    rooms[room_name].add(websocket)
    print(f"WebSocket connected to room: {room_name}")

    try:
        while True:
            message = await websocket.receive_text()
            # ルーム内の全員にメッセージを送信
            for ws in rooms[room_name]:
                await ws.send_text(f"[{room_name}] {message}")
    except WebSocketDisconnect:
        # WebSocket接続が切断された場合の処理
        rooms[room_name].remove(websocket)
        if not rooms[room_name]:  # ルームが空なら削除
            del rooms[room_name]
        print(f"WebSocket disconnected from room: {room_name}")
    except Exception as e:
        print(f"Error in WebSocket communication: {e}")
        await websocket.send_text("An error occurred, please try again.")
    finally:
        await websocket.close()



