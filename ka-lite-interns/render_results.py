import jinja2
import csv

template = u"""
<html>
<head>
</head>
<body>
    {% for row in csv %}
        <h1>Name: {{ row.10 }}, {{ row.9 }}</h1>
        <h2>Email: {{ row.11 }}</h2>
        <h2>Position: {{ row.1 }}</h2>
        <h2>Cover Letter:</h2>
        <p>{{ row.2 }}{{ row.5 }}{{ row.12 }}{{ row.14 }}{{ row.17 }}{{ row.19 }}</p>
        <h2>Tell us about yourself</h2>
        <p>{{row.43}}{{row.44}}{{row.45}}{{row.46}}{{row.47}}{{row.48}}</p>

        <h3>Additional items: </h3>
        <p><strong>Link to online portfolio</strong>: {{ row.3 }}</p>
        <p><strong>Link to online resume or linkedIn</strong>: {{ row.16 }}{{ row.18 }}{{ row.20 }}{{ row.21 }}{{ row.27 }}{{ row.28 }}{{ row.29 }}{{ row.30 }}{{ row.31 }}{{ row.32 }}</p>
        <p><strong>A list of 3 things you'd improve about either of our sites</strong>: {{ row.4 }}</p>
        <p><strong>Links to any live projects, past projects, your GitHub account and/or online portfolio</strong>: {{ row.6 }}{{ row.13 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [Photoshop/GIMP]</strong>: {{ row.23 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [Illustrator/Inkscape]</strong>: {{ row.24 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [Visual Design Principles]</strong>: {{ row.25 }}{{row.37}}</p>
        <p><strong>Rate your level of experience with the following tools/skills [User Experience Design Principles]</strong>: {{ row.26 }}{{ row.36 }}{{row.42}}</p>
        <p><strong>Rate your level of experience with the following tools/skills [HTML]</strong>: {{ row.33 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [CSS/LESS]</strong>: {{ row.34 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [JS]</strong>: {{ row.35 }}{{row.40}}</p>
        <p><strong>Rate your level of experience with the following tools/skills [Python]</strong>: {{ row.38 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [Django]</strong>: {{ row.39 }}</p>
        <p><strong>Rate your level of experience with the following tools/skills [Git]</strong>: {{ row.41 }}</p>
    {% endfor %}
    </table>
</body>
</html>
""".replace("\n", "")

t = jinja2.Template(template)

data = list(csv.reader(open("responses.csv")))[1:]

def clean(s):
    return s#
    # .encode('utf-8')

data = [[clean(a) for a in l] for l in data]
        
f = open("results.html", "w")

unicode_data = []
for item in data: 
    unicode_items = []
    for i in item:
        unicode_items.append(i.decode('utf-8'))
    unicode_data.append(unicode_items)

# for l in unicode_data:
#     for a in l:
#         try: 
#             unicode(a)
#         except:
#             print a

html = t.render({"csv": unicode_data}).replace(u"\u2019", "'").replace("\n", "<br/>").replace(u"\xa0"," ").replace(u"\u201c", '"').replace(u"\u201d", '"').replace(u"\u2013", '-')

f.write(html)

f.close()