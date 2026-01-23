import pandas as pd
import os

# Read the latest Excel file
files = [f for f in os.listdir('.') if f.startswith('leads_') and f.endswith('.xlsx')]
latest_file = max(files, key=os.path.getctime)
df = pd.read_excel(latest_file)

# HTML Template with "Hacker/Dashboard" aesthetic
html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automation Result</title>
    <style>
        body {{
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Consolas', 'Monaco', monospace;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max_width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            color: #58a6ff;
            border-bottom: 2px solid #21262d;
            padding-bottom: 10px;
        }}
        .stat-box {{
            background: #161b22;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #30363d;
            margin-bottom: 20px;
        }}
        .success-text {{ color: #2ea043; font-weight: bold; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #30363d;
            color: #8b949e;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #21262d;
        }}
        tr:nth-child(even) {{ background-color: #161b22; }}
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-bar">
            <h1>>> Google Maps Scraper Results</h1>
            <span class="success-text">● Status: COMPLETED</span>
        </div>
        
        <div class="stat-box">
            <p>Target: <span style="color: #fff">新宿 カフェ</span></p>
            <p>Collected: <span class="success-text">{len(df)} items</span></p>
            <p>File: {latest_file}</p>
        </div>

        <table>
            <thead>
                <tr>
                    <th>No.</th>
                    <th>Business Name</th>
                    <th>Link Status</th>
                </tr>
            </thead>
            <tbody>
"""

for i, row in df.iterrows():
    name = str(row['Name'])
    link = "✅ Acquired" if str(row['Link']).startswith('http') else "❌ Missing"
    html_content += f"""
                <tr>
                    <td>{i+1:02d}</td>
                    <td style="color: #fff; font-weight: bold;">{name}</td>
                    <td class="success-text">{link}</td>
                </tr>
    """

html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

with open("assets/preview.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("assets/preview.html created.")
