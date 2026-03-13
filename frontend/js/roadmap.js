// function generateRoadmap() {
//   console.log("generateRoadmap");
//   const statusInput = document.getElementById("status");
//   const goalInput = document.getElementById("goal");
//   const generateBtn = document.querySelector('button');


//   // Validate form
//   const isValid = validateForm([
//     { id: "status", validation: (val) => val.length > 5, errorMsg: "Please provide your current status (min 5 characters)" },
//     { id: "goal", validation: (val) => val.length > 5, errorMsg: "Please describe your career goal (min 5 characters)" }
//   ]);

//   if (!isValid) return;

//   setButtonLoading(generateBtn, true);

//   fetch(`${API_BASE}/roadmap/generate/`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "Authorization": "Bearer " + localStorage.getItem("token")
//     },
//     body: JSON.stringify({ 
//       current_status: statusInput.value.trim(), 
//       career_goal: goalInput.value.trim() 
//     })
//   })
//   .then(res => {
//     if (!res.ok) {
//       return res.json().then(err => {
//         throw new Error(err.detail || "Failed to generate roadmap");
//       });
//     }
//     showToast("🎉 Roadmap generated! Redirecting...", "success");
//     return res.json();
//   })
//   .then(() => {
//     window.location.href = "roadmap.html";
//   })
//   .catch(error => {
//     localStorage.setItem("roadmap generater err", error);
//     setButtonLoading(generateBtn, false);
//     showToast(error.message || "Failed to generate roadmap", "error");
//   });
// }
// -------------------------------------
async function generateRoadmap() {
  console.log("generateRoadmap");

  const statusInput = document.getElementById("status");
  const goalInput = document.getElementById("goal");
  const generateBtn = document.querySelector("button");

  // Validate form
  const isValid = validateForm([
    {
      id: "status",
      validation: (val) => val.length > 5,
      errorMsg: "Please provide your current status (min 5 characters)"
    },
    {
      id: "goal",
      validation: (val) => val.length > 5,
      errorMsg: "Please describe your career goal (min 5 characters)"
    }
  ]);

  if (!isValid) return;

  try {
    setButtonLoading(generateBtn, true);

    const response = await fetch(`${API_BASE}/roadmap/generate/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({
        current_status: statusInput.value.trim(),
        career_goal: goalInput.value.trim()
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Failed to generate roadmap");
    }

    await response.json();

    showToast("🎉 Roadmap generated! Redirecting...", "success");

    window.location.href = "roadmap.html";

  } catch (error) {
    console.error(error);
    localStorage.setItem("roadmap generator err", error.message);
    showToast(error.message || "Failed to generate roadmap", "error");
  } finally {
    setButtonLoading(generateBtn, false);
  }
}
