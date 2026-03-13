function requireAuth() {
  const token = localStorage.getItem("token");

  // 🚫 DO NOT GUARD PUBLIC PAGES
  const publicPages = ["login.html", "signup.html", "index.html"];
  const currentPage = window.location.pathname.split("/").pop();

  if (publicPages.includes(currentPage)) return;

  if (!token) {
    window.location.replace("login.html");
  }
}
