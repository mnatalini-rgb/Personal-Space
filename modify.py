import re

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/tradeit-nsm-dashboard.html', 'r') as f:
    content = f.read()

# 1. Styles
content = content.replace(
    '.show-all-btn:hover {\n            border-color: var(--accent);\n            color: var(--accent);\n        }\n    </style>',
    '.show-all-btn:hover {\n            border-color: var(--accent);\n            color: var(--accent);\n        }\n\n        .term {\n            border-bottom: 1px dotted var(--text-muted);\n            cursor: help;\n            position: relative;\n        }\n        .term:hover::after {\n            content: attr(data-tip);\n            position: absolute;\n            bottom: 100%;\n            left: 50%;\n            transform: translateX(-50%);\n            background: var(--surface);\n            border: 1px solid var(--border);\n            color: var(--text);\n            padding: 0.3rem 0.6rem;\n            border-radius: 6px;\n            font-size: 0.75rem;\n            white-space: nowrap;\n            z-index: 20;\n            box-shadow: 0 4px 12px rgba(0,0,0,0.4);\n        }\n    </style>'
)

# 2. Header
header_old = """        <header class="header">
            <span class="badge">FOR INTERNAL USE</span>
            <h1>Tradeit — Brand Integration Performance</h1>
            <h2>NSM Analysis: Jan–Feb 2026 | € Value per Conversion</h2>
            <p>Primary metric: € per 1K EBU (replaces deprecated OVU formula)</p>
        </header>"""

header_new = """        <header class="header">
            <span class="badge">FOR INTERNAL USE</span>
            <h1>Tradeit — Brand Integration Performance</h1>
            <h2>NSM Analysis: Jan–Feb 2026 | € Value per Conversion</h2>
            <p>Primary metric: € per 1K EBU</p>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.25rem;"><span class="term" data-tip="Eligible Brand Integration Users">EBU</span> = Eligible Brand Integration Users — the total audience pool eligible for a partner's missions in a given period.</p>
        </header>"""
content = content.replace(header_old, header_new)

# 3. KPI Tooltips
content = content.replace(
    '<div class="kpi-sub">€19/1K EBU | 591K EBU</div>',
    '<div class="kpi-sub">€19/1K <span class="term" data-tip="Eligible Brand Integration Users">EBU</span> | 591K <span class="term" data-tip="Eligible Brand Integration Users">EBU</span></div>'
)
content = content.replace(
    '<div class="kpi-sub">€21/1K EBU | 601K EBU</div>',
    '<div class="kpi-sub">€21/1K <span class="term" data-tip="Eligible Brand Integration Users">EBU</span> | 601K <span class="term" data-tip="Eligible Brand Integration Users">EBU</span></div>'
)

# 4. Sections 2-6 renaming and Trend insert
# Split at section 2
parts = content.split('<div class="section" id="section-2">')

trend_section = """<div class="section" id="section-2">
            <h2 class="section-title">2. NSM Trend</h2>
            <p style="margin-bottom: 1.5rem; color: var(--text-muted); font-size: 0.9rem;">
                Apr–Dec 2025 values are estimates derived from CDP unique user counts × € per conversion. Jan–Feb 2026 use actual mission data.
            </p>
            <div class="chart-container">
                <canvas id="nsmTrendChart"></canvas>
            </div>
        </div>

        <div class="section" id="section-3">"""

content = parts[0] + trend_section + parts[1]

# Rename existing 3 to 4, 4 to 5, 5 to 6
content = content.replace('<div class="section" id="section-3">', '<div class="section" id="section-4">')
content = content.replace('<h2 class="section-title">3. Month-over-Month Comparison</h2>', '<h2 class="section-title">4. Month-over-Month Comparison</h2>')

content = content.replace('<div class="section" id="section-4">', '<div class="section" id="section-5">')
content = content.replace('<h2 class="section-title">4. NA A/B Test (January)</h2>', '<h2 class="section-title">5. NA A/B Test (January)</h2>')

content = content.replace('<div class="section" id="section-5">', '<div class="section" id="section-6">')
content = content.replace('<h2 class="section-title">5. Segment Performance (€/1K EBU)</h2>', '<h2 class="section-title">6. Segment Performance (€/1K EBU)</h2>')

# A/B Test Tooltips
content = content.replace('<span>AL Rate</span>', '<span><span class="term" data-tip="Account Linkage — €0.38">AL</span> Rate</span>')
content = content.replace('<span>C1 Rate</span>', '<span><span class="term" data-tip="First Trade — €0.04">C1</span> Rate</span>')
content = content.replace('<span>C2 Rate</span>', '<span><span class="term" data-tip="Trade $250+ — €8.75">C2</span> Rate</span>')

