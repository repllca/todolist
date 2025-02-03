import React from 'react';

interface Task {
  id: number;
  name: string;
  points: number;
  completed: boolean;
}

interface TaskListProps {
  tasks: Task[];
}

const TaskList: React.FC<TaskListProps> = ({ tasks }) => {
  return (
    <div>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {task.name} - {task.points}ポイント
            <input placeholder='完了' type="checkbox" checked={task.completed} /> {/* チェックボックス */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;