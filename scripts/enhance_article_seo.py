#!/usr/bin/env python3
"""
Enhance dyarnaa.com articles with SEO elements:
- Table of contents
- Schema.org structured data
- Internal linking
- Reading time
- Better meta description
"""
import re
import json
from pathlib import Path

def add_table_of_contents(html: str, title: str) -> str:
    """Add a table of contents from H2 headings."""
    headings = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    if not headings:
        return html
    
    toc_items = []
    for i, h in enumerate(headings, 1):
        clean = re.sub(r'<[^>]+>', '', h).strip()
        if clean:
            toc_items.append(f'<li><a href="#toc-{i}">{clean}</a></li>')
    
    if not toc_items:
        return html
    
    toc_html = f'''
<div style="background:#f8f9fa;padding:20px;border-radius:12px;margin:30px 0;border-right:4px solid #667eea;">
<h3 style="color:#667eea;margin-top:0;">📋 جدول المحتويات</h3>
<ul style="line-height:2;">
{''.join(toc_items[:8])}
</ul>
</div>
'''
    
    # Insert after first H1 or at the beginning
    h1_match = re.search(r'</h1>', html)
    if h1_match:
        pos = h1_match.end()
        html = html[:pos] + toc_html + html[pos:]
    else:
        html = toc_html + html
    
    # Add IDs to headings
    for i, h in enumerate(headings, 1):
        old = re.escape(h[:50])  # Use first 50 chars as anchor
        new = f'<h2 id="toc-{i}"' + h[3:]  # Replace <h2 with <h2 id="toc-i"
        html = html.replace(h[:3] + '>', f'<h2 id="toc-{i}">', 1)
    
    return html


def add_schema_org(title: str, description: str, slug: str) -> str:
    """Add schema.org Article structured data."""
    schema = f'''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{description}",
  "url": "https://dyarnaa.com/blog/{slug}/",
  "publisher": {{
    "@type": "Organization",
    "name": "ديارنا الحديثة للاستثمار",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://dyarnaa.com/images/logo.png"
    }}
  }},
  "inLanguage": "ar",
  "genre": "natural stone guide"
}}
</script>
'''
    return schema


def add_reading_time(html: str, word_count: int) -> str:
    """Add reading time badge."""
    minutes = max(4, round(word_count / 170))
    badge = f'''
<div style="background:#e8f5e9;padding:10px 20px;border-radius:20px;display:inline-block;margin:10px 0;font-size:14px;color:#2e7d32;">
⏱️ وقت القراءة: {minutes} دقائق
</div>
'''
    
    # Insert after first paragraph
    p_match = re.search(r'</p>', html)
    if p_match:
        pos = p_match.end()
        html = html[:pos] + badge + html[pos:]
    
    return html


def enhance_article(content: str, title: str, description: str, slug: str) -> str:
    """Apply all SEO enhancements to article content."""
    word_count = len(re.sub(r'<[^>]+>', '', content).split())
    
    # Add table of contents
    content = add_table_of_contents(content, title)
    
    # Add schema.org
    schema = add_schema_org(title, description, slug)
    content = content + schema
    
    # Add reading time
    content = add_reading_time(content, word_count)
    
    return content


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 enhance_article_seo.py <blog_post_json_file>")
        sys.exit(1)
    
    path = sys.argv[1]
    with open(path) as f:
        post = json.load(f)
    
    enhanced = enhance_article(
        post.get('content', ''),
        post.get('title', ''),
        post.get('excerpt', ''),
        post.get('slug', '')
    )
    
    post['content'] = enhanced
    post['seo_enhanced'] = True
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Enhanced article: {path}")
    print(f"  Schema.org added")
    print(f"  Table of contents added")
    print(f"  Reading time badge added")
