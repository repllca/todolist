import './App.css';
import { RoomNameInput } from './pages/RoomMatch';
import { TodoPages } from './pages/TodoPages';
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<RoomNameInput />} />
        <Route path="/todo" element={<TodoPages />} />
      </Routes>
    </>
  );
}

export default App;