# Segment Performance Tooltips
content = content.replace('<th class="number">TOFU</th>', '<th class="number"><span class="term" data-tip="Top of Funnel — new/unactivated users">TOFU</span></th>')
content = content.replace('<th class="number">MOFU</th>', '<th class="number"><span class="term" data-tip="Middle of Funnel — linked, no trade yet">MOFU</span></th>')
content = content.replace('<th class="number">BOFU</th>', '<th class="number"><span class="term" data-tip="Bottom of Funnel — linked + has traded">BOFU</span></th>')

# 5. Extract Section 6 (Value Breakdown), Section 7 (Funnel) to reorder and add new Section 7 (Funnel Explainer)
import re
# Find where Section 6 starts
sec6_start = content.find('<div class="section" id="section-6">') # This is the old section 6, but we already replaced section-5 to section-6!
# Wait, let's fix the extraction by matching the title.
content = content.replace('<div class="section" id="section-6">\n            <h2 class="section-title">6. Value Breakdown', '<div class="section" id="section-X_TEMP">\n            <h2 class="section-title">9. Value Breakdown')

content = content.replace('<div class="section" id="section-7">\n            <h2 class="section-title">7. Funnel Conversion Rates', '<div class="section" id="section-8">\n            <h2 class="section-title">8. Funnel Conversion Rates')

# Key Insights
content = content.replace('<div class="section" id="section-8">\n            <h2 class="section-title">8. Key Insights', '<div class="section" id="section-10">\n            <h2 class="section-title">10. Key Insights')

# Extract the Value Breakdown section (now marked as X_TEMP)
# Extract the Funnel Conversion section (now marked as 8)
pattern_temp = r'(<div class="section" id="section-X_TEMP">.*?</div>\s*</div>)'
match_temp = re.search(pattern_temp, content, re.DOTALL)
if match_temp:
    val_breakdown_html = match_temp.group(1)
    content = content.replace(val_breakdown_html, '')
    # Fix ID
    val_breakdown_html = val_breakdown_html.replace('id="section-X_TEMP"', 'id="section-9"')
    
    # We will insert it AFTER section 8
    # But wait, we need to insert the Funnel Explainer (Section 7) BEFORE section 8
    
    funnel_explainer = """<div class="section" id="section-7">
            <h2 class="section-title">7. Tradeit Conversion Funnel</h2>
            <div class="insight-card" style="padding: 2rem; background-color: var(--bg); border: 1px solid var(--border); border-left: 4px solid var(--accent);">
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem; text-align: center;">
                    <div style="flex: 1;">
                        <div style="font-size: 1.25rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem;"><span class="term" data-tip="Eligible Brand Integration Users">EBU</span></div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">Total Eligible</div>
                    </div>
                    <div style="color: var(--accent); font-size: 1.5rem;">→</div>
                    <div style="flex: 1;">
                        <div style="font-size: 1.25rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem;"><span class="term" data-tip="Account Linkage — €0.38">AL</span></div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">Account Linkage (€0.38)</div>
                    </div>
                    <div style="color: var(--accent); font-size: 1.5rem;">→</div>
                    <div style="flex: 1;">
                        <div style="font-size: 1.25rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem;"><span class="term" data-tip="First Trade — €0.04">C1</span></div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">First Trade (€0.04)</div>
                    </div>
                    <div style="color: var(--accent); font-size: 1.5rem;">→</div>
                    <div style="flex: 1;">
                        <div style="font-size: 1.25rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem;"><span class="term" data-tip="Trade $250+ — €8.75">C2</span></div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">Trade $250+ (€8.75)</div>
                    </div>
                </div>
            </div>
        </div>\n\n        """
    
    # Let's find Section 8 and put Explainer before it, and Breakdown after it.
    parts8 = content.split('<div class="section" id="section-8">')
    
    # We need to find the end of section 8 to insert section 9
    sec8_content = parts8[1]
    # find next <div class="section"
    sec8_end_idx = sec8_content.find('<div class="section"')
    if sec8_end_idx == -1:
        # fallback
        sec8_end_idx = sec8_content.find('<div class="footer">')
    
    sec8_block = sec8_content[:sec8_end_idx]
    rest_of_file = sec8_content[sec8_end_idx:]
    
    content = parts8[0] + funnel_explainer + '<div class="section" id="section-8">' + sec8_block + val_breakdown_html + "\n\n        " + rest_of_file

# Funnel Table tooltips
content = content.replace('<th class="number">TOFU AL%</th>', '<th class="number"><span class="term" data-tip="Top of Funnel — new/unactivated users">TOFU</span> <span class="term" data-tip="Account Linkage — €0.38">AL</span>%</th>')
content = content.replace('<th class="number">TOFU C1%</th>', '<th class="number"><span class="term" data-tip="Top of Funnel — new/unactivated users">TOFU</span> <span class="term" data-tip="First Trade — €0.04">C1</span>%</th>')
content = content.replace('<th class="number">MOFU C1%</th>', '<th class="number"><span class="term" data-tip="Middle of Funnel — linked, no trade yet">MOFU</span> <span class="term" data-tip="First Trade — €0.04">C1</span>%</th>')
content = content.replace('<th class="number">BOFU C2%</th>', '<th class="number"><span class="term" data-tip="Bottom of Funnel — linked + has traded">BOFU</span> <span class="term" data-tip="Trade $250+ — €8.75">C2</span>%</th>')

