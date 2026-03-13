function login() {
  const loginBtn = document.querySelector('button');
  const username = document.getElementById("username");
  const password = document.getElementById("password");

  // Validate form
  const isValid = validateForm([
    { id: "username", validation: (val) => validateUsername(val), errorMsg: "Username must be 3+ characters" },
    { id: "password", validation: (val) => val.length > 0, errorMsg: "Password is required" }
  ]);

  if (!isValid) return;

  setButtonLoading(loginBtn, true);

  fetch(`${API_BASE}/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
      username: username.value.trim(), 
      password: password.value 
    })
  })
  .then(res => {
    if (!res.ok) {
      return res.json().then(err => {
        throw new Error(err.detail || "Login failed");
      });
    }
    return res.json();
  })
  .then(data => {
    if (!data.access) {
      throw new Error("No token received");
    }
    localStorage.setItem("token", data.access);
    // localStorage.removeItem("signup-to-login"); // removes the signup-to-login
    showToast("Login successful!", "success", 2000);
    
    setTimeout(() => {
      checkRoadmapAndRedirect();
    }, 500);
  })
  .catch(error => {
    setButtonLoading(loginBtn, false);
    showToast(error.message || "Login failed", "error");
  });
}


function checkRoadmapAndRedirect() {
  fetch(`${API_BASE}/roadmap/`, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.steps && data.steps.length > 0) {
      // roadmap exists
      window.location.href = "roadmap.html";
    } else {
      // no roadmap
      window.location.href = "onboarding.html";
    }
  })
  .catch(() => {
    // safety fallback
    window.location.href = "onboarding.html";
  });
}


