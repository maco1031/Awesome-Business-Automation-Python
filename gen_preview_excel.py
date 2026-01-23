import pandas as pd
import os

# Read the latest Excel file
files = [f for f in os.listdir('.') if f.startswith('leads_') and f.endswith('.xlsx')]
latest_file = max(files, key=os.path.getctime)
df = pd.read_excel(latest_file)

# Excel-like HTML Template
html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{latest_file} - Excel</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            background-color: #f0f0f0;
            overflow: hidden; /* Prevent body scroll, use inner scroll */
        }}
        .excel-header {{
            background-color: #217346;
            color: white;
            padding: 8px 15px;
            font-size: 14px;
            display: flex;
            align-items: center;
        }}
        .excel-toolbar {{
            background-color: #f3f2f1;
            border-bottom: 1px solid #e1dfdd;
            padding: 5px;
            height: 30px;
        }}
        .sheet-container {{
            background: white;
            height: calc(100vh - 70px);
            overflow: auto;
            position: relative;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            table-layout: fixed;
        }}
        th, td {{
            border: 1px solid #d4d4d4;
            padding: 4px 8px;
            font-size: 13px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            height: 20px;
        }}
        th {{
            background-color: #f8f9fa;
            color: #666;
            font-weight: normal;
            text-align: center;
        }}
        /* Column Widths */
        th:nth-child(1) {{ width: 40px; background-color: #f8f9fa; border-right: 2px solid #ccc; }} /* Row Number Header */
        th:nth-child(2) {{ width: 250px; }} /* Name */
        th:nth-child(3) {{ width: 150px; }} /* Search Query */
        th:nth-child(4) {{ width: 400px; }} /* Link */
        
        td:nth-child(1) {{
            background-color: #f8f9fa;
            text-align: center;
            color: #666;
            border-right: 2px solid #ccc;
        }}
        
        tr:hover td:not(:first-child) {{
            background-color: #e6f2ea; /* Excel selection color */
        }}
    </style>
</head>
<body>
    <div class="excel-header">
        <span>💾</span>&nbsp;&nbsp;{latest_file} - Excel
    </div>
    <div class="excel-toolbar">
        <!-- Mock toolbar -->
        <span style="color:#666; font-size:12px; margin-left:10px;">File | Home | Insert | Page Layout | Formulas | Data | Review | View</span>
    </div>

    <div class="sheet-container">
        <table>
            <thead>
                <tr>
                    <th></th> <!-- Corner -->
                    <th>A</th>
                    <th>B</th>
                    <th>C</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td style="font-weight:bold;">Name</td>
                    <td style="font-weight:bold;">Search Query</td>
                    <td style="font-weight:bold;">Link</td>
                </tr>
"""

for i, row in df.iterrows():
    name = str(row['Name'])
    query = str(row['Search Query'])
    link = str(row['Link'])
    html_content += f"""
                <tr>
                    <td>{i+2}</td>
                    <td>{name}</td>
                    <td>{query}</td>
                    <td style="color:blue; text-decoration:underline;">{link}</td>
                </tr>
    """

html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

with open("assets/preview_excel.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("assets/preview_excel.html created.")
