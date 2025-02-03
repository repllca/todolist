import React, { useState, useEffect } from 'react';
import TaskList from "../component/TaskList"
export const TodoPages = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // タスクをデータベースから取得するためのAPI呼び出し（仮）
    const fetchTasks = async () => {
      const response = await fetch('/api/tasks'); // APIからタスクを取得する
      const data = await response.json();
      setTasks(data.tasks); // 取得したタスクデータをstateに保存
    };

    fetchTasks(); // コンポーネントのマウント時にタスクを取得
  }, []); // 空の依存配列なので最初の一回のみ呼ばれる

  return (
    <div>
      <h1>タスク一覧</h1>
      <TaskList tasks={tasks} /> {/* TaskListにタスクデータを渡す */}
    </div>
  );
};


