
import json
import os

notebook_path = '/home/gabisml/ic/sionna/tutorials/sys/SYS_Meets_RT_modified.ipynb'

with open(notebook_path, 'r') as f:
    nb = json.load(f)

found = False
modified = False
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = cell.get('source', [])
        source_text = "".join(source)
        
        # Look for the specific plotting cell by content
        if "np.reshape(is_scheduled_hist" in source_text and "plt.imshow" in source_text:
            print(f"Found target cell {i}")
            print("--- Original Source ---")
            print(source_text)
            print("-----------------------")
            
            new_source = []
            for line in source:
                # Replace the assignment target
                # Pattern: is_scheduled_hist = np.reshape(is_scheduled_hist,
                if "is_scheduled_hist = np.reshape" in line:
                    print(f"Modifying line: {line.strip()}")
                    new_line = line.replace("is_scheduled_hist =", "is_scheduled_plot =", 1)
                    new_source.append(new_line)
                    modified = True
                
                # Replace the usage in imshow
                # Pattern: plt.imshow(is_scheduled_hist.T, cmap=cmap, aspect='auto')
                elif "plt.imshow(is_scheduled_hist.T" in line:
                    print(f"Modifying line: {line.strip()}")
                    new_line = line.replace("is_scheduled_hist.T", "is_scheduled_plot.T", 1)
                    new_source.append(new_line)
                    modified = True
                    
                else:
                    new_source.append(line)
            
            if modified:
                cell['source'] = new_source
                print("--- New Source ---")
                print("".join(new_source))
                print("------------------")
                found = True
                break

if found and modified:
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print("Notebook update written to disk.")
elif not found:
    print("Target cell NOT found.")
else:
    print("Target cell found but NO modifications made (patterns didn't match lines?).")
