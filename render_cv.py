import pandas as pd
from jinja2 import Environment, FileSystemLoader
import re
import pdfkit

# Load CSV data
csv_file = 'cv_data.csv'
df = pd.read_csv(csv_file)

# Organize data into sections
def organize_data(df):
    sections = {}
    for _, row in df.iterrows():
        section = row['Section']
        if section not in sections:
            sections[section] = []
        subsection = row['Subsection']
        detail = row['Detail']

        # Replace incorrect symbols in dates
        subsection = subsection.replace('â€“', '–').replace('â€”', '—')
        detail = detail.replace('â€“', '–').replace('â€”', '—')

        # Check if the subsection or detail contains a link placeholder and make it clickable
        link_match_subsection = re.search(r'\[(.+)\]\((https?://\S+)\)', subsection)
        if link_match_subsection:
            link_text = link_match_subsection.group(1)
            link_url = link_match_subsection.group(2)
            if 'github.com' in link_url:
                subsection = re.sub(r'\[(.+)\]\((https?://\S+)\)', f'<a href="{link_url}" target="_blank">{link_text} <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png" alt="GitHub" width="16" height="16" alt="GitHub" width="16" height="16"></a>', subsection)
            else:
                subsection = re.sub(r'\[(.+)\]\((https?://\S+)\)', f'<a href="{link_url}" target="_blank">{link_text}</a>', subsection)

        link_match_detail = re.search(r'\[(.+)\]\((https?://\S+)\)', detail)
        if link_match_detail:
            link_text = link_match_detail.group(1)
            link_url = link_match_detail.group(2)
            detail = re.sub(r'\[(.+)\]\((https?://\S+)\)', f'<a href="{link_url}" target="_blank">{link_text}</a>', detail)

        sections[section].append({'Subsection': subsection, 'Detail': detail})
    return sections

sections = organize_data(df)

# Setup Jinja2 environment for HTML templating
env = Environment(loader=FileSystemLoader('.'))

# Render the CV HTML
template_str = '''
<!DOCTYPE html>
<html>
<head>
    <title>Valentin Kriegmair Resume - CV</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style.css">
    <style>
        body {
            font-family: 'Helvetica', sans-serif;
            color: #333;
            background-color: #ffffff;
            line-height: 1.6;
            margin: 0;
            padding: 0 20px;
        }
        h1 {
            font-size: 36px;
            color: #222;
            margin-bottom: 10px;
        }
        .contact-info p {
            margin: 2px 0;
            font-size: 14px;
        }
        h2 {
            font-size: 24px;
            color: #444;
            border-bottom: 2px solid #ddd;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        table td {
            padding: 10px;
            vertical-align: top;
        }
        a {
            text-decoration: none;
            color: #0077b5;
        }
        a:hover {
            text-decoration: underline;
        }
        img {
            vertical-align: middle;
            margin-right: 5px;
            width: 16px;
            height: 16px;
        }
        .contact-info {
            margin-bottom: 20px;
        }
        .contact-info a {
            margin-right: 15px;
        }
    </style>
</head>
<body>
    <h1 style="text-align: left;">Valentin Kriegmair</h1>
    <div class="contact-info" style="text-align: left;">
        <p>Urbanstrasse 36b | 10967 Berlin</p>
        <p>valentin.kriegmair@gmail.com | 015119090065</p>
        <p>
            <a href="https://github.com/valentinkm" target="_blank"><img src="https://img.icons8.com/ios-glyphs/30/000000/github.png" alt="GitHub"> GitHub</a>
            <a href="https://www.linkedin.com/in/valentin-kriegmair-a12b4b269" target="_blank" style="margin-left: 15px;"><img src="https://img.icons8.com/ios-glyphs/30/000000/linkedin.png" alt="LinkedIn" width="16" height="16" alt="LinkedIn"> LinkedIn</a>
        </p>
    </div>

    {% for section, items in sections.items() %}
    <h2>{{ section }}</h2>
    <table>
        {% for item in items %}
        <tr>
            <td style="width: 30%; font-weight: bold;">{{ item['Subsection'] | safe }}</td>
            <td style="width: 70%;">{{ item['Detail'] | safe }}</td>
        </tr>
        {% endfor %}
    </table>
    <br>
    {% endfor %}
    <div style="text-align: center; margin-top: 20px;">
        <a href="cv.pdf" target="_blank">Download PDF Version of CV</a>
    </div>
</body>
</html>
'''

html_template = env.from_string(template_str)
html_output = html_template.render(sections=sections)

# Save the rendered HTML to a file
with open('cv.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("HTML CV generated as 'cv.html'")

# Convert the CV HTML file to PDF using pdfkit
try:
    options = {
        'quiet': '',
        'enable-local-file-access': None,
        'encoding': 'UTF-8'
    }
    pdfkit.from_file('cv.html', 'cv.pdf', options=options)
    print("CV PDF generated as 'cv.pdf'")
except Exception as e:
    print(f"An error occurred while generating the PDF: {e}")