# Insights Tooltips
content = content.replace('<h3>1. C2 Dominates Value</h3>', '<h3>1. <span class="term" data-tip="Trade $250+ — €8.75">C2</span> Dominates Value</h3>')
content = content.replace('The C2 conversion', 'The <span class="term" data-tip="Trade $250+ — €8.75">C2</span> conversion')

content = content.replace('EBU audience', '<span class="term" data-tip="Eligible Brand Integration Users">EBU</span> audience')
content = content.replace('low AL rate', 'low <span class="term" data-tip="Account Linkage — €0.38">AL</span> rate')

content = content.replace('1K EBU declined', '1K <span class="term" data-tip="Eligible Brand Integration Users">EBU</span> declined')

content = content.replace('<h3>4. BOFU is the C2 Engine</h3>', '<h3>4. <span class="term" data-tip="Bottom of Funnel — linked + has traded">BOFU</span> is the <span class="term" data-tip="Trade $250+ — €8.75">C2</span> Engine</h3>')
content = content.replace('The BOFU segment', 'The <span class="term" data-tip="Bottom of Funnel — linked + has traded">BOFU</span> segment')
content = content.replace('1K EBU by far', '1K <span class="term" data-tip="Eligible Brand Integration Users">EBU</span> by far')
content = content.replace('pure C2 generation', 'pure <span class="term" data-tip="Trade $250+ — €8.75">C2</span> generation')


# Now append the Trend Chart JS
js_insert = """
        // NSM Trend Calculation
        const trendLabels = ['Apr 25', 'May 25', 'Jun 25', 'Jul 25', 'Aug 25', 'Sep 25', 'Oct 25', 'Nov 25', 'Dec 25', 'Jan 26', 'Feb 26'];
        
        const estValues = [];
        const actualValues = [];
        const ebuLineData = [];
        
        for (let i = 11; i >= 3; i--) {
            const tradeit = cdpData[0].data[i];
            const trade = cdpData[2].data[i];
            const trade250 = cdpData[4].data[i];
            
            const estVal = (tradeit * 0.38) + (trade * 0.04) + (trade250 * 8.75);
            estValues.push(estVal);
            actualValues.push(null);
            ebuLineData.push(null);
        }
        
        // Jan 26
        estValues.push(null);
        actualValues.push(11343);
        ebuLineData.push(19);
        
        // Feb 26
        estValues.push(null);
        actualValues.push(12566);
        ebuLineData.push(21);
        
        const ctxNsmTrend = document.getElementById('nsmTrendChart').getContext('2d');
        new Chart(ctxNsmTrend, {
            type: 'bar',
            data: {
                labels: trendLabels,
                datasets: [
                    {
                        type: 'line',
                        label: '€/1K EBU',
                        data: ebuLineData,
                        borderColor: '#22c55e',
                        backgroundColor: '#22c55e',
                        borderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8,
                        showLine: false,
                        yAxisID: 'y1',
                        order: 1
                    },
                    {
                        type: 'bar',
                        label: 'Estimated € Value (CDP)',
                        data: estValues,
                        backgroundColor: 'rgba(255, 85, 0, 0.4)',
                        borderRadius: 4,
                        order: 2
                    },
                    {
                        type: 'bar',
                        label: 'Actual € Value (Missions)',
                        data: actualValues,
                        backgroundColor: '#ff5500',
                        borderRadius: 4,
                        order: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#d4d6dd' }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) label += ': ';
                                if (context.datasetIndex === 0) {
                                    if (context.parsed.y !== null) {
                                        return label + '€' + context.parsed.y;
                                    }
                                    return null;
                                }
                                if (context.parsed.y !== null) {
                                    label += '€' + context.parsed.y.toLocaleString('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0});
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#d4d6dd' },
                        stacked: true
                    },
                    y: {
                        grid: { color: gridColor },
                        ticks: { 
                            color: '#d4d6dd',
                            callback: value => '€' + value.toLocaleString('en-US')
                        },
                        stacked: true,
                        beginAtZero: true
                    },
                    y1: {
                        position: 'right',
                        grid: { display: false },
                        ticks: {
                            color: '#22c55e',
                            callback: value => '€' + value
                        },
                        min: 0,
                        max: 60
                    }
                }
            }
        });
"""

content = content.replace('// Format number with commas', js_insert + '\n        // Format number with commas')

with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/tradeit-nsm-dashboard.html', 'w') as f:
    f.write(content)
