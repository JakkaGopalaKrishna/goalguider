fetch(`${API_BASE}/roadmap/`, {
  headers: {
    "Authorization": "Bearer " + localStorage.getItem("token")
  }
})
.then(res => res.json())
.then(data => {
  const world = document.getElementById('world');
  const pole = document.getElementById('pole');
  const scrollSpacer = document.getElementById('scroll-spacer');

  if (!data.steps || data.steps.length === 0) {
    showToast("No roadmap yet. Complete onboarding.", "error");
    return;
  }

  const stepsData = data.steps;
  const stepGapY = 600; // Vertical distance between steps
  const stepElements = [];

  // 1. Set dynamic scroll height
  // const totalHeight = (stepsData.length + 1) * 100; 
  // scrollSpacer.style.height = totalHeight + "vh";
  const totalHeight = (stepsData.length * 100) + 100; 
  scrollSpacer.style.height = totalHeight + "vh";

  // 2. Set dynamic pole height
  // const poleHeight = (stepsData.length * stepGapY) + 3000;
  // pole.style.height = poleHeight + "px";
  // pole.style.top = -(poleHeight / 2) + "px";
  const totalStepSpan = stepsData.length * stepGapY;
  const poleHeight = totalStepSpan + 5000; // Large buffer
  pole.style.height = poleHeight + "px";
  pole.style.top = `-${2500}px`;

  // 3. Build pole faces
  pole.innerHTML = ''; // Clear template
  for (let i = 0; i < 6; i++) {
    const face = document.createElement('div');
    face.className = 'pole-face';
    face.style.transform = `rotateY(${i * 60}deg) translateZ(calc(var(--pole-dim)/2))`;
    pole.appendChild(face);
  }

  // 4. Build steps
  stepsData.forEach((step, i) => {
    const y = i * stepGapY;
    const r = i * 90; // Rotation spiral

    // Create Arm
    const arm = document.createElement('div');
    arm.className = 'connector-arm';
    arm.style.transform = `translateY(${y}px) rotateY(${r}deg) translateX(calc(var(--pole-dim)/2))`;
    world.appendChild(arm);

    // Create Card
    const el = document.createElement('div');
    el.className = 'step';
    el.style.setProperty('--y', `${y}px`);
    el.style.setProperty('--r', `${r}deg`);
    el.style.transform = `translateY(${y}px) rotateY(${r}deg) translateX(calc(var(--arm-len) + (var(--pole-dim)/2)))`;

    el.innerHTML = `
      <h2>Step ${step.step_number}: ${step.title}</h2>
      <p>${step.description}</p>
    `;

    // Click to scroll to this step
    el.addEventListener('click', () => {
      const scrollTarget = (i / (stepsData.length - 1)) * (document.documentElement.scrollHeight - window.innerHeight);
      window.scrollTo({ top: scrollTarget, behavior: 'smooth' });
    });

    world.appendChild(el);
    stepElements.push({ el, arm });
  });

function onScroll() {
  // Calculate scroll based ONLY on the spacer, not the whole document
  const spacerRect = scrollSpacer.getBoundingClientRect();
  const spacerHeight = scrollSpacer.offsetHeight;
  
  // How far we have scrolled relative to the top of the spacer
  const relativeScroll = window.scrollY;
  const maxScroll = spacerHeight - window.innerHeight;
  
  // Clamp the percentage between 0 and 1
  const scrollPercent = Math.max(0, Math.min(1, relativeScroll / maxScroll));

  const rotation = -scrollPercent * (stepsData.length - 1) * 90;
  const elevation = -scrollPercent * (stepsData.length - 1) * stepGapY;

  // Apply transformation to world
  world.style.transform = `rotateY(${rotation}deg) translateY(${elevation}px)`;

  // Toggle active classes
  const activeIndex = Math.round(scrollPercent * (stepsData.length - 1));
  stepElements.forEach((item, idx) => {
    const isActive = idx === activeIndex;
    item.el.classList.toggle('active', isActive);
    item.arm.classList.toggle('active', isActive);
  });
}
  window.addEventListener('scroll', onScroll);
  onScroll(); // Initial call

  showToast("3D Roadmap Loaded 🚀", "success");
})
.catch(err => {
  console.error(err);
  showToast("Failed to load roadmap", "error");
});