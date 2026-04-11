import re

with open("productivity-dashboard.html", "r") as f:
    content = f.read()

# 1. Add CSS
css_to_add = """
    /* Sidebar Layout */
    .dashboard-layout {
      display: flex;
      max-width: 1440px;
      margin: 0 auto;
      align-items: flex-start;
      min-height: 100vh;
    }
    .sidebar {
      width: var(--sidebar-width, 260px);
      flex-shrink: 0;
      padding: 24px 16px;
      position: sticky;
      top: 0;
      height: 100vh;
      border-right: 1px solid var(--border);
      background-color: var(--bg);
      transition: width 0.3s ease, padding 0.3s ease;
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
    }
    .sidebar.collapsed {
      width: var(--sidebar-collapsed-width, 64px);
      padding: 24px 8px;
    }
    .sidebar-toggle {
      background: none;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-muted);
      margin-bottom: 24px;
      align-self: flex-end;
      transition: transform 0.3s ease, background-color 0.2s ease;
    }
    .sidebar-toggle:hover {
      background-color: var(--surface);
      color: var(--text);
    }
    .sidebar.collapsed .sidebar-toggle {
      transform: rotate(180deg);
      align-self: center;
    }
    .sidebar-nav {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .nav-btn {
      background: transparent;
      color: var(--text-muted);
      border: none;
      padding: 10px 12px;
      border-radius: var(--radius-sm);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
      white-space: nowrap;
    }
    .nav-btn svg {
      flex-shrink: 0;
    }
    .nav-btn:hover { 
      color: var(--text); 
      background: var(--surface);
      box-shadow: var(--shadow);
    }
    .nav-btn.active {
      background-color: var(--accent);
      color: #fff;
      box-shadow: 0 4px 12px var(--accent-light);
    }
    .sidebar.collapsed .btn-label {
      opacity: 0;
      width: 0;
      overflow: hidden;
    }
    .main-content {
      flex-grow: 1;
      padding: 0 24px 24px;
      min-width: 0;
      background-color: var(--bg);
    }
    @media (max-width: 900px) {
      .dashboard-layout { flex-direction: column; }
      .sidebar { width: 100% !important; height: auto; position: relative; border-right: none; border-bottom: 1px solid var(--border); padding: 16px; flex-direction: row; align-items: center; justify-content: space-between; }
      .sidebar-toggle { display: none; }
      .sidebar-nav { flex-direction: row; flex-wrap: wrap; width: 100%; gap: 8px; }
      .nav-btn { width: auto; padding: 8px 16px; }
      .sidebar.collapsed .btn-label { opacity: 1; width: auto; overflow: visible; }
      .main-content { padding: 16px; width: 100%; }
    }
"""

if ".dashboard-layout {" not in content:
    content = content.replace("</style>", css_to_add + "\n  </style>")

# Remove the old .nav-tabs css and .settings-btn css so we don't conflict, though not strictly necessary.

# 2. Modify HTML layout
old_header_html = """  <nav style="background:#EEF2F3;padding:8px 24px;font-family:Inter,-apple-system,sans-serif;font-size:13px;font-weight:500;border-bottom:1px solid #E2E8F0;display:flex;align-items:center;gap:8px;">
    <a href="index.html" style="color:#1A1A2E;text-decoration:none;">← Hub</a>
    <span style="color:#CBD5E1;">·</span>
    <span style="color:#6B7280;">Productivity Dashboard</span>
  </nav>

  <div class="container">
    <header>
      <h1>Productivity Dashboard</h1>
      <div class="nav-tabs" id="navTabs">
        <button class="tab-btn active" data-target="tasks">Tasks</button>
        <button class="tab-btn" data-target="projects">Projects</button>
        <button class="tab-btn" data-target="weekly">Weekly Review</button>
        <button class="tab-btn" data-target="monthly">Monthly Review</button>
      </div>
      <button class="settings-btn" onclick="openSettings()">⚙️ Settings</button>
    </header>"""

