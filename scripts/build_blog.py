import os
import markdown
from datetime import datetime

POSTS_DIR = 'posts'
BLOG_DIR = 'blog'
TEMPLATES_DIR = 'templates'
INDEX_TEMPLATE = os.path.join(TEMPLATES_DIR, 'blog_index.html')
POST_TEMPLATE = os.path.join(TEMPLATES_DIR, 'blog_post.html')
BLOG_INDEX_OUTPUT = 'blog.html'


def parse_tags(raw_tags):
    if raw_tags is None:
        return []

    # Accept frontmatter tags like "a, b" or "[a, b]".
    cleaned = str(raw_tags).strip()
    if cleaned.startswith('[') and cleaned.endswith(']'):
        cleaned = cleaned[1:-1]

    tags = [tag.strip().strip('"\'') for tag in cleaned.split(',')]
    return [tag for tag in tags if tag]

def parse_frontmatter(md_content):
    metadata = {}
    content = md_content
    
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            content = parts[2]
            
            for line in frontmatter.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip()] = val.strip()
                    
    return metadata, content


def render_tag_chips(tags):
    if not tags:
        return ''

    chips = ''.join(f'<span class="tag-chip">{tag}</span>' for tag in tags)
    return f'<div class="post-tags">{chips}</div>'

def build_blog():
    os.makedirs(BLOG_DIR, exist_ok=True)
    
    with open(INDEX_TEMPLATE, 'r') as f:
        index_tpl = f.read()
        
    with open(POST_TEMPLATE, 'r') as f:
        post_tpl = f.read()
        
    posts = []
    
    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(POSTS_DIR, filename)
        with open(filepath, 'r') as f:
            md_content = f.read()
            
        metadata, content = parse_frontmatter(md_content)
        
        # Convert markdown to html
        html_content = markdown.markdown(
            content, 
            extensions=['fenced_code', 'tables', 'mdx_math', 'footnotes', 'sane_lists'],
            extension_configs={'mdx_math': {'enable_dollar_delimiter': True}}
        )
        
        # Default metadata if missing
        title = metadata.get('title', 'Untitled Post')
        date_str = metadata.get('date', 'Jan 1, 2026')
        excerpt = metadata.get('excerpt', '')
        tags = parse_tags(metadata.get('tags'))
        tags_html = render_tag_chips(tags)
        
        # Prepare post HTML
        post_html = post_tpl.replace('{{title}}', title)
        post_html = post_html.replace('{{date}}', date_str)
        post_html = post_html.replace('{{tags}}', tags_html)
        post_html = post_html.replace('{{content}}', html_content)
        
        # Output filename
        slug = filename.replace('.md', '')
        output_filename = f"{slug}.html"
        output_path = os.path.join(BLOG_DIR, output_filename)
        
        # Write post HTML
        with open(output_path, 'w') as f:
            f.write(post_html)
            
        # Parse date for sorting
        try:
            parsed_date = datetime.strptime(date_str, '%b %d, %Y')
        except ValueError:
            parsed_date = datetime.now()
            
        posts.append({
            'title': title,
            'date_str': date_str,
            'date': parsed_date,
            'excerpt': excerpt,
            'tags_html': tags_html,
            'url': f"blog/{output_filename}"
        })
        
        print(f"Built {output_path}")

    # Sort posts by date, newest first
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate index list
    list_items = []
    for post in posts:
        item = f"""                <li class="post-item">
                    <div class="post-date">{post['date_str']}</div>
                    <h2 class="post-title"><a href="{post['url']}">{post['title']}</a></h2>
                    <p class="post-excerpt">{post['excerpt']}</p>
                    {post['tags_html']}
                </li>"""
        list_items.append(item)
        
    
    # Inject into index template
    index_html = index_tpl.replace('{{post_list}}', '\n'.join(list_items))
    
    with open(BLOG_INDEX_OUTPUT, 'w') as f:
        f.write(index_html)
        
    print(f"Built {BLOG_INDEX_OUTPUT}")

if __name__ == '__main__':
    build_blog()
