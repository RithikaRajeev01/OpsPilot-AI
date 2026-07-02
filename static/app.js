// ==========================================================
// OpsPilot AI — Dashboard interactions
// ==========================================================

// ---- Tab switching ----
document.addEventListener("DOMContentLoaded", function () {
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");

  tabButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const target = btn.getAttribute("data-tab");

      tabButtons.forEach((b) => b.classList.remove("active"));
      tabPanels.forEach((p) => p.classList.remove("active"));

      btn.classList.add("active");
      const panel = document.getElementById(target);
      if (panel) panel.classList.add("active");
    });
  });

  // ---- KPI reveal animation ----
  document.querySelectorAll(".kpi-card h3").forEach(function (el, i) {
    el.style.opacity = "0";
    el.style.transform = "translateY(16px)";
    setTimeout(function () {
      el.style.transition = "opacity .5s ease, transform .5s ease";
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, 150 + i * 90);
  });

  // ---- Auto-tag risk badges inside the shipments table ----
  // Looks for cells whose text matches a risk level and wraps them
  // in a styled badge, so the backend can keep emitting plain text.
  const riskWords = {
    critical: "critical",
    high: "high",
    medium: "medium",
    low: "low",
  };
  document.querySelectorAll(".table-wrap td").forEach(function (td) {
    const text = td.textContent.trim().toLowerCase();
    if (riskWords[text]) {
      td.innerHTML =
        '<span class="risk-badge ' + riskWords[text] + '">' + text + "</span>";
    }
  });

  // ---- Sidebar active state ----
  const menuLinks = document.querySelectorAll(".menu a");
  menuLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (link.getAttribute("href") === "#") e.preventDefault();
      menuLinks.forEach((l) => l.classList.remove("active"));
      link.classList.add("active");
    });
  });

  // ---- Mobile sidebar toggle (if a .menu-toggle button exists) ----
  const menuToggle = document.querySelector(".menu-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });
  }
});

// ======================================================
// Sidebar -> Open corresponding tab
// ======================================================

document.querySelectorAll(".menu a").forEach(link => {

    link.addEventListener("click", function () {

        const href = this.getAttribute("href");

        if (!href.startsWith("#tab-")) return;

        const tabId = href.substring(1);

        // remove active from buttons
        document.querySelectorAll(".tab-btn").forEach(btn => {
            btn.classList.remove("active");
        });

        // remove active from panels
        document.querySelectorAll(".tab-panel").forEach(panel => {
            panel.classList.remove("active");
        });

        // activate correct button
        const btn = document.querySelector(`[data-tab="${tabId}"]`);
        if (btn) btn.classList.add("active");

        // activate correct panel
        const panel = document.getElementById(tabId);
        if (panel) {
            panel.classList.add("active");

            panel.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
    });

});