with open('rankings_fto_double.tsv', 'r') as f:
    lines = f.readlines()

cleaned = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 2:  # Ensure it's a valid line
        name = parts[1]
        # Remove duplicate names (assumes names are exactly doubled)
        if len(name) % 2 == 0 and name[:len(name)//2] == name[len(name)//2:]:
            parts[1] = name[:len(name)//2]
        cleaned.append('\t'.join(parts))

with open('rankings_fto_cleaned.tsv', 'w') as f:
    f.writelines(cleaned)