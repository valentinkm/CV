import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import re

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

        # Check if the subsection or detail contains a link placeholder and make it clickable
        link_match_subsection = re.search(r'\[(.+)\]\((https?://\S+)\)', subsection)
        if link_match_subsection:
            link_text = link_match_subsection.group(1)
            link_url = link_match_subsection.group(2)
            if 'github.com' in link_url:
                subsection = re.sub(r'\[(.+)\]\((https?://\S+)\)', f'<a href="{link_url}" target="_blank">{link_text} <img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/github.svg" alt="GitHub" width="16" height="16"></a>', subsection)
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
template_str = '''
<!DOCTYPE html>
<html>
<head>
    <title>Valentin Kriegmair - CV</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 style="text-align: left;">Valentin Kriegmair</h1>
    <div class="contact-info" style="text-align: left;">
        <p>Urbanstraße 36b | 10967 Berlin</p>
        <p>valentin.kriegmair@gmail.com | 015119090065</p>
        <p>
            <a href="https://github.com/valentinkm" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/github.svg" alt="GitHub" width="16" height="16"> GitHub</a> |
            <a href="https://www.linkedin.com/in/valentin-kriegmair-a12b4b269" target="_blank"><img src="https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/linkedin.svg" alt="LinkedIn" width="16" height="16"> LinkedIn</a>
        </p>
    </div>

    {% for section, items in sections.items() %}
    <h2>{{ section }}</h2>
    <table>
        {% for item in items %}
        <tr>
            <td>{{ item['Subsection'] | safe }}</td>
            <td>{{ item['Detail'] | safe }}</td>
        </tr>
        {% endfor %}
    </table>
    <br>
    {% endfor %}
</body>
</html>
'''

# Render the HTML
html_template = env.from_string(template_str)
html_output = html_template.render(sections=sections)

# Save the rendered HTML to a file
with open('index.html', 'w') as f:
    f.write(html_output)

print("HTML CV generated as 'index.html'")

# Optional: Convert the HTML to a PDF (requires WeasyPrint)
try:
    from weasyprint import HTML
    HTML('index.html').write_pdf('cv.pdf')
    print("PDF CV generated as 'cv.pdf'")
except ImportError:
    print("WeasyPrint is not installed. Install it to generate a PDF version.")