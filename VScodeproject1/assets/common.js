// Shared helpers: escaping, tooltip, theme toggle.
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
const pct = (v, d = 1) => (v * 100).toFixed(d) + "%";
const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

const tip = document.createElement("div");
tip.id = "tip"; tip.setAttribute("role", "tooltip");
document.body.appendChild(tip);
function showTip(e, html) {
  tip.innerHTML = html; tip.style.opacity = 1;
  const pad = 14, r = tip.getBoundingClientRect();
  let x = e.clientX + pad, y = e.clientY + pad;
  if (x + r.width > innerWidth - 8) x = e.clientX - r.width - pad;
  if (y + r.height > innerHeight - 8) y = e.clientY - r.height - pad;
  tip.style.left = x + "px"; tip.style.top = y + "px";
}
function hideTip() { tip.style.opacity = 0; }
function bindTip(el, html) {
  el.addEventListener("pointermove", e => showTip(e, html));
  el.addEventListener("pointerleave", hideTip);
}

// Theme toggle (remembers choice per browser; works without storage too)
const themeListeners = [];
(function () {
  let saved = null;
  try { saved = localStorage.getItem("theme"); } catch (_) {}
  if (saved) document.documentElement.dataset.theme = saved;
  const btn = $("theme-btn");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const cur = document.documentElement.dataset.theme ||
      (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const next = cur === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (_) {}
    themeListeners.forEach(f => f());
  });
})();

function setStatus(ok, text) {
  const el = $("status");
  if (!el) return;
  el.classList.toggle("err", !ok);
  el.lastChild.textContent = text;
}
