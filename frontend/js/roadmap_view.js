fetch(`${API_BASE}/roadmap/`, {
  headers: {
    "Authorization": "Bearer " + localStorage.getItem("token")
  }
})
.then(res => res.json())
.then(data => {
  const container = document.getElementById("roadmap");

  if (!data.steps || data.steps.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: #999;">No roadmap yet. Go to onboarding to create one!</p>';
    return;
  }

  data.steps.forEach(step => {
    const div = document.createElement("div");
    div.className = "card";
    div.style.cursor = "pointer";
    
    const isExpanded = localStorage.getItem(`roadmap-step-${step.step_number}`) === 'true';
    
    const header = document.createElement("div");
    header.style.display = "flex";
    header.style.justifyContent = "space-between";
    header.style.alignItems = "center";
    
    header.innerHTML = `
      <div>
        <h3 style="margin: 0;">Step ${step.step_number}: ${step.title}</h3>
        <small style="color: #999;">${step.duration}</small>
      </div>
      <span style="font-size: 20px; transition: transform 0.3s;" class="expand-icon">▼</span>
    `;
    
    const descDiv = document.createElement("div");
    descDiv.className = "step-description";
    descDiv.innerHTML = `<p style="margin-top: 15px; line-height: 1.6; color: #555;">${step.description}</p>`;
    descDiv.style.maxHeight = isExpanded ? "500px" : "0";
    descDiv.style.overflow = "hidden";
    descDiv.style.transition = "max-height 0.3s ease";
    
    div.appendChild(header);
    div.appendChild(descDiv);
    
    header.style.cursor = "pointer";
    header.onclick = () => {
      const isOpen = descDiv.style.maxHeight !== "0px";
      descDiv.style.maxHeight = isOpen ? "0" : "500px";
      header.querySelector(".expand-icon").style.transform = isOpen ? "rotate(0deg)" : "rotate(180deg)";
      localStorage.setItem(`roadmap-step-${step.step_number}`, !isOpen);
    };
    
    container.appendChild(div);
  });

  showToast("Roadmap loaded! Click steps to expand", "success", 2000);
})
.catch(error => {
  showToast("Failed to load roadmap", "error");
});
