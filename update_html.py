import re

def update_file():
    with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add CSS
    css = """
        /* New Horizontal Funnel Styles */
        .funnel-container { width: 100%; margin: 2rem 0; position: relative; }
        .funnel-stages { display: flex; justify-content: space-between; align-items: stretch; position: relative; z-index: 2; gap: 1rem; }
        .funnel-stage-card { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 1.2rem; text-align: center; cursor: pointer; transition: all 0.2s ease; box-shadow: var(--shadow); display: flex; flex-direction: column; justify-content: center; position: relative; }
        .funnel-stage-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover); }
        .funnel-stage-card.active { background: var(--accent); color: #fff; border-color: var(--accent); }
        .funnel-stage-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; opacity: 0.85; font-weight: 600; }
        .funnel-stage-card.active .funnel-stage-label { color: rgba(255, 255, 255, 0.9); }
        .funnel-stage-card:not(.active) .funnel-stage-label { color: var(--text-muted); }
        .funnel-stage-value { font-size: 1.75rem; font-weight: 700; }
        .funnel-stage-explore { font-size: 0.75rem; font-weight: 600; margin-top: 0.75rem; opacity: 0; height: 0; overflow: hidden; transition: opacity 0.2s ease; }
        .funnel-stage-card.active .funnel-stage-explore { opacity: 1; height: auto; color: #fff; margin-top: 0.75rem; }
        .funnel-flow { position: relative; width: 100%; height: 120px; margin-top: -10px; z-index: 1; }
        .funnel-flow svg { width: 100%; height: 100%; display: block; }
        .funnel-percentages { position: absolute; top: 50%; transform: translateY(-50%); left: 0; width: 100%; display: flex; padding: 0; pointer-events: none; }
        .funnel-percentage { background: var(--surface); color: var(--accent); font-weight: 700; font-size: 0.85rem; padding: 0.2rem 0.6rem; border-radius: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); position: absolute; transform: translate(-50%, -50%); border: 1px solid rgba(37,99,235,0.2); }
        .enrichment-section { display: none; }
        .enrichment-section.active { display: block; }
"""
    if '/* New Horizontal Funnel Styles */' not in content:
        content = content.replace('</style>', css + '\n    </style>')

    # 2. Add JS
    js = """
    function selectFunnelStage(partner, stageId) {
        // Reset all cards in this partner's funnel
        var cards = document.querySelectorAll('#' + partner + '-tab-funnel .funnel-stage-card');
        for (var i = 0; i < cards.length; i++) {
            cards[i].classList.remove('active');
        }
        
        // Set clicked card as active
        var activeCard = document.getElementById('card-' + partner + '-' + stageId);
        if (activeCard) {
            activeCard.classList.add('active');
        }
        
        // Hide all enrichment sections for this partner
        var sections = document.querySelectorAll('#' + partner + '-tab-funnel .enrichment-section');
        for (var j = 0; j < sections.j; j++) {
            sections[j].classList.remove('active');
            sections[j].style.display = 'none';
        }
        
        // Show the selected enrichment section
        var activeSection = document.getElementById('enrichment-' + partner + '-' + stageId);
        if (activeSection) {
            activeSection.classList.add('active');
            activeSection.style.display = 'block';
        }
        
        // Update section title
        var titleEl = document.getElementById('enrichment-title-' + partner);
        if (titleEl) {
            var stageName = stageId.toUpperCase();
            titleEl.innerText = 'Stage Enrichment — ' + stageName + ' User Profile';
        }
    }
"""
    if 'function selectFunnelStage' not in content:
        content = content.replace('</script>\n</body>', js + '\n    </script>\n</body>')

    with open('nsm-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

update_file()
