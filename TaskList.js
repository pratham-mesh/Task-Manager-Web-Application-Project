import React, { useEffect, useState } from "react";

const TaskList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/tasks")
      .then((response) => response.json())
      .then((data) => setTasks(data));
  }, []);

  const deleteTask = (id) => {
    fetch(`http://localhost:8000/tasks/${id}`, {
      method: "DELETE",
    }).then(() => setTasks(tasks.filter((task) => task.id !== id)));
  };

  return (
    <div>
      <h1>Task List</h1>
      {tasks.map((task) => (
        <div key={task.id}>
          <h2>{task.name}</h2>
          <p>{task.description}</p>
          <button onClick={() => deleteTask(task.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
