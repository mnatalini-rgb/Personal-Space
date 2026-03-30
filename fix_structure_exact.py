with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/nsm-dashboard.html', 'r') as f:
    lines = f.readlines()

# find exactly where weekly-performance-section is
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '<div class="section" id="weekly-performance-section">' in line:
        start_idx = i
        break

if start_idx != -1:
    # it ends at start_idx + 26
    end_idx = start_idx + 26
    
    # get the section lines
    section_lines = lines[start_idx:end_idx+1]
    
    # remove them from original place (delete from end to start to preserve indices)
    del lines[start_idx:end_idx+1]
    
    # now we insert them right before the </div> that closes the tradeit-tab-missions.
    # We want it to be right before the last closing </div> in that block.
    # The block ends around line 795 (now 795 since we haven't deleted yet, wait, we deleted AFTER it).
    # Since we deleted lines AFTER the insertion point, the insertion point index remains the same.
    # The user said: "before line 793 (</div> closing the Missions tab)". But line 793 in the original file was the first </div> after </table>.
    # Let's see the context.
    
    insert_idx = -1
    for i in range(780, 800):
        if '</table>' in lines[i] and '</div>' in lines[i+1]:
            # we want to insert after the </div> that closes the .section.
            # </table> is i, </div> for table-wrapper is i+1, </div> for section is i+2
            # </div> for tradeit-tab-missions is i+3
            insert_idx = i + 3
            break

    if insert_idx != -1:
        # insert section_lines at insert_idx
        for j, line in enumerate(section_lines):
            lines.insert(insert_idx + j, line)
        
        with open('/Users/moritznatalini/Desktop/Master_Product_Folder/analysis/nsm-dashboard.html', 'w') as f:
            f.writelines(lines)
        print(f"Successfully moved section to index {insert_idx}")
    else:
        print("Could not find insertion point.")
else:
    print("Could not find weekly-performance-section.")

