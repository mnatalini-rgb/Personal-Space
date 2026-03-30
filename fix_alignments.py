with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/prebid-slides.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("left: 40px;\n    height: 40px;\n    color: #FFFFFF;\n    font-family: 'Barlow Condensed'", "left: 80px;\n    height: 40px;\n    color: #FFFFFF;\n    font-family: 'Barlow Condensed'")
content = content.replace("padding-left: 40px;\n    z-index: 10;", "padding-left: 80px;\n    z-index: 10;")
content = content.replace("right: 40px;\n    height: 30px;", "right: 80px;\n    height: 30px;")
content = content.replace("bottom: 40px; /* Right above the footer bar */\n    left: 40px;", "bottom: 45px; /* Right above the footer bar */\n    left: 80px;")
content = content.replace("bottom: 40px;\n    left: 50%;", "bottom: 45px;\n    left: 50%;") # nav-hint

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/prebid-slides.html', 'w', encoding='utf-8') as f:
    f.write(content)
