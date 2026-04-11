import re

with open('nsm-dashboard.html', 'r') as f:
    content = f.read()

# Add missing CSS for sidebar toggling
sidebar_css = """
        /* Sidebar Toggle Logic */
        .sidebar {
            transition: width 0.3s ease, padding 0.3s ease;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
            z-index: 100;
        }
        .sidebar.collapsed {
            width: 64px;
            padding: 2rem 0.5rem;
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
        .sidebar.collapsed .btn-label {
            opacity: 0;
            width: 0;
            overflow: hidden;
            display: none;
        }
        .sidebar .partner-btn {
            gap: 12px;
            white-space: nowrap;
        }
        .sidebar .partner-btn svg {
            flex-shrink: 0;
        }
"""
content = content.replace("/* Dashboard Layout */", sidebar_css + "\n        /* Dashboard Layout */")

# Replace sidebar html
sidebar_html_old = """        <aside class="sidebar">
            <div class="partner-selector-wrapper">
                <div class="partner-selector">
                    <button type="button" id="btn-combined" class="partner-btn active" onclick="switchPartner('combined')">📊 Portfolio</button>
                    <button type="button" id="btn-tradeit" class="partner-btn" onclick="switchPartner('tradeit')">🎯 Tradeit</button>
                    <button type="button" id="btn-winline" class="partner-btn" onclick="switchPartner('winline')">🎲 Winline</button>
                    <button type="button" id="btn-whitemarket" class="partner-btn" onclick="switchPartner('whitemarket')">🛒 WhiteMarket</button>
                    <button type="button" id="btn-paysafe" class="partner-btn" onclick="switchPartner('paysafe')">💳 PaySafe</button>
                    <button type="button" id="btn-roadmap" class="partner-btn roadmap-btn" onclick="switchPartner('roadmap')">📋 Roadmap</button>
                </div>
            </div>
        </aside>"""

sidebar_html_new = """        <aside class="sidebar" id="sidebar">
            <button class="sidebar-toggle" onclick="toggleSidebar()">
                <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
            </button>
            <div class="partner-selector-wrapper">
                <div class="partner-selector">
                    <button type="button" id="btn-combined" class="partner-btn active" onclick="switchPartner('combined')">
                        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>
                        <span class="btn-label">Portfolio</span>
                    </button>
                    <button type="button" id="btn-tradeit" class="partner-btn" onclick="switchPartner('tradeit')">
                        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>
                        <span class="btn-label">Tradeit</span>
                    </button>
                    <button type="button" id="btn-winline" class="partner-btn" onclick="switchPartner('winline')">
                        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><circle cx="15.5" cy="15.5" r="1.5"></circle></svg>
                        <span class="btn-label">Winline</span>
                    </button>
                    <button type="button" id="btn-whitemarket" class="partner-btn" onclick="switchPartner('whitemarket')">
                        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
                        <span class="btn-label">WhiteMarket</span>
                    </button>
                    <button type="button" id="btn-paysafe" class="partner-btn" onclick="switchPartner('paysafe')">
                        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
                        <span class="btn-label">PaySafe</span>
                    </button>
                    <button type="button" id="btn-roadmap" class="partner-btn roadmap-btn" onclick="switchPartner('roadmap')">
                        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                        <span class="btn-label">Roadmap</span>
                    </button>
                </div>
            </div>
        </aside>"""

content = content.replace(sidebar_html_old, sidebar_html_new)

# Add toggle JS logic
script_addition = """
    // Sidebar logic
    function toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.toggle('collapsed');
        localStorage.setItem('nsm-sidebar-collapsed', sidebar.classList.contains('collapsed'));
    }

    document.addEventListener('DOMContentLoaded', () => {
        if (localStorage.getItem('nsm-sidebar-collapsed') === 'true') {
            document.getElementById('sidebar').classList.add('collapsed');
        }
    });
"""
content = content.replace("function switchPartner(partner)", script_addition + "\n    function switchPartner(partner)")

with open('nsm-dashboard.html', 'w') as f:
    f.write(content)

