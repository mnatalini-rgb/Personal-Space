import re

def process_html():
    with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    def replacer_combined(match):
        old_block = match.group(0)
        return """<div class="funnel-container">
    <div class="funnel-stages">
        <div id="card-combined-ebu" class="funnel-stage-card" onclick="selectFunnelStage('combined', 'ebu')">
            <div class="funnel-stage-label">EBU</div>
            <div class="funnel-stage-value">2,602,164</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-combined-al" class="funnel-stage-card" onclick="selectFunnelStage('combined', 'al')">
            <div class="funnel-stage-label">AL</div>
            <div class="funnel-stage-value">41,211</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-combined-c2" class="funnel-stage-card active" onclick="selectFunnelStage('combined', 'c2')">
            <div class="funnel-stage-label">C2</div>
            <div class="funnel-stage-value">20,989</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
    </div>
    <div class="funnel-flow">
        <svg viewBox="0 0 1000 100" preserveAspectRatio="none">
            <defs>
                <linearGradient id="flow-gradient-comb" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#93c5fd" stop-opacity="0.8"/>
                </linearGradient>
            </defs>
            <path d="M 166 0 C 333 0, 333 20, 500 20 C 666 20, 666 40, 833 40 L 833 100 C 666 100, 666 80, 500 80 C 333 80, 333 100, 166 100 Z" fill="url(#flow-gradient-comb)"/>
        </svg>
        <div class="funnel-percentages">
            <div class="funnel-percentage" style="left: 33.33%;">1.6%</div>
            <div class="funnel-percentage" style="left: 66.66%;">50.9%</div>
        </div>
    </div>
</div>"""

    pattern_combined = re.compile(r'<div style="display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto;">.*?</svg>\n                            <span>50\.9% conversion</span>\n                        </div>\n\n                        <div style="width: 42%; background: #8b5cf6; color: #fff; border-radius: 0 0 var\(--radius-md\) var\(--radius-md\); padding: 1\.1rem 1\.5rem; text-align: center;">\n                            <div style="font-size: 0\.8rem; text-transform: uppercase; letter-spacing: 0\.08em; opacity: 0\.85; margin-bottom: 0\.25rem;">C2 — Second Conversion</div>\n                            <div style="font-size: 2rem; font-weight: 700;">20,989</div>\n                        </div>\n                    </div>\n\n                    <div style="max-width: 700px; margin: 2rem auto 0;">\n                        <table style="width: 100%; border-collapse: collapse; font-size: 0\.9rem;">.*?</tbody>\n                        </table>\n                    </div>', re.DOTALL)
    
    html = pattern_combined.sub(replacer_combined, html)

    with open('nsm-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)

process_html()
