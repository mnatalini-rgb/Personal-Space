import re

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/index.html', 'r') as f:
    content = f.read()

# Remove .card-desc
content = re.sub(r'\s*<div class="card-desc">.*?</div>', '', content, flags=re.DOTALL)

# Add .summary-card css
css_add = """
    /* Summary Card */
    .summary-card {
      background: rgba(37, 99, 235, 0.03);
      border: 1px solid rgba(37, 99, 235, 0.1);
      border-radius: var(--radius-sm);
      padding: 24px;
      margin-bottom: 24px;
    }
    .summary-header {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 12px;
    }
    .summary-header svg {
      color: #2563eb;
    }
    .summary-body {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.6;
    }
    .summary-placeholder {
      opacity: 0.8;
    }
"""

content = content.replace("/* Sections */", css_add + "\n    /* Sections */")

# Update .card-grid css
content = re.sub(r'\.card-grid \{\s*display: grid;\s*grid-template-columns: repeat\(auto-fill, minmax\(280px, 1fr\)\);\s*gap: 14px;\s*\}', 
                 '.card-grid {\n      display: grid;\n      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));\n      gap: 16px;\n    }', content)

# Update a.card
content = re.sub(r'a\.card \{\s*display: flex;\s*gap: 16px;\s*align-items: flex-start;\s*background: var\(--surface\);\s*border: 1px solid var\(--border\);\s*border-radius: var\(--radius-sm\);\s*padding: 20px;',
                 'a.card {\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      text-align: center;\n      gap: 12px;\n      background: var(--surface);\n      border: 1px solid var(--border);\n      border-radius: var(--radius-sm);\n      padding: 24px 16px;', content)

# Update .card-icon
content = re.sub(r'\.card-icon \{\s*width: 40px;\s*height: 40px;\s*border-radius: 10px;\s*display: flex;\s*align-items: center;\s*justify-content: center;\s*font-size: 20px;\s*flex-shrink: 0;\s*\}',
                 '.card-icon {\n      width: 48px;\n      height: 48px;\n      border-radius: 12px;\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      font-size: 24px;\n      flex-shrink: 0;\n      margin-bottom: 4px;\n    }', content)

# Update .card-body
content = re.sub(r'\.card-body \{\s*flex: 1;\s*min-width: 0;\s*\}',
                 '.card-body {\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      gap: 10px;\n      width: 100%;\n    }', content)

# Update .card-title
content = re.sub(r'\.card-title \{\s*font-size: 15px;\s*font-weight: 600;\s*margin-bottom: 4px;\s*display: flex;\s*align-items: center;\s*gap: 8px;\s*flex-wrap: wrap;\s*\}',
                 '.card-title {\n      font-size: 14px;\n      font-weight: 600;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      gap: 10px;\n      width: 100%;\n      line-height: 1.3;\n    }', content)

# Update .badge
content = re.sub(r'\.badge \{\s*font-size: 10px;',
                 '.badge {\n      font-size: 11px;', content)

# Insert the new section
summary_html = """
  <!-- Daily Summary -->
  <section id="daily-summary" class="section" style="padding-top: 0;">
    <div class="summary-card">
      <div class="summary-header">
        <svg width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
        <span id="daily-date">Today</span>
      </div>
      <div class="summary-body">
        <p class="summary-placeholder">No updates yet. Daily summary will appear here.</p>
      </div>
    </div>
  </section>
"""
content = content.replace('  <!-- Section 1: Core Workflows -->', summary_html + '\n  <!-- Section 1: Core Workflows -->')

# Update Hero
content = re.sub(r'  <!-- Hero -->\n  <div class="hero">\n    <h1>Ads & Partnerships Hub</h1>\n    <p>Dashboards, metrics, experiments, and project tracking — Moritz Natalini</p>\n  </div>',
                 '  <!-- Hero -->\n  <div class="hero" style="padding: 40px 32px 24px;">\n    <h1 style="font-size: 24px;">Ads & Partnerships</h1>\n  </div>', content)

# Add the JS for date
js_date = """
    // Generate today's date
    (function() {
      const dateEl = document.getElementById('daily-date');
      if (dateEl) {
        const options = { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' };
        dateEl.textContent = 'Today — ' + new Date().toLocaleDateString('en-GB', options);
      }
    })();
"""
content = content.replace("  <script>", "  <script>\n" + js_date)

# Add badges to section headers
content = content.replace('<div class="section-header">Core Workflows</div>', '<div class="section-header">Core Workflows &middot; 4</div>')
content = content.replace('<div class="section-header">Analytics & Metrics</div>', '<div class="section-header">Analytics & Metrics &middot; 2</div>')
content = content.replace('<div class="section-header">Experiments & Releases</div>', '<div class="section-header">Experiments & Releases</div>')

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/index.html', 'w') as f:
    f.write(content)
