import re

with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Tab 1: Combined
old_comb = r'<div style="display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto;">.*?<table style="width: 100%; border-collapse: collapse; font-size: 0\.9rem;">.*?</tbody>\s*</table>\s*</div>'
new_comb = """<div class="funnel-container">
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
text = re.sub(old_comb, new_comb, text, flags=re.DOTALL, count=1)

# Tab 2: Tradeit
old_trade = r'<div style="display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto;">.*?<table style="width: 100%; border-collapse: collapse; font-size: 0\.9rem;">.*?</tbody>\s*</table>\s*</div>'
new_trade = """<div class="funnel-container">
    <div class="funnel-stages">
        <div id="card-tradeit-ebu" class="funnel-stage-card" onclick="selectFunnelStage('tradeit', 'ebu')">
            <div class="funnel-stage-label">EBU</div>
            <div class="funnel-stage-value">1,809,569</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-tradeit-al" class="funnel-stage-card" onclick="selectFunnelStage('tradeit', 'al')">
            <div class="funnel-stage-label">AL</div>
            <div class="funnel-stage-value">28,226</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-tradeit-c2" class="funnel-stage-card active" onclick="selectFunnelStage('tradeit', 'c2')">
            <div class="funnel-stage-label">C2</div>
            <div class="funnel-stage-value">11,133</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
    </div>
    <div class="funnel-flow">
        <svg viewBox="0 0 1000 100" preserveAspectRatio="none">
            <defs>
                <linearGradient id="flow-gradient-trade" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#93c5fd" stop-opacity="0.8"/>
                </linearGradient>
            </defs>
            <path d="M 166 0 C 333 0, 333 20, 500 20 C 666 20, 666 40, 833 40 L 833 100 C 666 100, 666 80, 500 80 C 333 80, 333 100, 166 100 Z" fill="url(#flow-gradient-trade)"/>
        </svg>
        <div class="funnel-percentages">
            <div class="funnel-percentage" style="left: 33.33%;">1.6%</div>
            <div class="funnel-percentage" style="left: 66.66%;">39.5%</div>
        </div>
    </div>
</div>"""
text = re.sub(old_trade, new_trade, text, flags=re.DOTALL, count=1)

# Tab 3: Winline
old_win = r'<div style="display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto;">.*?<table style="width: 100%; border-collapse: collapse; font-size: 0\.9rem;">.*?</tbody>\s*</table>\s*</div>'
new_win = """<div class="funnel-container">
    <div class="funnel-stages">
        <div id="card-winline-ebu" class="funnel-stage-card" onclick="selectFunnelStage('winline', 'ebu')">
            <div class="funnel-stage-label">EBU</div>
            <div class="funnel-stage-value">685,181</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-winline-al" class="funnel-stage-card" onclick="selectFunnelStage('winline', 'al')">
            <div class="funnel-stage-label">AL</div>
            <div class="funnel-stage-value">15,308</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-winline-kyc" class="funnel-stage-card" onclick="selectFunnelStage('winline', 'kyc')">
            <div class="funnel-stage-label">KYC</div>
            <div class="funnel-stage-value">1,021</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-winline-ftd" class="funnel-stage-card" onclick="selectFunnelStage('winline', 'ftd')">
            <div class="funnel-stage-label">FTD</div>
            <div class="funnel-stage-value">561</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-winline-bet" class="funnel-stage-card active" onclick="selectFunnelStage('winline', 'bet')">
            <div class="funnel-stage-label">BET</div>
            <div class="funnel-stage-value">10,499</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
    </div>
    <div class="funnel-flow">
        <svg viewBox="0 0 1000 100" preserveAspectRatio="none">
            <defs>
                <linearGradient id="flow-gradient-win" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#93c5fd" stop-opacity="0.8"/>
                </linearGradient>
            </defs>
            <path d="M 100 0 C 200 0, 200 12, 300 12 C 400 12, 400 25, 500 25 C 600 25, 600 38, 700 38 C 800 38, 800 50, 900 50 L 900 100 C 800 100, 800 88, 700 88 C 600 88, 600 75, 500 75 C 400 75, 400 62, 300 62 C 200 62, 200 100, 100 100 Z" fill="url(#flow-gradient-win)"/>
        </svg>
        <div class="funnel-percentages">
            <div class="funnel-percentage" style="left: 20%;">2.2%</div>
            <div class="funnel-percentage" style="left: 40%;">6.7%</div>
            <div class="funnel-percentage" style="left: 60%;">54.9%</div>
            <div class="funnel-percentage" style="left: 80%;">N/A</div>
        </div>
    </div>
</div>"""
text = re.sub(old_win, new_win, text, flags=re.DOTALL, count=1)

# Tab 4: WhiteMarket
old_white = r'<div style="display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto;">.*?<table style="width: 100%; border-collapse: collapse; font-size: 0\.9rem;">.*?</tbody>\s*</table>\s*</div>'
new_white = """<div class="funnel-container">
    <div class="funnel-stages">
        <div id="card-whitemarket-ebu" class="funnel-stage-card" onclick="selectFunnelStage('whitemarket', 'ebu')">
            <div class="funnel-stage-label">EBU</div>
            <div class="funnel-stage-value">116,533</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-whitemarket-al" class="funnel-stage-card" onclick="selectFunnelStage('whitemarket', 'al')">
            <div class="funnel-stage-label">AL</div>
            <div class="funnel-stage-value">649</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-whitemarket-c2" class="funnel-stage-card active" onclick="selectFunnelStage('whitemarket', 'c2')">
            <div class="funnel-stage-label">C2</div>
            <div class="funnel-stage-value">189</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
        <div id="card-whitemarket-c3" class="funnel-stage-card" onclick="selectFunnelStage('whitemarket', 'c3')">
            <div class="funnel-stage-label">C3</div>
            <div class="funnel-stage-value">651</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>
    </div>
    <div class="funnel-flow">
        <svg viewBox="0 0 1000 100" preserveAspectRatio="none">
            <defs>
                <linearGradient id="flow-gradient-white" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#93c5fd" stop-opacity="0.8"/>
                </linearGradient>
            </defs>
            <path d="M 125 0 C 250 0, 250 15, 375 15 C 500 15, 500 30, 625 30 C 750 30, 750 45, 875 45 L 875 100 C 750 100, 750 85, 625 85 C 500 85, 500 70, 375 70 C 250 70, 250 100, 125 100 Z" fill="url(#flow-gradient-white)"/>
        </svg>
        <div class="funnel-percentages">
            <div class="funnel-percentage" style="left: 25%;">0.56%</div>
            <div class="funnel-percentage" style="left: 50%;">29.1%</div>
            <div class="funnel-percentage" style="left: 75%;">N/A</div>
        </div>
    </div>
</div>"""
text = re.sub(old_white, new_white, text, flags=re.DOTALL, count=1)

with open('nsm-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

