import json
import re

with open('assets/papers.json', 'r') as f:
    unique_papers = json.load(f)

html_blocks = []
for p in unique_papers:
    venue = p.get('venue', '')
    year = p.get('year', '')
    
    authors = p.get('authors', '')
    # replace Fabian Gloeckle with bold version
    authors = re.sub(r'Fabian Gloeckle', r'<strong>Fabian Gloeckle</strong>', authors)
    
    link = p.get('link', '')
    link_type = p.get('link_type', '[Link]')
    
    links_html = f'<a href="{link}" target="_blank">{link_type}</a>'
    if 'extra_links' in p:
        for ext in p['extra_links']:
            links_html += f'\n                        <a href="{ext["url"]}" target="_blank">{ext["label"]}</a>'
            
    html = f"""                <div class="publication">
                    <div class="pub-title">{p['title']}</div>
                    <div class="pub-authors">{authors}</div>
                    <div class="pub-venue">{venue}</div>
                    <div class="pub-links">
                        {links_html}
                    </div>
                </div>"""
    html_blocks.append(html)

html_content = "\n".join(html_blocks)

with open('papers.html', 'w') as f:
    f.write(html_content)

print(f"Generated papers.html with {len(unique_papers)} papers.")
