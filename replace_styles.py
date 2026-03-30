import re

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/prebid-slides.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_style = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@400;600;700&display=swap');

  :root {
    --bg: #FEFEFE;
    --surface: #EEEEEE;
    --surface-2: #CCCCCC;
    --border: #CCCCCC;
    --text: #000000;
    --text-muted: #595959;
    --accent: #4285F4;
    --accent-light: #4285F4;
    --green: #0097A7;
    --green-bg: #EEEEEE;
    --red: #D63031;
    --orange: #FFAB40;
    --orange-bg: #EEEEEE;
    --blue: #78909C;
    --blue-bg: #EEEEEE;
    --dark-bar: #262626;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  html, body { height: 100%; overflow: hidden; }

  body {
    font-family: 'Barlow', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
  }

  .deck { position: relative; width: 100vw; height: 100vh; }

  .slide {
    position: absolute;
    inset: 0;
    display: none;
    flex-direction: column;
    justify-content: center;
    padding: 100px 80px 80px 80px; /* 60px below top bar + 40px top bar = 100px; 50px above footer + 30px footer = 80px */
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .slide.active { display: flex; opacity: 1; }

  /* Top Bar */
  .slide::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 40px;
    background: var(--dark-bar);
    z-index: 1;
  }

  /* Footer Bar */
  .slide::after {
    content: 'CONFIDENTIAL';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 30px;
    background: var(--dark-bar);
    color: #FFFFFF;
    font-family: 'Barlow', sans-serif;
    font-weight: 500;
    font-size: 7pt;
    display: flex;
    align-items: center;
    padding-left: 40px;
    z-index: 10;
  }

  /* We position .label over the top bar */
  .label {
    position: absolute;
    top: 0;
    left: 40px;
    height: 40px;
    color: #FFFFFF;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px; /* 16-18pt per spec */
    font-weight: 700;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    letter-spacing: normal;
    z-index: 2;
    margin: 0;
  }

  /* Specific fix for labels inside KPI cards */
  .kpi .label {
    position: static;
    height: auto;
    color: #000000;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    text-transform: uppercase;
    display: block;
    margin-bottom: 6px;
    letter-spacing: normal;
    font-weight: 700;
  }

  .slide-number {
    position: absolute;
    bottom: 0;
    right: 40px;
    height: 30px;
    font-family: 'Barlow', sans-serif;
    font-size: 7pt;
    color: #FFFFFF;
    font-weight: 500;
    display: flex;
    align-items: center;
    z-index: 11;
  }

  .slide-footer {
    position: absolute;
    bottom: 40px; /* Right above the footer bar */
    left: 40px;
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 400;
  }

  h1, h2 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32pt !important;
    font-weight: 700;
    line-height: 1.15;
    margin-bottom: 16px;
    color: #000000;
    margin-top: 20px; /* Provide some gap from top bar if needed */
  }

  h3 { 
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px; 
    font-weight: 600; 
    line-height: 1.3; 
    margin-bottom: 12px; 
    color: #000000;
  }

  .subtitle { 
    font-family: 'Barlow', sans-serif;
    font-size: 13pt; 
    color: #000000; 
    font-weight: 400; 
    line-height: 1.5; 
  }

  .gradient-text {
    background: none;
    -webkit-background-clip: unset;
    -webkit-text-fill-color: unset;
    color: #000000;
  }

  .positive { color: var(--green); }
  .negative { color: var(--red); }
  .warning { color: var(--orange); }

  .kpi-row {
    display: flex;
    gap: 32px;
    margin-top: 32px;
  }

  .kpi {
    background: #EEEEEE;
    border: 1px solid #CCCCCC;
    border-radius: 0; /* Minimal design per templates usually implies no border-radius or standard, spec didn't specify radius but said #EEEEEE background, #CCCCCC border */
    padding: 28px 32px;
    flex: 1;
    text-align: center;
    color: #000000;
  }

  .kpi .kpi-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 44px;
    font-weight: 700;
    margin: 8px 0 4px;
  }

  .kpi .kpi-desc {
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    color: #000000;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13pt;
    margin-top: 16px;
  }

  th {
    text-align: right;
    padding: 10px 14px;
    font-weight: 600;
    color: #000000;
    border: 1px solid #000000;
    font-size: 14px;
    text-transform: none;
    letter-spacing: normal;
    background: transparent;
  }

  th:first-child { text-align: left; }

  td {
    padding: 10px 14px;
    text-align: right;
    border: 1px solid #000000;
    font-variant-numeric: tabular-nums;
    font-weight: 400;
    color: #000000;
  }

  td:first-child { text-align: left; font-weight: 500; }

  tr.total-row td {
    border-top: 2px solid #000000;
    border-bottom: 2px solid #000000;
    font-weight: 700;
    background: transparent;
  }

  .bar-group { margin-bottom: 28px; }
  .bar-group-label { 
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px; 
    font-weight: 700; 
    margin-bottom: 10px; 
  }

  .bar-row {
    display: flex;
    align-items: center;
    margin: 6px 0;
    gap: 12px;
  }

  .bar-row-label {
    width: 110px;
    font-family: 'Barlow', sans-serif;
    font-size: 14px;
    color: #000000;
    text-align: right;
    flex-shrink: 0;
    font-weight: 500;
  }

  .bar-track {
    flex: 1;
    height: 36px;
    background: transparent;
    border-radius: 0;
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: 0;
    display: flex;
    align-items: center;
    padding-left: 14px;
    font-size: 15px;
    font-weight: 600;
    color: #FFFFFF;
  }

  .bar-moba { background: var(--accent); }
  .bar-publift { background: var(--blue); }
  .bar-publift-net { background: rgba(120,144,156,0.45); }

  .callout {
    background: #EEEEEE;
    border: none;
    border-left: 4px solid var(--accent);
    border-radius: 0;
    padding: 24px 32px;
    margin-top: 20px;
  }

  .callout-orange { border-left-color: var(--orange); }
  .callout-green { border-left-color: var(--green); }
  .callout-blue { border-left-color: var(--accent); }

  .callout h3 { color: #000000 !important; }

  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }

  .phase-list { list-style: none; margin-top: 16px; }

  .phase-list li {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 20px;
    font-size: 13pt;
    line-height: 1.5;
  }

  .phase-num {
    flex-shrink: 0;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--dark-bar);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 16px;
  }

  .method-list {
    list-style: none;
    margin-top: 8px;
  }

  .method-list li {
    font-size: 13pt;
    line-height: 1.6;
    padding: 6px 0;
    padding-left: 20px;
    position: relative;
    color: var(--text);
  }

  .method-list li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 14px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--dark-bar);
  }

  .nav-hint {
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'Barlow', sans-serif;
    font-size: 12px;
    color: var(--text-muted);
    pointer-events: none;
    z-index: 20;
  }
</style>"""

new_content = re.sub(r'<style>.*?</style>', new_style, content, flags=re.DOTALL)

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/prebid-slides.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
