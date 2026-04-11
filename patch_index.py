import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add sidebar CSS before </style>
sidebar_css = """
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
      z-index: 200;
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
      padding: 0;
      min-width: 0;
      background-color: var(--bg);
    }
    @media (max-width: 900px) {
      .dashboard-layout { flex-direction: column; }
      .sidebar { width: 100% !important; height: auto; position: relative; border-right: none; border-bottom: 1px solid var(--border); padding: 16px; flex-direction: row; align-items: center; justify-content: space-between; z-index: 100; }
      .sidebar-toggle { display: none; }
      .sidebar-nav { flex-direction: row; flex-wrap: wrap; width: 100%; gap: 8px; }
      .nav-btn { width: auto; padding: 8px 16px; }
      .sidebar.collapsed .btn-label { opacity: 1; width: auto; overflow: visible; }
      .main-content { padding: 0; width: 100%; }
    }
"""
content = content.replace("</style>", sidebar_css + "\n  </style>")

# 2. Add Sidebar HTML & wrap body in dashboard-layout
sidebar_html = """  <div class="dashboard-layout">
    <aside class="sidebar" id="sidebar">
      <button class="sidebar-toggle" onclick="toggleSidebar()">
        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <nav class="sidebar-nav">
        <button class="nav-btn active" onclick="scrollToSection('core')">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
          <span class="btn-label">Core Workflows</span>
        </button>
        <button class="nav-btn" onclick="scrollToSection('analytics')">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
          <span class="btn-label">Analytics</span>
        </button>
        <button class="nav-btn" onclick="scrollToSection('experiments')">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m14-6h2m-2 6h2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path></svg>
          <span class="btn-label">Experiments</span>
        </button>
        <button class="nav-btn" onclick="scrollToSection('releases')">
          <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path><line x1="4" y1="22" x2="4" y2="15"></line></svg>
          <span class="btn-label">Releases</span>
        </button>
      </nav>
    </aside>
    <main class="main-content">
"""

content = content.replace("<body>\n", "<body>\n" + sidebar_html)
content = content.replace("</body>", "    </main>\n  </div>\n\n</body>")

# 3. Add ids and logic
content = content.replace('id="core"', 'id="core"')
content = content.replace('<div class="subsection-header">\n      <span class="subsection-dot dot-shipped"></span>\n      Releases\n    </div>', '<div class="subsection-header" id="releases">\n      <span class="subsection-dot dot-shipped"></span>\n      Releases\n    </div>')

script_addition = """
    // Sidebar logic
    function toggleSidebar() {
      const sidebar = document.getElementById('sidebar');
      sidebar.classList.toggle('collapsed');
      localStorage.setItem('hub-sidebar-collapsed', sidebar.classList.contains('collapsed'));
    }

    function scrollToSection(id) {
      const el = document.getElementById(id);
      if (el) {
        const yOffset = -80; 
        const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
        window.scrollTo({top: y, behavior: 'smooth'});
      }
    }

    // ScrollSpy
    window.addEventListener('scroll', () => {
      const sections = ['core', 'analytics', 'experiments', 'releases'];
      let current = '';
      
      for (const id of sections) {
        const el = document.getElementById(id);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 100) {
            current = id;
          }
        }
      }
      
      if (current) {
        document.querySelectorAll('.sidebar-nav .nav-btn').forEach(btn => {
          btn.classList.remove('active');
          if (btn.getAttribute('onclick').includes(current)) {
            btn.classList.add('active');
          }
        });
      }
    });

    // Init sidebar state
    document.addEventListener('DOMContentLoaded', () => {
      if (localStorage.getItem('hub-sidebar-collapsed') === 'true') {
        document.getElementById('sidebar').classList.add('collapsed');
      }
    });
"""
content = content.replace("</script>\n\n</body>", script_addition + "\n  </script>\n\n</body>")

with open('index.html', 'w') as f:
    f.write(content)

