// Plays the step-by-step build of animated SVG figures (img.anim-fig) like a slide build:
// once when a figure first scrolls into view, and again whenever the reader presses Replay.
// Each build is CSS inside the SVG, so cloning the <img> starts it from the first step.
// Readers who ask for reduced motion see the finished figure and no button (see figure-build.css).
(function () {
  function restart(img) {
    var fresh = img.cloneNode(true);
    img.replaceWith(fresh);
    return fresh;
  }
  function setup(img) {
    if (img.dataset.buildReady) return;
    img.dataset.buildReady = "1";
    var current = img;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "anim-replay";
    btn.textContent = "↻ Replay build";
    btn.setAttribute("aria-label", "Replay the step-by-step build of this figure");
    btn.addEventListener("click", function (ev) {
      ev.preventDefault(); ev.stopPropagation();
      current = restart(current);
    });
    // Sphinx wraps a sized image in a link to the file, so the button goes after the link.
    (current.closest("a") || current).insertAdjacentElement("afterend", btn);
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { io.disconnect(); current = restart(current); }
        });
      }, { threshold: 0.35 });
      io.observe(current);
    }
  }
  function init() { document.querySelectorAll("img.anim-fig").forEach(setup); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
