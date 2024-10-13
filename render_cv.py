import pandas as pd

from jinja2 import Environment, FileSystemLoader

# Load the CSV data
cv_data = pd.read_csv('cv_data.csv')

# Setup Jinja2 environment for HTML templating
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Organize data for templating
sections = cv_data.groupby('Section')

# Render the template with data
html_output = template.render(sections=sections)

# Write the rendered HTML to a file
with open('index.html', 'w') as file:
    file.write(html_output)
