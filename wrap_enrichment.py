import re

with open('nsm-dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

def wrap_enrichment(partner, default_stage, other_stages):
    global text
    
    pat_title = r'<h2 class="section-title" style="margin-top: 2\.5rem;">BOFU Enrichment — (.*?) User Profile</h2>'
    new_title = f'<h2 id="enrichment-title-{partner}" class="section-title" style="margin-top: 2.5rem;">Stage Enrichment — {default_stage.upper()} User Profile</h2>'
    text = text.replace(f'<h2 class="section-title" style="margin-top: 2.5rem;">BOFU Enrichment — {default_stage.upper()} User Profile</h2>', new_title)
    
    grid_start = '<div class="kpi-grid" style="grid-template-columns: repeat(4, 1fr);">'
    
    placeholders = ""
    for stg in other_stages:
        placeholders += f'''
        <div id="enrichment-{partner}-{stg}" class="enrichment-section" style="display: none;">
            <div style="text-align: center; padding: 4rem 2rem; background: var(--surface); border: 1px dashed var(--border); border-radius: var(--radius-md); margin-bottom: 2rem;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 1rem; opacity: 0.5;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                <h3 style="font-size: 1.1rem; color: var(--text); margin-bottom: 0.5rem;">Stage Enrichment — Coming Soon</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; max-width: 400px; margin: 0 auto;">Run BQ query to populate enrichment data for {stg.upper()} users</p>
            </div>
        </div>
'''
    
    text = text.replace(grid_start, placeholders + f'\n        <div id="enrichment-{partner}-{default_stage}" class="enrichment-section active" style="display: block;">\n                    ' + grid_start)
    
    # We must also close the wrapper div at the end of the tab content.
    # Actually, each tab ends with `            </div>\n\n            <div id=` or just ends the file.
    # It's safer to just inject the closing tag right before the next tab starts, or before `<script>`.
    
    if partner == 'combined':
        text = text.replace('            </div>\n\n            <div id="tradeit-tab-funnel" class="tab-content" style="display: none;">', '            </div>\n        </div>\n\n            <div id="tradeit-tab-funnel" class="tab-content" style="display: none;">')
    elif partner == 'tradeit':
        text = text.replace('            </div>\n\n            <div id="winline-tab-funnel" class="tab-content" style="display: none;">', '            </div>\n        </div>\n\n            <div id="winline-tab-funnel" class="tab-content" style="display: none;">')
    elif partner == 'winline':
        text = text.replace('            </div>\n\n            <div id="whitemarket-tab-funnel" class="tab-content" style="display: none;">', '            </div>\n        </div>\n\n            <div id="whitemarket-tab-funnel" class="tab-content" style="display: none;">')
    elif partner == 'whitemarket':
        text = text.replace('            </div>\n\n        </div>\n    </div>\n    \n    <script>', '            </div>\n        </div>\n\n        </div>\n    </div>\n    \n    <script>')

wrap_enrichment('combined', 'c2', ['ebu', 'al'])
wrap_enrichment('tradeit', 'c2', ['ebu', 'al'])
wrap_enrichment('winline', 'bet', ['ebu', 'al', 'kyc', 'ftd'])
wrap_enrichment('whitemarket', 'c2', ['ebu', 'al', 'c3'])

with open('nsm-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

