#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix notebook 2: Add logging, preserve raw data
"""
import json
from pathlib import Path

# Load notebook
nb_path = Path("notebooks/02_Building_Cleaned_Matrix.ipynb")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and fix cells
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    source = ''.join(cell['source'])
    
    # PROBLEMA C: Cell 5 - sobrescreve raw data
    if "wrong_files = [" in source and "file_df.to_csv(file" in source:
        print(f"✓ Fixing CELL {i}: Column swap (CELL 5)")
        new_source = '''import pandas as pd
from pathlib import Path

# Ensure processed directory exists
Path("../data/processed").mkdir(parents=True, exist_ok=True)

wrong_files = [
    "../data/raw/GSM8564267_HCB10-21.xls",
    "../data/raw/GSM8564268_HCB11-21.xls"
]

for file_path in wrong_files:
    file_df = pd.read_csv(file_path, sep="\t")

    # Get columns
    cols = list(file_df.columns)

    # Swap columns 'Transcription ID' and sample column
    cols[3], cols[5] = cols[5], cols[3]

    # Reorder dataframe
    file_df = file_df[cols]

    # Print new order
    print(f"\n{Path(file_path).name}")
    print(file_df.columns[0]+" | "+
          file_df.columns[1]+" | "+
          file_df.columns[2]+" | "+
          file_df.columns[3]+" | "+
          file_df.columns[4]+" | "+
          file_df.columns[5]+" | "+
          file_df.columns[6])

    # Save to processed, NOT overwriting raw
    processed_file = file_path.replace("../data/raw/", "../data/processed/fixed_")
    file_df.to_csv(processed_file, sep="\t", index=False)
    inconsistencies_log["column_fixes"].append({
        "file": Path(file_path).name,
        "fix": "Swapped columns 3 and 5",
        "output": processed_file
    })
    print(f"Fixed file saved to: {processed_file}")'''
        
        cell['source'] = new_source.split('\n')
        # Add newlines to source
        cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line 
                          for i, line in enumerate(cell['source'])]
    
    # PROBLEMA C: Cell 12 - sobrescreve raw data (filtra por Type)
    elif "file_df = file_df[file_df[\"Type\"] == \"mRNA\"]" in source and "file_df.to_csv(file" in source:
        print(f"✓ Fixing CELL {i}: Filter by Type (CELL 12)")
        new_source = '''# Process files: filter by Type and save to processed
for file in files:
    file_df = pd.read_csv(file, sep="\t")
    
    # Count before filtering
    before_count = len(file_df)
    
    file_df = file_df[file_df["Type"] == "mRNA"]
    
    after_count = len(file_df)
    
    # Save to processed, NOT overwriting raw
    processed_file = str(file).replace("../data/raw/", "../data/processed/filtered_")
    file_df.to_csv(processed_file, sep="\t", index=False)
    
    inconsistencies_log["filtered_files"].append({
        "file": file.name,
        "rows_before": before_count,
        "rows_after": after_count,
        "rows_removed": before_count - after_count,
        "output": processed_file
    })
    
    print(f"{file.name}: {before_count} → {after_count} rows (removed {before_count - after_count})")'''
        
        cell['source'] = new_source.split('\n')
        cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line 
                          for i, line in enumerate(cell['source'])]

# Add logging initialization at the beginning if not present
first_code_cell = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        first_code_cell = i
        break

if first_code_cell is not None:
    source = ''.join(nb['cells'][first_code_cell]['source'])
    if 'inconsistencies_log' not in source:
        print(f"✓ Adding logging initialization at CELL {first_code_cell}")
        
        new_source = '''from pathlib import Path
import pandas as pd
from datetime import datetime

# Initialize logging for inconsistencies
inconsistencies_log = {
    "timestamp": datetime.now().isoformat(),
    "duplicates": [],
    "missing_values": [],
    "column_fixes": [],
    "filtered_files": []
}

files = list(Path("../data/raw").glob("*.xls"))

for file in files:
    print(file)'''
        
        nb['cells'][first_code_cell]['source'] = new_source.split('\n')
        nb['cells'][first_code_cell]['source'] = [line + '\n' if i < len(nb['cells'][first_code_cell]['source']) - 1 else line 
                                                    for i, line in enumerate(nb['cells'][first_code_cell]['source'])]

# Add cell at end to save logs
print(f"✓ Adding cell to save inconsistencies log")
log_save_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Save inconsistencies log\n",
        "import json\n",
        "\n",
        "log_file = '../data/processed/inconsistencies_log.json'\n",
        "Path('../data/processed').mkdir(parents=True, exist_ok=True)\n",
        "\n",
        "with open(log_file, 'w') as f:\n",
        "    json.dump(inconsistencies_log, f, indent=2)\n",
        "\n",
        "print(f'Inconsistencies log saved to: {log_file}')"
    ]
}

nb['cells'].append(log_save_cell)

# Save corrected notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n✅ Notebook corrigido! Salvo em: {nb_path}")
print("\nMudanças:")
print("  ✓ Problema C (CRÍTICO): Raw data não será mais sobrescrito")
print("     - Dados processados salvos em ../data/processed/")
print("  ✓ Problema A: Logs de inconsistências salvos em JSON")
print("  ✓ Problema B: Pode refatorar em funções depois (marcado como secundário)")
