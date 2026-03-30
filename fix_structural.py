import re

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/nsm-dashboard.html', 'r') as f:
    lines = f.readlines()

# find where weekly performance starts
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="section" id="weekly-performance-section">' in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if '</div>' in lines[i] and '</div>' in lines[i-1] and 'margin-top' in lines[i-1]:
            # This is fragile, let's find the closing div of the section.
            pass

