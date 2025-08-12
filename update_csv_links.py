"""Update an input CSV (Company Name, OldLink) to a new CSV with fresh application links
Usage: python update_csv_links.py input.csv output.csv https://your-deployed-url/apply
"""
import csv, random, sys
from urllib.parse import quote_plus

if len(sys.argv) < 4:
    print('Usage: python update_csv_links.py input.csv output.csv https://your-deployed-url/apply')
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = sys.argv[2]
base = sys.argv[3].rstrip('/')

rows = []
with open(input_csv, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader, None)
    for r in reader:
        if not r: continue
        name = r[0].strip()
        # build new link
        track = str(random.randint(1000000000, 9999999999))
        comp = quote_plus(name)
        new_link = f"{base}?company={comp}&track={track}&utm_source=Simplify&gh_src=Simplify"
        rows.append([name, new_link])

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Company Name', 'Application Link'])
    writer.writerows(rows)

print(f'Wrote {len(rows)} updated links to {output_csv}')
