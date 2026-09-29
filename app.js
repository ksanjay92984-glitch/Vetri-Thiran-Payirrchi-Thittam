const tokenKey = "pocketsmart_token";

function token() { return localStorage.getItem(tokenKey); }
function authHeaders() {
  const t = token();
  return t ? {"Authorization": `Bearer ${t}`} : {};
}
function showMessage(el, text, cls="") {
  el.textContent = text;
  el.className = cls;
}

document.addEventListener("DOMContentLoaded", () => {
  const register = document.querySelector("#registerForm");
  if (register) register.addEventListener("submit", async e => {
    e.preventDefault();
    const f = new FormData(register);
    const payload = Object.fromEntries(f.entries());
    const res = await fetch("/api/register", {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem(tokenKey, data.access_token);
      location.href = "/planner";
    } else showMessage(document.querySelector("#message"), data.detail || "Registration failed", "error");
  });

  const login = document.querySelector("#loginForm");
  if (login) login.addEventListener("submit", async e => {
    e.preventDefault();
    const f = new FormData(login);
    const payload = Object.fromEntries(f.entries());
    const res = await fetch("/api/login", {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem(tokenKey, data.access_token);
      location.href = "/planner";
    } else showMessage(document.querySelector("#message"), data.detail || "Login failed", "error");
  });

  document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    document.querySelector("#"+btn.dataset.tab).classList.add("active");
  }));

  document.querySelectorAll(".plannerForm").forEach(form => form.addEventListener("submit", async e => {
    e.preventDefault();
    if (!token()) { location.href="/login"; return; }
    const isMultipart = form.enctype === "multipart/form-data";
    const body = isMultipart
      ? new FormData(form)
      : Object.fromEntries(new FormData(form).entries());
    if (!isMultipart) {
      if (body.budget) body.budget = Number(body.budget);
      if (body.guests) body.guests = Number(body.guests);
    }
    const result = document.querySelector("#result");
    result.innerHTML = "<p>Generating recommendations...</p>";
    const options = {method:"POST", headers:authHeaders()};
    if (isMultipart) options.body = body;
    else {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(body);
    }
    const res = await fetch(form.dataset.endpoint, options);
    const data = await res.json();
    if (!res.ok) {
      result.innerHTML = `<p class="error">${data.detail || "Request failed"}</p>`;
      return;
    }
    renderResult(data);
  });

  const history = document.querySelector("#history");
  if (history) loadHistory(history);
});

function renderResult(data) {
  const result = document.querySelector("#result");
  result.innerHTML = `
    <h2>${escapeHtml(data.planner)} recommendations</h2>
    <p class="muted">${escapeHtml(data.summary || "")}</p>
    ${data.recommendations.map(r => `
      <div class="rec">
        <strong>${escapeHtml(r.item)}</strong>
        <span class="price">₹${Number(r.estimated_price).toFixed(2)}</span>
        <div class="muted">${escapeHtml(r.platform)} • ${escapeHtml(r.category)}</div>
        <p>${escapeHtml(r.reason)}</p>
      </div>`).join("")}
  `;
}

async function loadHistory(el) {
  if (!token()) { el.innerHTML = "<p>Please login to view history.</p>"; return; }
  const res = await fetch("/api/history", {headers:authHeaders()});
  const data = await res.json();
  if (!res.ok) { el.innerHTML = `<p class="error">${data.detail || "Unable to load history"}</p>`; return; }
  if (!data.length) { el.innerHTML = "<p>No saved recommendations yet.</p>"; return; }
  el.innerHTML = data.map(x => `<article class="card"><h3>${escapeHtml(x.planner)}</h3><p class="muted">${escapeHtml(x.created_at)}</p><pre>${escapeHtml(x.output_json)}</pre></article>`).join("");
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}
