import re

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/tradeit-nsm-dashboard.html', 'r') as f:
    content = f.read()

# Fix the IDs and titles for the corrupted sections
# 1. Headline KPIs -> section-1
# 2. NSM Trend -> section-2
# 2. Region-Level Summary -> section-3, title "3. Region-Level Summary"
# 4. Month-over-Month Comparison -> section-4, title "4. Month-over-Month Comparison"
# 5. NA A/B Test (January) -> section-5, title "5. NA A/B Test (January)"
# 6. Segment Performance -> section-6, title "6. Segment Performance"

# Let's just use regex to fix them sequentially
content = re.sub(
    r'<div class="section" id="section-\d+">\s*<h2 class="section-title">2\. Region-Level Summary</h2>',
    '<div class="section" id="section-3">\n            <h2 class="section-title">3. Region-Level Summary</h2>',
    content
)

content = re.sub(
    r'<div class="section" id="section-\d+">\s*<h2 class="section-title">4\. Month-over-Month Comparison</h2>',
    '<div class="section" id="section-4">\n            <h2 class="section-title">4. Month-over-Month Comparison</h2>',
    content
)

content = re.sub(
    r'<div class="section" id="section-\d+">\s*<h2 class="section-title">5\. NA A/B Test \(January\)</h2>',
    '<div class="section" id="section-5">\n            <h2 class="section-title">5. NA A/B Test (January)</h2>',
    content
)

content = re.sub(
    r'<div class="section" id="section-\d+">\s*<h2 class="section-title">6\. Segment Performance \(\€/1K EBU\)</h2>',
    '<div class="section" id="section-6">\n            <h2 class="section-title">6. Segment Performance (€/1K EBU)</h2>',
    content
)

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/tradeit-nsm-dashboard.html', 'w') as f:
    f.write(content)
