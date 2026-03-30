import re

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/nsm-dashboard.html', 'r') as f:
    content = f.read()

# The weekly performance section we want to move:
# <div class="section" id="weekly-performance-section"> ... </div>
# It is currently between the end of Tradeit tab and the start of Winline tab.
# We want to move it to just before the closing </div> of tradeit-tab-missions.

pattern = re.compile(r'(    </div>\s*<!-- closes Mystery Box comparison section -->\s*)    </div>\s*(    <!-- Weekly Performance placeholder.*?</div>\s*)\s*</div>\s*<!-- \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* -->\s*<!-- WINLINE VIEW -->', re.DOTALL)

# Let's just find the section and extract it.
section_pattern = re.compile(r'(\s*<!-- Weekly Performance placeholder.*?</div>\s*</div>)', re.DOTALL)
match = section_pattern.search(content)

# Actually, I'll use a simpler approach.
