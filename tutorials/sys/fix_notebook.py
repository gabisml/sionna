
import json
import os

notebook_path = '/home/gabisml/ic/sionna/tutorials/sys/SYS_Meets_RT_modified.ipynb'

with open(notebook_path, 'r') as f:
    nb = json.load(f)

found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell.get('source', [])
        # Check if this is the target cell
        # converting list of strings to single string for easier checking
        source_text = "".join(source)
        if "is_scheduled_hist = np.reshape(is_scheduled_hist" in source_text:
            print("Found target cell.")
            new_source = []
            for line in source:
                if "is_scheduled_hist = np.reshape(is_scheduled_hist" in line:
                    new_line = line.replace("is_scheduled_hist =", "is_scheduled_plot =")
                    new_source.append(new_line)
                elif "plt.imshow(is_scheduled_hist.T" in line:
                    new_line = line.replace("is_scheduled_hist.T", "is_scheduled_plot.T")
                    new_source.append(new_line)
                else:
                    new_source.append(line)
            cell['source'] = new_source
            found = True
            break

if found:
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    print("Notebook fixed successfully.")
else:
    print("Target cell not found.")
