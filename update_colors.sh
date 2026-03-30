#!/bin/bash
FILE="/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/nsm-dashboard.html"

# CSS variables
sed -i '' 's/--bg: #0e0f11;/--bg: #f8f9fa;/' "$FILE"
sed -i '' 's/--surface: #151618;/--surface: #ffffff;/' "$FILE"
sed -i '' 's/--border: #232529;/--border: #e2e4e9;/' "$FILE"
sed -i '' 's/--text: #eeeeee;/--text: #1a1a2e;/' "$FILE"
sed -i '' 's/--text-muted: #8b8d91;/--text-muted: #6b7280;/' "$FILE"
sed -i '' 's/--accent: #5e6ad2;/--accent: #2563eb;\n            --accent-light: #dbeafe;/' "$FILE"
sed -i '' 's/--green: #2ecc71;/--green: #059669;/' "$FILE"
sed -i '' 's/--red: #e74c3c;/--red: #dc2626;\n            --yellow: #d97706;/' "$FILE"

# CSS classes
sed -i '' 's/rgba(94, 106, 210, 0.15)/var(--accent-light)/g' "$FILE"
sed -i '' 's/rgba(35, 37, 41, 0.5)/#f1f3f5/g' "$FILE"
sed -i '' 's/\.section { margin-bottom: 3rem; background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 2rem; }/.section { margin-bottom: 3rem; background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }/' "$FILE"
sed -i '' 's/\.kpi-card { background-color: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; text-align: center; }/.kpi-card { background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; text-align: center; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }/' "$FILE"
sed -i '' 's/\.table-wrapper { overflow-x: auto; background-color: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 1.5rem; }/.table-wrapper { overflow-x: auto; background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 1.5rem; }/' "$FILE"
sed -i '' 's/\.insight-card { background-color: var(--bg); border-left: 4px solid var(--accent); border-radius: var(--radius-md); padding: 1.5rem; margin-bottom: 1rem; }/.insight-card { background-color: var(--surface); border-left: 4px solid var(--accent); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; margin-bottom: 1rem; }/' "$FILE"
sed -i '' 's/\.ab-card { background-color: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; }/.ab-card { background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.5rem; }/' "$FILE"
sed -i '' 's/box-shadow: 0 4px 12px rgba(0,0,0,0.4);/box-shadow: 0 4px 12px rgba(0,0,0,0.15);/g' "$FILE"
sed -i '' 's/tr:hover td {/tr:hover td {\n            background-color: #f8f9fa;/' "$FILE"

sed -i '' 's/\.tab-btn:hover { color: var(--text); background-color: var(--surface); }/.tab-btn:hover { color: var(--text); background-color: #f1f3f5; }/' "$FILE"
sed -i '' 's/\.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); background-color: var(--surface); }/.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); background-color: #ffffff; }/' "$FILE"

# JS colors and inline styles
sed -i '' "s/'#8b8d91'/'#6b7280'/g" "$FILE"
sed -i '' "s/'#232529'/'#e2e4e9'/g" "$FILE"
sed -i '' "s/'#eeeeee'/'#1a1a2e'/g" "$FILE"
sed -i '' "s/'#5e6ad2'/'#2563eb'/g" "$FILE"
sed -i '' "s/'rgba(94, 106, 210, 0.4)'/'rgba(37, 99, 235, 0.4)'/g" "$FILE"
sed -i '' "s/'rgba(94,106,210,0.1)'/'rgba(37, 99, 235, 0.1)'/g" "$FILE"
sed -i '' "s/'rgba(94, 106, 210, 0.1)'/'rgba(37, 99, 235, 0.1)'/g" "$FILE"
sed -i '' "s/'#2ecc71'/'#059669'/g" "$FILE"
sed -i '' "s/'#0e0f11'/'#ffffff'/g" "$FILE"
sed -i '' "s/'#fbbf24'/'#d97706'/g" "$FILE"
sed -i '' "s/'#a855f7'/'#7c3aed'/g" "$FILE"
sed -i '' "s/'#e74c3c'/'#dc2626'/g" "$FILE"

sed -i '' 's/background: rgba(21, 22, 24, 0.5)/background: rgba(241, 243, 245, 0.5)/g' "$FILE"
sed -i '' 's/color: #5e6ad2/color: #2563eb/g' "$FILE"
sed -i '' 's/background-color: rgba(94,106,210,0.1)/background-color: rgba(37,99,235,0.1)/g' "$FILE"

# JS Active Pill state: Assuming they are in CSS `.partner-selector .active` or similar
# Wait, the instruction says: "The partner selector pill should use the new accent color for active state". Let's check.
