import React, { useState } from "react";

interface RoomCreateRequest {
  name: string;
  user_name: string;
}

interface TaskCreateRequest {
  name: string;
  points: number;
  creator_id: number;
  assignee_id: number;
  room_id: number;
}

export const RoomNameInput = () => {
  const [roomName, setRoomName] = useState<string>("");
  const [userName, setUserName] = useState<string>("");
  const [taskName, setTaskName] = useState<string>("");
  const [points, setPoints] = useState<number>(0);
  const [creatorId, setCreatorId] = useState<number>(1); // 例: 最初のユーザーID
  const [assigneeId, setAssigneeId] = useState<number>(2); // 例: 次のユーザーID
  const [roomId, setRoomId] = useState<number>(0);

  const handleJoinRoom = async () => {
    if (!roomName || !userName) {
      alert("ルーム名とユーザー名を入力してください");
      return;
    }

    const requestData: RoomCreateRequest = {
      name: roomName,
      user_name: userName,
    };

    try {
      const response = await fetch("http://localhost:8000/api/rooms", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const error = await response.json();
        alert(`エラー: ${error.detail}`);
        return;
      }

      const data = await response.json();
      console.log("ルームに入室しました:", data);
      setRoomId(data.id); // ルームIDを保存
    } catch (error) {
      console.error("リクエスト失敗:", error);
      alert("入室に失敗しました");
    }
  };

  const handleCreateTask = async () => {
    if (!taskName || points <= 0) {
      alert("タスク名とポイントを入力してください");
      return;
    }

    const taskData: TaskCreateRequest = {
      name: taskName,
      points,
      creator_id: creatorId,
      assignee_id: assigneeId,
      room_id: roomId,
    };

    try {
      const response = await fetch("/api/tasks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const error = await response.json();
        alert(`エラー: ${error.detail}`);
        return;
      }

      const data = await response.json();
      console.log("タスクが作成されました:", data);
    } catch (error) {
      console.error("リクエスト失敗:", error);
      alert("タスク作成に失敗しました");
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="ルーム名を入力してください"
        value={roomName}
        onChange={(e) => setRoomName(e.target.value)}
      />
      <input
        type="text"
        placeholder="ユーザー名を入力してください"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      <button onClick={handleJoinRoom}>入室</button>

      <hr />

      <input
        type="text"
        placeholder="タスク名を入力してください"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
      />
      <input
        type="number"
        placeholder="ポイント"
        value={points}
        onChange={(e) => setPoints(Number(e.target.value))}
      />
      <button onClick={handleCreateTask}>タスク作成</button>
    </div>
  );
};


