import re

with open('analysis/nsm-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Round values in Missions tab
# Only replace in tradeit-tab-missions block
start_idx = content.find('<div id="tradeit-tab-missions"')
end_idx = content.find('<!-- WINLINE CONTAINER -->')

if start_idx != -1 and end_idx != -1:
    missions_block = content[start_idx:end_idx]
    
    # Decimal replacements mapping
    replacements = {
        '€12,255.38': '€12,255',
        '€13,444.16': '€13,444',
        '€68,719.48': '€68,719',
        '€591.67': '€592',
        '€620.05': '€620',
        '€126.58': '€127',
        '€2,038.75': '€2,039',
        '€3,417.53': '€3,418',
        '€177.14': '€177',
        '€2,940.00': '€2,940',
        '€429.25': '€429',
        '€28.61': '€29',
        '€507.50': '€508',
        '€736.51': '€737',
        '€90.54': '€91',
        '€551.25': '€551',
        '€1,355.37': '€1,355',
        '€99.97': '€100',
        '€1,566.25': '€1,566',
        '€4,784.64': '€4,785',
        '€183.38': '€183',
        '€3,036.25': '€3,036',
        '€399.76': '€400',
        '€2.20': '€2',
        '€621.25': '€621',
        '€780.27': '€780',
        '€54.82': '€55',
        '€560.00': '€560',
        '€38,794.76': '€38,795',
        '€4,066.61': '€4,067',
        '€17,771.22': '€17,771',
        '€2,183.36': '€2,183',
        '€1,108.18': '€1,108',
        '€1,067.23': '€1,067',
        '€1,120.68': '€1,121',
        '€286.36': '€286',
        '€22.54': '€23',
        '€437.50': '€438',
        '€20.66': '€21',
        '€236.25': '€236',
        '€1,443.75': '€1,444',
        '€20.38': '€20',
        '€140.00': '€140',
        '€6,534.67': '€6,535',
        '€8,004.27': '€8,004',
        '€19,501.33': '€19,501',
        '€3,377.05': '€3,377',
        '€3,021.59': '€3,022',
        '€1,568.22': '€1,568',
        '€965.36': '€965',
        '€1,023.21': '€1,023',
        '€1,324.14': '€1,324',
        '€1,378.30': '€1,378',
        '€1,395.09': '€1,395',
        '€1,281.06': '€1,281'
    }
    
    for old, new in replacements.items():
        missions_block = missions_block.replace(old, new)
        
    content = content[:start_idx] + missions_block + content[end_idx:]

# Round chart titles in JS
content = content.replace("January (€12,255.38)", "January (€12,255)")
content = content.replace("February (€13,444.16)", "February (€13,444)")

# Round chart arrays
content = content.replace("[null, 6534.67, null, 3377.05, 965.36, 1378.30]", "[null, 6535, null, 3377, 965, 1378]")
content = content.replace("[null, 8004.27, null, 3021.59, 1023.21, 1395.09]", "[null, 8004, null, 3022, 1023, 1395]")
content = content.replace("[38794.76, 19501.33, 2183.36, 1568.22, 1324.14, 1281.06]", "[38795, 19501, 2183, 1568, 1324, 1281]")

# 2. Add region filter UI
# Find section A end to insert filter UI
filter_html = """
                <div class="section region-filter-section" style="margin-top: 2rem; margin-bottom: 2rem;">
                    <div class="partner-selector" id="missionsRegionFilter" style="display: flex; gap: 0.5rem; background: var(--surface); padding: 0.5rem; border-radius: 8px; border: 1px solid var(--border); overflow-x: auto;">
                        <button class="partner-btn active" data-region="All Regions">All Regions</button>
                        <button class="partner-btn" data-region="EU">EU</button>
                        <button class="partner-btn" data-region="CIS">CIS</button>
                        <button class="partner-btn" data-region="LATAM">LATAM</button>
                        <button class="partner-btn" data-region="NA">NA</button>
                        <button class="partner-btn" data-region="MENA">MENA</button>
                        <button class="partner-btn" data-region="APAC">APAC</button>
                    </div>
                </div>
"""
content = content.replace('<div class="section">\n                    <h2 class="section-title">B. Regional Breakdown', filter_html + '\n                <div class="section">\n                    <h2 class="section-title">B. Regional Breakdown')

# Update Section B to have IDs for rows for easy filtering
# actually we can just rely on the text in the td. Let's do that via JS.

# 3. Add G. Weekly Performance section
weekly_section = """
                <div class="section" id="weekly-performance-section">
                    <h2 class="section-title">G. Weekly Performance Trend</h2>
                    <div class="insight-card" style="border: 2px dashed var(--border); background: rgba(21, 22, 24, 0.5); text-align: center; padding: 4rem 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1rem;">
                        <div style="font-size: 3rem; color: var(--text-muted); opacity: 0.5;">
                            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="18" y1="20" x2="18" y2="10"></line>
                                <line x1="12" y1="20" x2="12" y2="4"></line>
                                <line x1="6" y1="20" x2="6" y2="14"></line>
                            </svg>
                        </div>
                        <h3 style="color: var(--text-muted); font-size: 1.2rem; margin: 0;">Weekly breakdown data coming soon</h3>
                        <p style="color: var(--text-muted); margin: 0; max-width: 400px;">Upload weekly CSVs to populate this section with week-over-week € value trends, AL/C1/C2 progress, and regional shifts.</p>
                        
                        <!-- Wireframe placeholders -->
                        <div style="display: flex; gap: 1rem; width: 100%; max-width: 800px; margin-top: 2rem; opacity: 0.3;">
                            <div style="flex: 2; height: 150px; background: linear-gradient(180deg, var(--border) 0%, transparent 100%); border-radius: 4px; position: relative;">
                                <div style="position: absolute; bottom: 0; left: 10%; width: 80%; height: 2px; background: var(--accent);"></div>
                            </div>
                            <div style="flex: 3; display: flex; flex-direction: column; gap: 0.5rem;">
                                <div style="height: 20px; background: var(--border); border-radius: 2px; width: 100%;"></div>
                                <div style="height: 20px; background: var(--border); border-radius: 2px; width: 100%;"></div>
                                <div style="height: 20px; background: var(--border); border-radius: 2px; width: 80%;"></div>
                                <div style="height: 20px; background: var(--border); border-radius: 2px; width: 90%;"></div>
                            </div>
                        </div>
                    </div>
                </div>
"""
content = content.replace('<!-- WINLINE CONTAINER -->', weekly_section + '\n            <!-- WINLINE CONTAINER -->')

# 4. Add JS for region filter
# Inject JS near the end of body or inside the existing script.
filter_js = """
        // Missions Region Filter Logic
        const missionsData = [
            {month:'Jan', region:'NA', segment:'General (A)', al:1101, c1:176, c2:19, value:592},
            {month:'Jan', region:'NA', segment:'General (B)', al:1217, c1:221, c2:17, value:620},
            {month:'Jan', region:'NA', segment:'AL&NoTrade', al:0, c1:102, c2:14, value:127},
            {month:'Jan', region:'NA', segment:'AL&Trade', al:0, c1:0, c2:233, value:2039},
            {month:'Jan', region:'CIS', segment:'General', al:7371, c1:1195, c2:65, value:3418},
            {month:'Jan', region:'CIS', segment:'AL&NoTrade', al:0, c1:491, c2:18, value:177},
            {month:'Jan', region:'CIS', segment:'AL&Trade', al:0, c1:0, c2:336, value:2940},
            {month:'Jan', region:'MENA', segment:'General', al:813, c1:164, c2:13, value:429},
            {month:'Jan', region:'MENA', segment:'AL&NoTrade', al:0, c1:59, c2:3, value:29},
            {month:'Jan', region:'MENA', segment:'AL&Trade', al:0, c1:0, c2:58, value:508},
            {month:'Jan', region:'APAC', segment:'General', al:1479, c1:206, c2:19, value:737},
            {month:'Jan', region:'APAC', segment:'AL&NoTrade', al:0, c1:76, c2:10, value:91},
            {month:'Jan', region:'APAC', segment:'AL&Trade', al:0, c1:0, c2:63, value:551},
            {month:'Feb', region:'NA', segment:'General', al:2571, c1:491, c2:41, value:1355},
            {month:'Feb', region:'NA', segment:'AL&NoTrade', al:0, c1:93, c2:11, value:100},
            {month:'Feb', region:'NA', segment:'AL&Trade', al:0, c1:0, c2:179, value:1566},
            {month:'Feb', region:'CIS', segment:'General', al:9820, c1:1826, c2:112, value:4785},
            {month:'Feb', region:'CIS', segment:'AL&NoTrade', al:0, c1:647, c2:18, value:183},
            {month:'Feb', region:'CIS', segment:'AL&Trade', al:0, c1:0, c2:347, value:3036},
            {month:'Feb', region:'MENA', segment:'General', al:895, c1:179, c2:6, value:400},
            {month:'Feb', region:'MENA', segment:'AL&NoTrade', al:0, c1:55, c2:0, value:2},
            {month:'Feb', region:'MENA', segment:'AL&Trade', al:0, c1:0, c2:71, value:621},
            {month:'Feb', region:'APAC', segment:'General', al:1548, c1:207, c2:21, value:780},
            {month:'Feb', region:'APAC', segment:'AL&NoTrade', al:0, c1:58, c2:6, value:55},
            {month:'Feb', region:'APAC', segment:'AL&Trade', al:0, c1:0, c2:64, value:560},
            {month:'Mar', region:'EU', segment:'General', al:83586, c1:10427, c2:756, value:38795},
            {month:'Mar', region:'CIS', segment:'General (CIS EXC)', al:9872, c1:1100, c2:31, value:4067},
            {month:'Mar', region:'CIS', segment:'General MB', al:44685, c1:4023, c2:72, value:17771},
            {month:'Mar', region:'CIS', segment:'AL&NoTrade MB', al:0, c1:1909, c2:24, value:286},
            {month:'Mar', region:'CIS', segment:'AL&Trade', al:0, c1:0, c2:165, value:1444},
            {month:'Mar', region:'LATAM', segment:'General', al:4805, c1:624, c2:38, value:2183},
            {month:'Mar', region:'NA', segment:'General MB', al:2568, c1:246, c2:14, value:1108},
            {month:'Mar', region:'NA', segment:'AL&NoTrade MB', al:0, c1:126, c2:2, value:23},
            {month:'Mar', region:'NA', segment:'AL&Trade', al:0, c1:0, c2:50, value:438},
            {month:'Mar', region:'MENA', segment:'General MB', al:2668, c1:241, c2:5, value:1067},
            {month:'Mar', region:'MENA', segment:'AL&NoTrade MB', al:0, c1:79, c2:2, value:21},
            {month:'Mar', region:'MENA', segment:'AL&Trade', al:0, c1:0, c2:27, value:236},
            {month:'Mar', region:'APAC', segment:'General MB', al:2789, c1:209, c2:6, value:1121},
            {month:'Mar', region:'APAC', segment:'AL&NoTrade MB', al:0, c1:72, c2:2, value:20},
            {month:'Mar', region:'APAC', segment:'AL&Trade', al:0, c1:0, c2:16, value:140}
        ];

        document.addEventListener('DOMContentLoaded', () => {
            const filterBtns = document.querySelectorAll('#missionsRegionFilter .partner-btn');
            
            filterBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    filterBtns.forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    const region = e.target.dataset.region;
                    
                    // 1. Update Section A KPIs
                    const isAll = region === 'All Regions';
                    let janVal = 0, febVal = 0, marVal = 0;
                    
                    missionsData.forEach(d => {
                        const match = isAll || d.region === region;
                        if(match) {
                            if(d.month === 'Jan') janVal += d.value;
                            if(d.month === 'Feb') febVal += d.value;
                            if(d.month === 'Mar') marVal += d.value;
                        }
                    });
                    
                    const kpiCards = document.querySelectorAll('#tradeit-tab-missions .kpi-card');
                    if (kpiCards.length >= 3) {
                        kpiCards[0].querySelector('.kpi-value').textContent = '€' + janVal.toLocaleString('en-US');
                        kpiCards[1].querySelector('.kpi-value').textContent = '€' + febVal.toLocaleString('en-US');
                        kpiCards[2].querySelector('.kpi-value').textContent = '€' + marVal.toLocaleString('en-US');
                        
                        if (isAll) {
                            kpiCards[0].querySelector('.kpi-sub').textContent = 'AL: 11,981 | C1: 2,690 | C2: 868';
                            kpiCards[1].querySelector('.kpi-sub').textContent = 'MoM: +€1,189 (+9.7%)';
                        } else {
                            kpiCards[0].querySelector('.kpi-sub').textContent = `Filtered: ${region}`;
                            kpiCards[1].querySelector('.kpi-sub').textContent = `Filtered: ${region}`;
                        }
                    }

                    // 2. Filter Section B Table
                    const bRows = document.querySelectorAll('#tradeit-tab-missions .section:nth-of-type(3) tbody tr');
                    bRows.forEach(row => {
                        const regionCell = row.cells[1].textContent.trim();
                        // "CIS EXC" should match "CIS"
                        const match = isAll || regionCell.startsWith(region);
                        row.style.display = match ? '' : 'none';
                    });

                    // 3. Filter Section C Summary Table
                    const cRows = document.querySelectorAll('#tradeit-tab-missions .section:nth-of-type(4) tbody tr');
                    cRows.forEach(row => {
                        const regionCell = row.cells[0].textContent.trim();
                        row.style.display = (isAll || regionCell === region) ? '' : 'none';
                    });

                    // 4. Update Section C Chart
                    if (window.charts && charts.tradeit && charts.tradeit.missionsRegion) {
                        const chart = charts.tradeit.missionsRegion;
                        const regions = ['EU', 'CIS', 'LATAM', 'NA', 'MENA', 'APAC'];
                        
                        chart.data.labels = regions.filter(r => isAll || r === region);
                        
                        const janDataOrig = [null, 6535, null, 3377, 965, 1378];
                        const febDataOrig = [null, 8004, null, 3022, 1023, 1395];
                        const marDataOrig = [38795, 19501, 2183, 1568, 1324, 1281];
                        
                        chart.data.datasets[0].data = chart.data.labels.map(l => janDataOrig[regions.indexOf(l)]);
                        chart.data.datasets[1].data = chart.data.labels.map(l => febDataOrig[regions.indexOf(l)]);
                        chart.data.datasets[2].data = chart.data.labels.map(l => marDataOrig[regions.indexOf(l)]);
                        
                        chart.update();
                    }
                });
            });
        });
"""

# Let's insert the JS right before the closing </body> tag
content = content.replace('</body>', filter_js + '\n</body>')

with open('analysis/nsm-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
