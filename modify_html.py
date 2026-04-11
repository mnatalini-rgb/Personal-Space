import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace CSS variables
new_vars = """    :root {
      --bg: #EEF2F3;
      --surface: #ffffff;
      --border: #E2E8F0;
      --text: #1A1A2E;
      --text-muted: #6B7280;
      --accent: #2563eb;
      --accent-light: rgba(37, 99, 235, 0.08);
      --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      --radius-lg: 20px;
      --radius-md: 14px;
      --radius-sm: 8px;
      --shadow: 0 2px 12px rgba(0,0,0,0.06);
      --shadow-hover: 0 8px 32px rgba(0,0,0,0.10);
      --sidebar-width: 240px;
      --sidebar-collapsed-width: 56px;
    }"""
content = re.sub(r':root\s*\{[^}]*\}', new_vars, content)

# Remove sticky header & header nav css
content = re.sub(r'/\*\s*Sticky Header\s*\*/.*?(?=/\*\s*Hero\s*\*/)', '', content, flags=re.DOTALL)

# Add dashboard layout css
layout_css = """
    /* Dashboard Layout */
    .top-nav { background:#EEF2F3; padding:8px 24px; font-size:13px; font-weight:500; border-bottom:1px solid #E2E8F0; }

    .dashboard-layout {
      display: flex;
      max-width: 1400px;
      margin: 0 auto;
      align-items: flex-start;
    }

    .sidebar {
      width: var(--sidebar-width);
      flex-shrink: 0;
      padding: 2rem 1.5rem 2rem 2rem;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      border-right: 1px solid var(--border);
      transition: width 0.25s ease, padding 0.25s ease;
    }

    .sidebar.collapsed {
      width: var(--sidebar-collapsed-width);
      padding: 2rem 0.5rem;
    }

    .sidebar-toggle {
      width: 100%;
      display: flex;
      justify-content: flex-end;
      background: none;
      border: none;
      cursor: pointer;
      padding: 0.5rem;
      margin-bottom: 1rem;
      color: var(--text-muted);
    }

    .sidebar-toggle svg {
      transition: transform 0.25s ease;
    }

    .sidebar.collapsed .sidebar-toggle svg {
      transform: rotate(180deg);
    }

    .nav-section-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
      padding-left: 12px;
    }
    
    .sidebar.collapsed .nav-section-label {
      display: none;
    }

    .sidebar-nav {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .sidebar .nav-btn {
      background: transparent;
      color: var(--text-muted);
      border: none;
      padding: 0.85rem 1rem;
      border-radius: var(--radius-md);
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      width: 100%;
    }

    .sidebar .nav-btn:hover { 
      color: var(--text); 
      background: var(--surface);
      box-shadow: var(--shadow);
    }

    .sidebar .nav-btn.active {
      background-color: var(--accent);
      color: #fff;
      box-shadow: 0 4px 12px var(--accent-light);
    }

    .sidebar.collapsed .nav-btn {
      justify-content: center;
      padding: 0.85rem 0;
    }

    .sidebar.collapsed .btn-label {
      display: none;
    }

    .sidebar.collapsed .nav-btn svg {
      margin-right: 0 !important;
    }

    .main-content {
      flex-grow: 1;
      padding: 0;
      min-width: 0;
    }

    @media (max-width: 900px) {
      .dashboard-layout { flex-direction: column; }
      .sidebar { width: 100%; height: auto; position: relative; border-right: none; border-bottom: 1px solid var(--border); padding: 1.5rem; flex-direction: row; }
      .sidebar-toggle { display: none; }
      .sidebar.collapsed { width: 100%; padding: 1.5rem; }
      .sidebar.collapsed .btn-label { display: inline; }
      .sidebar.collapsed .nav-btn svg { margin-right: 8px !important; }
      .sidebar-nav { flex-direction: row; flex-wrap: wrap; }
      .sidebar .nav-btn { width: auto; }
      .nav-section-label { display: none; }
    }
"""
content = content.replace("    /* Hero */", layout_css + "\n    /* Hero */")

# Add SVGs colors
icon_colors = """
    /* Icon backgrounds per section */
    .icon-projects { background: rgba(37, 99, 235, 0.10); color: #2563eb; }
    .icon-roadmap { background: rgba(124, 58, 237, 0.10); color: #7c3aed; }
    .icon-pipeline { background: rgba(16, 185, 129, 0.10); color: #059669; }
    .icon-releases { background: rgba(139, 92, 246, 0.10); color: #8b5cf6; }
    .icon-nsm { background: rgba(217, 119, 6, 0.10); color: #d97706; }
    .icon-qbr { background: rgba(79, 70, 229, 0.10); color: #4f46e5; }
    .icon-prebid { background: rgba(220, 38, 38, 0.10); color: #dc2626; }
    .icon-prebid-slides { background: rgba(234, 88, 12, 0.10); color: #ea580c; }
    .icon-skinvault { background: rgba(8, 145, 178, 0.10); color: #0891b2; }
    .icon-peripheral { background: rgba(156, 163, 175, 0.10); color: #6b7280; }
    .icon-trust-modal { background: rgba(5, 150, 105, 0.10); color: #059669; }
    .icon-interstitial { background: rgba(220, 38, 38, 0.10); color: #dc2626; }
    .icon-csstats { background: rgba(37, 99, 235, 0.10); color: #2563eb; }
    .icon-ads-alert { background: rgba(79, 70, 229, 0.10); color: #4f46e5; }
    .icon-rewarded-video { background: rgba(234, 88, 12, 0.10); color: #ea580c; }
    .icon-mystery-box { background: rgba(168, 85, 247, 0.10); color: #a855f7; }
    .icon-age-modal { background: rgba(14, 165, 233, 0.10); color: #0ea5e9; }
    .icon-weekly { background: rgba(14, 165, 233, 0.10); color: #0ea5e9; }"""

