import React, { useState } from "react";

const TaskForm = ({ task = {}, onSubmit }) => {
  const [name, setName] = useState(task.name || "");
  const [description, setDescription] = useState(task.description || "");
  const [dueDate, setDueDate] = useState(task.due_date || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, description, dueDate });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Task Name</label>
        <input value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div>
        <label>Description</label>
        <input value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div>
        <label>Due Date</label>
        <input type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default TaskForm;