new_header_html = """  <div class="dashboard-layout">
    <aside class="sidebar">
      <button class="sidebar-toggle" onclick="toggleSidebar()">
        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <nav class="sidebar-nav">
        <button class="nav-btn active" data-target="tasks">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5H21M9 12H21M9 19H21M3 5L5 7L7 3M3 12L5 14L7 10M3 19L5 21L7 17"/></svg>
          <span class="btn-label">Tasks</span>
        </button>
        <button class="nav-btn" data-target="projects">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
          <span class="btn-label">Projects</span>
        </button>
        <button class="nav-btn" data-target="weekly">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M9 14l1.5 3 1.5-3 1.5 3 1.5-3"/></svg>
          <span class="btn-label">Weekly Review</span>
        </button>
        <button class="nav-btn" data-target="monthly">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span class="btn-label">Monthly Review</span>
        </button>
        <button class="nav-btn" onclick="openSettings()">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06-.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1h.09a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
          <span class="btn-label">Settings</span>
        </button>
      </nav>
    </aside>
    <main class="main-content">
      <nav style="background:#EEF2F3;padding:16px 0;font-family:Inter,-apple-system,sans-serif;font-size:13px;font-weight:500;display:flex;align-items:center;gap:8px;margin-bottom:24px;">
        <a href="index.html" style="color:#1A1A2E;text-decoration:none;">← Hub</a>
        <span style="color:#CBD5E1;">·</span>
        <span style="color:#6B7280;">Productivity Dashboard</span>
      </nav>
      <header style="border-bottom:none;margin-bottom:24px;padding-bottom:0;">
        <h1 style="font-size:28px;">Productivity Dashboard</h1>
      </header>"""

content = content.replace(old_header_html, new_header_html)

# Now we need to close the <div class="dashboard-layout"> instead of the <div class="container">
# At the end of the file, right before <!-- Settings Modal -->
end_container_html = """    </div>
  </div>

  <!-- Settings Modal -->"""

new_end_container_html = """    </div>
    </main>
  </div>

  <!-- Settings Modal -->"""

content = content.replace(end_container_html, new_end_container_html)

js_to_add = """
    // --- Sidebar Logic ---
    function toggleSidebar() {
      const sidebar = document.querySelector('.sidebar');
      if(sidebar) {
        sidebar.classList.toggle('collapsed');
        localStorage.setItem('productivity-sidebar-collapsed', sidebar.classList.contains('collapsed'));
      }
    }

    const sidebarCollapsed = localStorage.getItem('productivity-sidebar-collapsed') === 'true';
    if (sidebarCollapsed) {
      const sidebar = document.querySelector('.sidebar');
      if (sidebar) sidebar.classList.add('collapsed');
    }

    // Nav switching
    document.querySelectorAll('.nav-btn[data-target]').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.dataset.target;
        document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
        document.getElementById(target)?.classList.add('active');
        document.querySelectorAll('.nav-btn[data-target]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      });
    });
"""

# Insert JS logic after <script> tag
if "function toggleSidebar()" not in content:
    content = content.replace("<script>", "<script>\n" + js_to_add)

# Now the tab buttons in JS. The old code might have had listeners for .tab-btn. We should ensure we don't break old scripts but the new `.nav-btn` code handles switching. 
# Look for old tab script if any
old_js_tabs = """document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
        document.getElementById(btn.dataset.target).classList.add('active');
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      });
    });"""

if old_js_tabs in content:
    content = content.replace(old_js_tabs, "// (old tab script removed)")
else:
    # Use regex to find it
    content = re.sub(r"document\.querySelectorAll\('\.tab-btn'\)\.forEach.*?\}\);\s*\}\);", "// (old tab script removed)", content, flags=re.DOTALL)

with open("productivity-dashboard.html", "w") as f:
    f.write(content)

