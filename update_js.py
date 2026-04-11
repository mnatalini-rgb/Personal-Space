import re

def update_file():
    with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    js = """
    function selectFunnelStage(partner, stageId) {
        var cards = document.querySelectorAll('#' + partner + '-tab-funnel .funnel-stage-card');
        for (var i = 0; i < cards.length; i++) {
            cards[i].classList.remove('active');
        }
        
        var activeCard = document.getElementById('card-' + partner + '-' + stageId);
        if (activeCard) {
            activeCard.classList.add('active');
        }
        
        var sections = document.querySelectorAll('#' + partner + '-tab-funnel .enrichment-section');
        for (var j = 0; j < sections.length; j++) {
            sections[j].classList.remove('active');
            sections[j].style.display = 'none';
        }
        
        var activeSection = document.getElementById('enrichment-' + partner + '-' + stageId);
        if (activeSection) {
            activeSection.classList.add('active');
            activeSection.style.display = 'block';
        }
        
        var titleEl = document.getElementById('enrichment-title-' + partner);
        if (titleEl) {
            var stageName = stageId.toUpperCase();
            titleEl.innerText = 'Stage Enrichment — ' + stageName + ' User Profile';
        }
    }
"""
    if 'function selectFunnelStage' in content:
        content = re.sub(r'function selectFunnelStage.*?}\n', js, content, flags=re.DOTALL)
    else:
        content = content.replace('</script>\n</body>', js + '\n</script>\n</body>')

    with open('nsm-dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

update_file()
