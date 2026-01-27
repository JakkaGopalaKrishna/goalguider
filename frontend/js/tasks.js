function loadTasks() {
  const container = document.getElementById("tasks");
  container.innerHTML = '<p style="text-align: center; color: #999;">Loading tasks...</p>';

  fetch(`${API_BASE}/tasks/`, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  })
  .then(res => res.json())
  .then(tasks => {
    const container = document.getElementById("tasks");
    container.innerHTML = "";

    if (tasks.length === 0) {
      container.innerHTML = '<p style="text-align: center; color: #999;">No tasks yet. Generate a roadmap first!</p>';
      return;
    }

    tasks.forEach((task, index) => {
      const taskDiv = document.createElement("div");
      taskDiv.className = `task ${task.is_completed ? 'completed' : ''}`;
      
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = task.is_completed;
      checkbox.disabled = task.is_completed;
      checkbox.onchange = () => completeTask(task.id, checkbox);
      
      const contentDiv = document.createElement("div");
      contentDiv.className = "task-content";
      contentDiv.innerHTML = `<span class="task-title">${task.title}</span>`;
      
      taskDiv.appendChild(checkbox);
      taskDiv.appendChild(contentDiv);
      
      container.appendChild(taskDiv);
    });

    showToast(`${tasks.filter(t => t.is_completed).length} tasks completed today!`, "success", 2000);
  })
  .catch(error => {
    showToast("Failed to load tasks", "error");
  });
}

function completeTask(taskId, checkbox) {
  checkbox.disabled = true;
  
  fetch(`${API_BASE}/tasks/complete/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({ task_id: taskId })
  })
  .then(res => res.json())
  .then(() => {
    checkbox.checked = true;
    loadTasks();
    loadStreak();
    showToast("Great job! Task completed! 🎉", "success", 2000);
  })
  .catch(error => {
    checkbox.disabled = false;
    checkbox.checked = false;
    showToast("Failed to complete task", "error");
  });
}

function loadStreak() {
  fetch(`${API_BASE}/tasks/streak/`, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  })
  .then(res => res.json())
  .then(data => {
    const streakEl = document.getElementById("streak");
    streakEl.innerHTML = `
      <span class="streak-icon">🔥</span>
      <span>Current Streak: <strong>${data.current_streak}</strong> days</span>
      <span style="margin-left: 20px;">🏆 Best: <strong>${data.best_streak}</strong></span>
    `;
  });
}

// Load initial data
loadTasks();
loadStreak();

// Refresh every 30 seconds
setInterval(loadTasks, 30000);