content = re.sub(r'/\*\s*Icon backgrounds per section\s*\*/.*?(?=/\*\s*Footer\s*\*/)', icon_colors + "\n\n    ", content, flags=re.DOTALL)

# Re-write the HTML structure
body_start = content.find('<body>') + 6
body_end = content.find('<script>')

old_body = content[body_start:body_end]

# Generate new body
new_body = """
  <nav class="top-nav">Ads & Partnerships</nav>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <button type="button" class="sidebar-toggle" onclick="toggleSidebar()" title="Toggle sidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>
      <div class="nav-section-label">Navigation</div>
      <nav class="sidebar-nav">
        <button type="button" class="nav-btn active" onclick="scrollToSection('core')" title="Core Workflows">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px; flex-shrink: 0;"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          <span class="btn-label">Core Workflows</span>
        </button>
        <button type="button" class="nav-btn" onclick="scrollToSection('analytics')" title="Analytics">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px; flex-shrink: 0;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
          <span class="btn-label">Analytics</span>
        </button>
        <button type="button" class="nav-btn" onclick="scrollToSection('experiments')" title="Experiments">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px; flex-shrink: 0;"><path d="M9 3h6v7l5 8a2 2 0 0 1-1.7 3H5.7A2 2 0 0 1 4 18l5-8V3z"/><line x1="9" y1="3" x2="15" y2="3"/></svg>
          <span class="btn-label">Experiments</span>
        </button>
      </nav>
    </aside>
    <main class="main-content">
"""

# We need to extract the parts (Hero, Sections, Footer) and wrap them
main_content = re.sub(r'<!-- Sticky Header -->.*?</header>', '', old_body, flags=re.DOTALL)
new_body += main_content + "    </main>\n  </div>\n"

# Replace emojis with SVGs in new_body
emoji_map = {
    '📋': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>',
    '🗺️': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
    '⚙️': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    '📦': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    '💰': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    '📊': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    '🧪': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6v7l5 8a2 2 0 0 1-1.7 3H5.7A2 2 0 0 1 4 18l5-8V3z"/><line x1="9" y1="3" x2="15" y2="3"/></svg>',
    '💎': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9z"/><path d="M2 9h20"/></svg>',
    '🖥️': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    '📑': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    '🚀': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
}

for emoji, svg in emoji_map.items():
    new_body = new_body.replace(f'<div class="card-icon icon-projects">{emoji}</div>', f'<div class="card-icon icon-projects">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-roadmap">{emoji}</div>', f'<div class="card-icon icon-roadmap">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-pipeline">{emoji}</div>', f'<div class="card-icon icon-pipeline">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-releases">{emoji}</div>', f'<div class="card-icon icon-releases">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-nsm">{emoji}</div>', f'<div class="card-icon icon-nsm">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-qbr">{emoji}</div>', f'<div class="card-icon icon-qbr">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-prebid">{emoji}</div>', f'<div class="card-icon icon-prebid">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-prebid-slides">{emoji}</div>', f'<div class="card-icon icon-prebid-slides">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-skinvault">{emoji}</div>', f'<div class="card-icon icon-skinvault">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-peripheral">{emoji}</div>', f'<div class="card-icon icon-peripheral">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-trust-modal">{emoji}</div>', f'<div class="card-icon icon-trust-modal">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-interstitial">{emoji}</div>', f'<div class="card-icon icon-interstitial">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-csstats">{emoji}</div>', f'<div class="card-icon icon-csstats">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-ads-alert">{emoji}</div>', f'<div class="card-icon icon-ads-alert">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-rewarded-video">{emoji}</div>', f'<div class="card-icon icon-rewarded-video">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-mystery-box">{emoji}</div>', f'<div class="card-icon icon-mystery-box">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-age-modal">{emoji}</div>', f'<div class="card-icon icon-age-modal">{svg}</div>')
    new_body = new_body.replace(f'<div class="card-icon icon-weekly">{emoji}</div>', f'<div class="card-icon icon-weekly">{svg}</div>')

# some of the replacements might just be straightforward
for emoji, svg in emoji_map.items():
    new_body = new_body.replace(emoji, svg)

content = content[:body_start] + new_body + content[body_end:]

# Add JS functions
js_code = """<script>
    function scrollToSection(id) {
      document.getElementById(id).scrollIntoView({ behavior: 'smooth', block: 'start' });
      document.querySelectorAll('.sidebar-nav .nav-btn').forEach(b => b.classList.remove('active'));
      event.currentTarget.classList.add('active');
    }

    function toggleSidebar() {
      const sidebar = document.querySelector('.sidebar');
      sidebar.classList.toggle('collapsed');
      localStorage.setItem('hub-sidebar-collapsed', sidebar.classList.contains('collapsed'));
    }

    document.addEventListener('DOMContentLoaded', function() {
      if (localStorage.getItem('hub-sidebar-collapsed') === 'true') {
        document.querySelector('.sidebar').classList.add('collapsed');
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            document.querySelectorAll('.sidebar-nav .nav-btn').forEach(b => b.classList.remove('active'));
            const btn = document.querySelector(`.nav-btn[onclick*="${entry.target.id}"]`);
            if (btn) btn.classList.add('active');
          }
        });
      }, { threshold: 0.3 });

      document.querySelectorAll('.section').forEach(s => observer.observe(s));
    });
"""
content = content.replace('<script>', js_code)

with open('index.html', 'w') as f:
    f.write(content)
