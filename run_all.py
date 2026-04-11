import re

def process():
    with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    def make_funnel(partner, default_active, stages):
        cards_html = ""
        svg_paths = ""
        percents_html = ""
        
        n = len(stages)
        width_per_stage = 1000 / n
        
        for i, stg in enumerate(stages):
            id_val = stg['id']
            label = stg['label']
            val = stg['val']
            active = " active" if id_val == default_active else ""
            
            cards_html += f'''
        <div id="card-{partner}-{id_val}" class="funnel-stage-card{active}" onclick="selectFunnelStage('{partner}', '{id_val}')">
            <div class="funnel-stage-label">{label}</div>
            <div class="funnel-stage-value">{val}</div>
            <div class="funnel-stage-explore">Explore ▸</div>
        </div>'''

            if i < n - 1:
                pct = stg['conv']
                left_pct = (i + 1) * (100 / n)
                percents_html += f'''
            <div class="funnel-percentage" style="left: {left_pct}%;">{pct}</div>'''

        if n == 3:
            path_d = "M 166 0 C 333 0, 333 20, 500 20 C 666 20, 666 40, 833 40 L 833 100 C 666 100, 666 80, 500 80 C 333 80, 333 100, 166 100 Z"
        elif n == 4:
            path_d = "M 125 0 C 250 0, 250 15, 375 15 C 500 15, 500 30, 625 30 C 750 30, 750 45, 875 45 L 875 100 C 750 100, 750 85, 625 85 C 500 85, 500 70, 375 70 C 250 70, 250 100, 125 100 Z"
        elif n == 5:
            path_d = "M 100 0 C 200 0, 200 12, 300 12 C 400 12, 400 25, 500 25 C 600 25, 600 38, 700 38 C 800 38, 800 50, 900 50 L 900 100 C 800 100, 800 88, 700 88 C 600 88, 600 75, 500 75 C 400 75, 400 62, 300 62 C 200 62, 200 100, 100 100 Z"

        return f'''<div class="funnel-container">
    <div class="funnel-stages">{cards_html}
    </div>
    <div class="funnel-flow">
        <svg viewBox="0 0 1000 100" preserveAspectRatio="none">
            <defs>
                <linearGradient id="flow-gradient-{partner}" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#93c5fd" stop-opacity="0.8"/>
                </linearGradient>
            </defs>
            <path d="{path_d}" fill="url(#flow-gradient-{partner})"/>
        </svg>
        <div class="funnel-percentages">{percents_html}
        </div>
    </div>
</div>'''

    def get_enrichment(partner, default_active, stages, orig_enrichment):
        html = ""
        for stg in stages:
            id_val = stg['id']
            label = stg['label']
            display = "block" if id_val == default_active else "none"
            act_cls = " active" if id_val == default_active else ""
            
            if id_val == default_active:
                inner = orig_enrichment
            else:
                inner = f'''
                    <div style="text-align: center; padding: 4rem 2rem; background: var(--surface); border: 1px dashed var(--border); border-radius: var(--radius-md); margin-bottom: 2rem;">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 1rem; opacity: 0.5;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                        <h3 style="font-size: 1.1rem; color: var(--text); margin-bottom: 0.5rem;">Stage Enrichment — Coming Soon</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; max-width: 400px; margin: 0 auto;">Run BQ query to populate enrichment data for {label} users</p>
                    </div>'''
            
            html += f'''
            <div id="enrichment-{partner}-{id_val}" class="enrichment-section{act_cls}" style="display: {display};">
                {inner}
            </div>'''
        return html

    def replace_tab(content, partner, stages, default_active):
        # find funnel div block to replace
        pattern = r'<div style="display: flex; flex-direction: column; align-items: center; gap: 0; max-width: 700px; margin: 0 auto;">.*?</svg>.*?<span>.*? conversion</span>.*?</div>.*?</div>.*?<div style="max-width: 700px; margin: 2rem auto 0;">.*?<table style="width: 100%; border-collapse: collapse; font-size: 0\.9rem;">.*?</tbody>\s*</table>\s*</div>'
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
            funnel_html = make_funnel(partner, default_active, stages)
            content = content[:match.start()] + funnel_html + content[match.end():]
        
        # update enrichment title
        title_pattern = r'<h2 class="section-title" style="margin-top: 2\.5rem;">BOFU Enrichment — (.*?) User Profile</h2>'
        content = re.sub(title_pattern, f'<h2 id="enrichment-title-{partner}" class="section-title" style="margin-top: 2.5rem;">Stage Enrichment — {default_active.upper()} User Profile</h2>', content)
        
        # find enrichment section body and wrap it
        enrichment_start_pattern = r'<div class="kpi-grid" style="grid-template-columns: repeat\(4, 1fr\);">'
        start_match = re.search(enrichment_start_pattern, content)
        if start_match:
            # We assume enrichment data goes until the end of tab content
            # Wait, better to let the manual process do the enrichment wrap.
            pass
        
        return content

    # Skipping full automation for safety, this requires careful string slicing
    pass

process()
