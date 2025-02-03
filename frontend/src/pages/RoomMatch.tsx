import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

interface RoomCreateRequest {
  name: string;
  user_name: string;
}

export const RoomNameInput = () => {
  const [roomName, setRoomName] = useState<string>("");
  const [userName, setUserName] = useState<string>("");
  const navigate = useNavigate();

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
      
      // 入室後、/todoページに遷移
      navigate("/todo");
    } catch (error) {
      console.error("リクエスト失敗:", error);
      alert("入室に失敗しました");
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
    </div>
  );
};



