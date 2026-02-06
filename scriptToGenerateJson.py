import pandas as pd
import json

# Load CSV
file_path = r"C:\Users\Admin\Downloads\complaints_processed.csv\complaints_processed.csv"
df = pd.read_csv(file_path)

# Rename columns if needed (adjust these if your column names differ)
df = df.rename(columns={
    df.columns[2]: "complaint",
    df.columns[1]: "category",
    df.columns[0]: "sr"
})

knowledge_base = {"KnowledgeBase": []}

# Group complaints by category
grouped = df.groupby("category")

for category, group in grouped:
    complaints = group["complaint"].dropna().unique().tolist()

    if not complaints:
        continue

    entry = {
        "Category": category,
        "Complaint": complaints[0],              # representative complaint
        "Complaint Variants": complaints          # all variants
    }

    knowledge_base["KnowledgeBase"].append(entry)

# Save JSON to file
output_path = r"C:\Users\Admin\Desktop\Day_Zero\Complaints.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(knowledge_base, f, indent=2, ensure_ascii=False)

print(f"Knowledge base JSON created at: {output_path}")
