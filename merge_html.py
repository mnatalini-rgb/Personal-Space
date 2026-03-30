import re

with open('weekly-plan-16-21-mar-2026.html', 'r', encoding='utf-8') as f:
    html1 = f.read()

with open('weekly-plan-23-28-mar-2026.html', 'r', encoding='utf-8') as f:
    html2 = f.read()

# Extract styles from file 2 (since they are identical)
# Wait, let's just find the end of the <style> block and everything before it
style_end_idx = html2.find('</style>')
head_part = html2[:style_end_idx]

# Add the week-selector css
week_selector_css = """
    .week-selector { display: inline-flex; background-color: var(--surface); border: 1px solid var(--border); border-radius: 9999px; padding: 0.25rem; gap: 0.25rem; margin-bottom: 1.5rem; }
    .week-btn { background: transparent; color: var(--text-muted); border: none; padding: 0.5rem 1.5rem; border-radius: 9999px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: all 0.15s ease; }
    .week-btn:hover { color: var(--text); }
    .week-btn.active { background-color: var(--accent); color: #fff; }
"""

header_html = """
<body>
  <div class="container">

    <header>
      <h1>Weekly Plan</h1>
      <div class="subtitle" id="weekSubtitle">Mon 23 &ndash; Fri 28 March 2026 &middot; Monetisation (Ads &amp; Partnerships)</div>
      <span class="faceit-badge">FACEIT</span>
    </header>

    <div class="week-selector">
      <button class="week-btn" data-target="week-16-21" data-subtitle="Mon 16 &ndash; Fri 21 March 2026 &middot; Monetisation (Ads &amp; Partnerships)">Mar 16–21</button>
      <button class="week-btn active" data-target="week-23-28" data-subtitle="Mon 23 &ndash; Fri 28 March 2026 &middot; Monetisation (Ads &amp; Partnerships)">Mar 23–28</button>
    </div>

    <section class="today-focus" id="todayFocusSection">
      <h2>Today's Focus <span id="todayFocusDate"></span></h2>
      <div class="today-focus-content" id="todayFocusContent"></div>
    </section>
"""

# Extract the content blocks
# Start from <section class="dashboard"> to </footer>
def get_content_body(html):
    start_str = '<section class="dashboard">'
    end_str = '</footer>'
    start_idx = html.find(start_str)
    end_idx = html.find(end_str) + len(end_str)
    return html[start_idx:end_idx]

content1 = get_content_body(html1)
content2 = get_content_body(html2)

# Script part
script_part = """
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const weekBtns = document.querySelectorAll('.week-btn');
      const weekContents = document.querySelectorAll('.week-content');
      const weekSubtitle = document.getElementById('weekSubtitle');
      
      const today = new Date();
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const todayName = dayNames[today.getDay()];
      
      function updateTodayFocus(activeWeekContainer) {
        const dayRows = activeWeekContainer.querySelectorAll('.day-row-list');
        let targetRow = null;
        let targetDayName = '';
        let targetDateStr = '';
        
        for (const row of dayRows) {
          const labelEl = row.querySelector('.day-label');
          if (!labelEl) continue;
          
          const textNode = Array.from(labelEl.childNodes).find(n => n.nodeType === Node.TEXT_NODE);
          const text = textNode ? textNode.textContent.trim() : '';
          
          const dateSpan = labelEl.querySelector('.day-date');
          const dateStr = dateSpan ? dateSpan.textContent.trim() : '';
          
          if (text === todayName) {
            targetRow = row;
            targetDayName = text;
            targetDateStr = dateStr;
            break;
          }
        }
        
        if (!targetRow && dayRows.length > 0) {
          const dayOfWeek = today.getDay();
          if (dayOfWeek === 0 || dayOfWeek === 6) {
            targetRow = dayRows[0];
          } else {
            targetRow = dayRows[0]; 
          }
          
          if (targetRow) {
             const labelEl = targetRow.querySelector('.day-label');
             const textNode = Array.from(labelEl.childNodes).find(n => n.nodeType === Node.TEXT_NODE);
             targetDayName = textNode ? textNode.textContent.trim() : '';
             const dateSpan = labelEl.querySelector('.day-date');
             targetDateStr = dateSpan ? dateSpan.textContent.trim() : '';
          }
        }
        
        const focusDate = document.getElementById('todayFocusDate');
        const focusContent = document.getElementById('todayFocusContent');
        
        if (targetRow) {
          const isToday = targetDayName === todayName;
          focusDate.textContent = `\\u2014 ${isToday ? 'Today, ' : ''}${targetDayName} ${targetDateStr}`;
          
          const tasksContainer = targetRow.querySelector('.day-tasks');
          focusContent.innerHTML = '';
          if (tasksContainer) {
            const clone = tasksContainer.cloneNode(true);
            focusContent.appendChild(clone);
          } else {
            focusContent.innerHTML = '<p style="color: var(--text-muted)">No tasks scheduled.</p>';
          }
        } else {
          focusDate.textContent = '';
          focusContent.innerHTML = '<p style="color: var(--text-muted)">No tasks scheduled today.</p>';
        }
      }

      weekBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          weekBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          
          weekSubtitle.innerHTML = btn.getAttribute('data-subtitle');
          
          const targetId = btn.getAttribute('data-target');
          let activeContainer = null;
          
          weekContents.forEach(content => {
            if (content.id === targetId) {
              content.style.display = 'block';
              activeContainer = content;
            } else {
              content.style.display = 'none';
            }
          });
          
          if (activeContainer) {
            updateTodayFocus(activeContainer);
          }
        });
      });

      const initialActive = document.querySelector('.week-btn.active');
      if (initialActive) {
        const targetId = initialActive.getAttribute('data-target');
        const activeContainer = document.getElementById(targetId);
        if (activeContainer) updateTodayFocus(activeContainer);
      }
    });
  </script>
</body>
</html>
"""

# Title tag adjustment: let's just make it a generic "Weekly Plan" or keep the active one
new_head = head_part.replace('<title>Weekly Plan — 23–28 March 2026</title>', '<title>Weekly Plan</title>')

with open('weekly-plan.html', 'w', encoding='utf-8') as f:
    f.write(new_head)
    f.write(week_selector_css)
    f.write('  </style>\n</head>\n')
    f.write(header_html)
    
    f.write('    <div class="week-content" id="week-16-21" style="display: none;">\n')
    f.write(content1)
    f.write('\n    </div>\n\n')
    
    f.write('    <div class="week-content" id="week-23-28">\n')
    f.write(content2)
    f.write('\n    </div>\n')
    
    f.write(script_part)

