#!/usr/bin/env python3
"""
Blog Builder Script
Converts Markdown files to HTML with the same theme as the main portfolio site
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

def extract_frontmatter(content):
    """Extract frontmatter from markdown content"""
    if content.startswith('---'):
        end_pos = content.find('---', 3)
        if end_pos != -1:
            frontmatter = content[3:end_pos].strip()
            content = content[end_pos + 3:].strip()
            
            # Parse frontmatter
            metadata = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle list values like tags: ["tag1", "tag2"]
                    if value.startswith('[') and value.endswith(']'):
                        # Remove brackets and split by comma
                        list_content = value[1:-1]  # Remove [ and ]
                        if list_content.strip():  # Check if not empty
                            # Split by comma and clean up each item
                            items = [item.strip().strip('"\'') for item in list_content.split(',')]
                            metadata[key] = items
                        else:
                            metadata[key] = []
                    else:
                        # Remove quotes if present
                        value = value.strip('"\'')
                        
                        # Handle boolean values
                        if value.lower() in ('true', 'false'):
                            value = value.lower() == 'true'
                        
                        # Handle date values
                        if key == 'date':
                            try:
                                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                            except ValueError:
                                try:
                                    value = datetime.strptime(value[:19], '%Y-%m-%dT%H:%M:%S')
                                except ValueError:
                                    value = datetime.now()
                        
                        metadata[key] = value
            
            return metadata, content
    
    return {}, content

def convert_markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    # Configure markdown extensions
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'linenums': True
            }
        }
    )
    
    return md.convert(md_content)

def load_blog_posts(posts_dir):
    """Load all blog posts from the posts directory"""
    posts = []
    
    for file_path in Path(posts_dir).rglob('*.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata, md_content = extract_frontmatter(content)
        
        # Extract slug from filename
        slug = file_path.stem
        
        # Generate HTML content
        html_content = convert_markdown_to_html(md_content)
        
        # Set default values if not in frontmatter
        if 'title' not in metadata:
            metadata['title'] = slug.replace('-', ' ').title()
        
        if 'date' not in metadata:
            metadata['date'] = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        if 'description' not in metadata:
            # Extract first 150 chars of content as description
            plain_text = BeautifulSoup(html_content, 'html.parser').get_text()
            metadata['description'] = plain_text[:150] + "..." if len(plain_text) > 150 else plain_text
        
        if 'tags' not in metadata:
            metadata['tags'] = []
        
        post_data = {
            'slug': slug,
            'filename': str(file_path),
            'metadata': metadata,
            'content': html_content,
            'raw_content': md_content
        }
        
        posts.append(post_data)
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x['metadata']['date'], reverse=True)
    return posts

def generate_blog_html_template():
    """Generate the HTML template for blog posts"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} | Blog - Thamilselven</title>
    <meta name="description" content="{{DESCRIPTION}}">
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{{TITLE}} - Thamilselven">
    <meta property="og:description" content="{{DESCRIPTION}}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tselven.com/blog/{{SLUG}}.html">
    <meta property="og:image" content="{{OG_IMAGE}}">
    <meta property="og:site_name" content="Thamilselven's Blog">
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{TITLE}} - Thamilselven">
    <meta name="twitter:description" content="{{DESCRIPTION}}">
    <meta name="twitter:image" content="{{OG_IMAGE}}">
    <link rel="stylesheet" href="../style.css">
    <link rel="stylesheet" href="./blog.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</head>
<body>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
        <i class="fas fa-moon" id="themeIcon"></i>
    </button>

    <div class="bg-animation">
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
        <div class="floating-shape shape-4"></div>
    </div>

    <div class="card blog-card">
        <!-- Blog Header -->
        <header class="blog-header">
            <div class="blog-title-section">
                <h1 class="blog-post-title">{{TITLE}}</h1>
                <div class="blog-meta">
                    <span class="blog-date"><i class="far fa-calendar"></i> {{DATE}}</span>
                    <!-- TAGS_PLACEHOLDER -->
                </div>
            </div>
        </header>

        <!-- Main Content Area -->
        <div class="blog-content-wrapper">
            <!-- Sidebar -->
            <aside class="blog-sidebar">
                <div class="sidebar-content">
                    <div class="blog-profile">
                        <img src="../thamilselven.jpg" alt="Thamilselven" class="blog-profile-img">
                        <h3 class="blog-author-name">Thamilselven</h3>
                        <p class="blog-author-title">Software Engineer | Backend & DevOps</p>
                    </div>

                    <div class="sidebar-section">
                        <h3 class="sidebar-title">Recent Posts</h3>
                        <ul class="recent-posts-list">
                            <!-- RECENT_POSTS_PLACEHOLDER -->
                        </ul>
                    </div>

                    <div class="sidebar-section">
                        <h3 class="sidebar-title">Categories</h3>
                        <div class="categories-list">
                            <!-- CATEGORIES_PLACEHOLDER -->
                        </div>
                    </div>

                    <div class="sidebar-section">
                        <h3 class="sidebar-title">Subscribe</h3>
                        <p class="sidebar-text">Stay updated with our latest posts.</p>
                        <a href="./rss.xml" class="rss-subscribe-link" target="_blank">
                            <i class="fas fa-rss"></i> Subscribe via RSS
                        </a>
                    </div>
                </div>
            </aside>

            <!-- Blog Article -->
            <main class="blog-main-content">
                <article class="blog-article">
                    {{{CONTENT}}}
                </article>

                <!-- Post Navigation -->
                <div class="post-navigation">
                    <!-- PREVIOUS_POST_PLACEHOLDER -->
                    <!-- NEXT_POST_PLACEHOLDER -->
                </div>
            </main>
        </div>
    </div>

    <!-- Back to Home Button -->
    <a href="../index.html" class="back-to-home">
        <i class="fas fa-arrow-left"></i> Back to Portfolio
    </a>

    <script>
        // Theme switching functionality (same as main site)
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const htmlElement = document.documentElement;

        const currentTheme = localStorage.getItem('theme') || 'light';
        htmlElement.setAttribute('data-theme', currentTheme);
        updateThemeIcon(currentTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });

        function updateThemeIcon(theme) {
            themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }

        // Format date helper for JavaScript
        function formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        }
    </script>
</body>
</html>'''

def generate_blog_index_template():
    """Generate the HTML template for blog index/main page"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - Thamilselven</title>
    <meta name="description" content="Latest articles and insights from Thamilselven's software engineering journey">
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Blog - Thamilselven">
    <meta property="og:description" content="Latest articles and insights from Thamilselven's software engineering journey">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tselven.com/blog/index.html">
    <meta property="og:image" content="https://tselven.com/thamilselven.jpg">
    <meta property="og:site_name" content="Thamilselven's Blog">
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Blog - Thamilselven">
    <meta name="twitter:description" content="Latest articles and insights from Thamilselven's software engineering journey">
    <meta name="twitter:image" content="https://tselven.com/thamilselven.jpg">
    <link rel="stylesheet" href="../style.css">
    <link rel="stylesheet" href="../blog/blog.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;500;700&display=swap" rel="stylesheet">
</head>
<body>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
        <i class="fas fa-moon" id="themeIcon"></i>
    </button>

    <div class="bg-animation">
        <div class="floating-shape shape-1"></div>
        <div class="floating-shape shape-2"></div>
        <div class="floating-shape shape-3"></div>
        <div class="floating-shape shape-4"></div>
    </div>

    <div class="card blog-index-card">
        <header class="blog-index-header">
            <h1 class="blog-index-title">My Blog</h1>
            <p class="blog-index-subtitle">Sharing insights, tutorials, and thoughts on software engineering</p>
        </header>

        <div class="blog-content-wrapper">
            <aside class="blog-sidebar">
                <div class="sidebar-content">
                    <div class="blog-profile">
                        <img src="../thamilselven.jpg" alt="Thamilselven" class="blog-profile-img">
                        <h3 class="blog-author-name">Thamilselven</h3>
                        <p class="blog-author-title">Software Engineer | Backend & DevOps</p>
                    </div>

                    <div class="sidebar-section">
                        <h3 class="sidebar-title">About This Blog</h3>
                        <p class="sidebar-text">Welcome to my personal blog where I share my experiences, learnings, and insights about software engineering, backend development, and DevOps.</p>
                    </div>

                    <div class="sidebar-section">
                        <h3 class="sidebar-title">Categories</h3>
                        <div class="categories-list">
                            <!-- CATEGORIES_PLACEHOLDER -->
                        </div>
                    </div>

                    <div class="sidebar-section">
                        <h3 class="sidebar-title">Subscribe</h3>
                        <p class="sidebar-text">Stay updated with our latest posts.</p>
                        <a href="./rss.xml" class="rss-subscribe-link" target="_blank">
                            <i class="fas fa-rss"></i> Subscribe via RSS
                        </a>
                    </div>
                </div>
            </aside>

            <main class="blog-main-content">
                <div class="blog-posts-grid">
                    <!-- POSTS_PLACEHOLDER -->
                </div>
            </main>
        </div>
    </div>

    <!-- Back to Home Button -->
    <a href="../index.html" class="back-to-home">
        <i class="fas fa-arrow-left"></i> Back to Portfolio
    </a>

    <script>
        // Theme switching functionality (same as main site)
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const htmlElement = document.documentElement;

        const currentTheme = localStorage.getItem('theme') || 'light';
        htmlElement.setAttribute('data-theme', currentTheme);
        updateThemeIcon(currentTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });

        function updateThemeIcon(theme) {
            themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }

        // Format date helper for JavaScript
        function formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        }
    </script>
</body>
</html>'''

def simple_format_date(date_obj):
    """Simple date formatting function"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except ValueError:
            try:
                date_obj = datetime.strptime(date_obj[:19], '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                date_obj = datetime.now()
    elif isinstance(date_obj, datetime):
        pass
    else:
        date_obj = datetime.now()
    
    return date_obj.strftime('%B %d, %Y')

def generate_blog_post(output_dir, post_data, all_posts, recent_count=5):
    """Generate HTML for a single blog post"""
    # Find previous and next posts
    current_index = all_posts.index(post_data)
    previous_post = all_posts[current_index + 1] if current_index + 1 < len(all_posts) else None
    next_post = all_posts[current_index - 1] if current_index > 0 else None
    
    # Get recent posts
    recent_posts = all_posts[:recent_count] if len(all_posts) >= recent_count else all_posts
    
    # Get all unique categories
    all_categories = set()
    for post in all_posts:
        if 'tags' in post['metadata']:
            all_categories.update(post['metadata']['tags'])
    all_categories = sorted(list(all_categories))
    
    # Load the template
    template = generate_blog_html_template()
    
    # Replace placeholders
    html_content = template.replace('{{TITLE}}', post_data['metadata']['title'])
    html_content = html_content.replace('{{DESCRIPTION}}', post_data['metadata']['description'])
    html_content = html_content.replace('{{{CONTENT}}}', post_data['content'])
    html_content = html_content.replace('{{SLUG}}', post_data['slug'])
    
    # Handle og:image - use image from frontmatter if provided, otherwise default
    og_image = post_data['metadata'].get('image', 'https://tselven.com/thamilselven.jpg')
    html_content = html_content.replace('{{OG_IMAGE}}', og_image)
    
    # Format date
    formatted_date = simple_format_date(post_data['metadata']['date'])
    html_content = html_content.replace('{{DATE}}', formatted_date)
    
    # Handle tags
    if 'tags' in post_data['metadata'] and post_data['metadata']['tags']:
        tags_html = ''.join([f'<span class="blog-tag">{tag}</span>' for tag in post_data['metadata']['tags']])
        html_content = html_content.replace('<!-- TAGS_PLACEHOLDER -->', f'<div class="blog-tags">{tags_html}</div>')
    else:
        html_content = html_content.replace('<!-- TAGS_PLACEHOLDER -->', '')
    
    # Insert recent posts
    recent_posts_html = ''
    for post in recent_posts:
        if post != post_data:  # Don't include current post in recent posts
            post_date = simple_format_date(post['metadata']['date'])
            recent_posts_html += f'''
        <li class="recent-post-item">
            <a href="{post['slug']}.html" class="recent-post-link">{post['metadata']['title']}</a>
            <span class="recent-post-date">{post_date}</span>
        </li>'''
    
    html_content = html_content.replace('<!-- RECENT_POSTS_PLACEHOLDER -->', recent_posts_html)
    
    # Insert categories
    categories_html = ''.join([f'<a href="#" class="category-link">{cat}</a>' for cat in all_categories])
    html_content = html_content.replace('<!-- CATEGORIES_PLACEHOLDER -->', categories_html)
    
    # Handle post navigation
    prev_html = ''
    if previous_post:
        prev_html = f'''<a href="{previous_post['slug']}.html" class="nav-link prev-link">
            <i class="fas fa-arrow-left"></i>
            <span>{previous_post['metadata']['title']}</span>
        </a>'''
    
    next_html = ''
    if next_post:
        next_html = f'''<a href="{next_post['slug']}.html" class="nav-link next-link">
            <span>{next_post['metadata']['title']}</span>
            <i class="fas fa-arrow-right"></i>
        </a>'''
    
    html_content = html_content.replace('<!-- PREVIOUS_POST_PLACEHOLDER -->', prev_html)
    html_content = html_content.replace('<!-- NEXT_POST_PLACEHOLDER -->', next_html)
    
    # Replace Disqus placeholder (this would be configured in production)
    html_content = html_content.replace('{{DISQUS_SHORTNAME}}', 'your-disqus-shortname')
    
    # Write the output file
    output_file = os.path.join(output_dir, f"{post_data['slug']}.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated blog post: {output_file}")

def generate_blog_index(output_dir, all_posts):
    """Generate the main blog index page"""
    # Get all unique categories
    all_categories = set()
    for post in all_posts:
        if 'tags' in post['metadata']:
            all_categories.update(post['metadata']['tags'])
    all_categories = sorted(list(all_categories))
    
    # Load the template
    template = generate_blog_index_template()
    
    # Generate posts HTML
    posts_html = ''
    for post in all_posts:
        post_date = simple_format_date(post['metadata']['date'])
        
        tags_html = ''
        if 'tags' in post['metadata'] and post['metadata']['tags']:
            tags_html = ''.join([f'<span class="blog-tag">{tag}</span>' for tag in post['metadata']['tags']])
        
        post_html = f'''
        <article class="blog-post-card">
            <h2 class="blog-post-card-title">
                <a href="{post['slug']}.html">{post['metadata']['title']}</a>
            </h2>
            <div class="blog-post-meta">
                <span class="blog-date"><i class="far fa-calendar"></i> {post_date}</span>
                {f'<div class="blog-tags">{tags_html}</div>' if tags_html else ''}
            </div>
            <p class="blog-post-excerpt">{post['metadata']['description']}</p>
            <a href="{post['slug']}.html" class="read-more-link">Read More <i class="fas fa-arrow-right"></i></a>
        </article>'''
        posts_html += post_html
    
    # Generate categories HTML
    categories_html = ''
    if all_categories:
        categories_html = ''.join([f'<a href="#" class="category-link">{cat}</a>' for cat in all_categories])
    
    # Replace placeholders
    html_content = template
    html_content = html_content.replace('<!-- POSTS_PLACEHOLDER -->', posts_html)
    html_content = html_content.replace('<!-- CATEGORIES_PLACEHOLDER -->', categories_html)
    
    # Write the output file
    output_file = os.path.join(output_dir, 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated blog index: {output_file}")

def generate_sitemap(posts, base_url="https://tselven.com"):
    """Generate sitemap.xml for blog posts and main site pages"""
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add main site pages
    sitemap_content += f'  <url>\n    <loc>{base_url}/index.html</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    
    sitemap_content += f'  <url>\n    <loc>{base_url}/privacy.html</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.5</priority>\n  </url>\n'
    
    sitemap_content += f'  <url>\n    <loc>{base_url}/terms.html</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.5</priority>\n  </url>\n'
    
    # Add main blog page
    sitemap_content += f'  <url>\n    <loc>{base_url}/blog/index.html</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    
    # Add each blog post
    for post in posts:
        lastmod = post['metadata']['date'].strftime('%Y-%m-%d')
        sitemap_content += f'  <url>\n    <loc>{base_url}/blog/{post["slug"]}.html</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
    
    sitemap_content += '</urlset>'
    
    return sitemap_content

def generate_rss_feed(posts, base_url="https://tselven.com"):
    """Generate RSS feed for blog posts"""
    rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content += '<rss version="2.0">\n'
    rss_content += '  <channel>\n'
    rss_content += '    <title>Thamilselven - Blog</title>\n'
    rss_content += '    <description>Latest articles and insights from Thamilselven\'s software engineering journey</description>\n'
    rss_content += f'    <link>{base_url}/blog/</link>\n'
    rss_content += f'    <pubDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate>\n'
    rss_content += f'    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")}</lastBuildDate>\n'
    rss_content += '    <language>en-US</language>\n'
    
    # Add each blog post
    for post in posts[:10]:  # Limit to 10 most recent posts
        pub_date = post['metadata']['date'].strftime("%a, %d %b %Y %H:%M:%S %z")
        description = post['metadata']['description']
        link = f"{base_url}/blog/{post['slug']}.html"
        
        rss_content += '    <item>\n'
        rss_content += f'      <title><![CDATA[{post["metadata"]["title"]}]]></title>\n'
        rss_content += f'      <description><![CDATA[{description}]]></description>\n'
        rss_content += f'      <link>{link}</link>\n'
        rss_content += f'      <guid isPermaLink="true">{link}</guid>\n'
        rss_content += f'      <pubDate>{pub_date}</pubDate>\n'
        rss_content += '    </item>\n'
    
    rss_content += '  </channel>\n'
    rss_content += '</rss>'
    
    return rss_content

def generate_robots_txt(base_url="https://tselven.com"):
    """Generate robots.txt file"""
    robots_content = f"User-agent: *\nDisallow:\n\nSitemap: {base_url}/sitemap.xml"
    return robots_content

def main():
    # Define paths
    posts_dir = './blog/posts'
    output_dir = './blog'
    sitemap_path = './sitemap.xml'
    rss_path = './blog/rss.xml'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all blog posts
    print("Loading blog posts...")
    posts = load_blog_posts(posts_dir)
    print(f"Loaded {len(posts)} blog posts")
    
    if not posts:
        print("No blog posts found. Creating a sample post...")
        sample_post = """---
title: "Welcome to My Blog"
date: "{}"
description: "Welcome to my personal blog where I share my experiences and insights about software engineering."
tags: ["blog", "welcome"]
---

# Welcome to My Blog

Hello and welcome to my personal blog! This is the place where I'll be sharing my thoughts, experiences, and insights about software engineering, backend development, DevOps, and more.

## What to Expect

In this blog, you'll find articles about:

- Software engineering best practices
- Backend development techniques
- DevOps and infrastructure topics
- Cloud technologies and services
- Personal projects and learnings
- Tutorials and guides

Stay tuned for more content coming soon!

""".format(datetime.now().isoformat())
        
        sample_path = os.path.join(posts_dir, 'welcome.md')
        os.makedirs(posts_dir, exist_ok=True)
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(sample_post)
        
        posts = load_blog_posts(posts_dir)
    
    # Generate blog index page
    print("Generating blog index page...")
    generate_blog_index(output_dir, posts)
    
    # Generate individual blog posts
    print("Generating individual blog posts...")
    for post in posts:
        generate_blog_post(output_dir, post, posts)
    
    # Generate sitemap
    print("Generating sitemap...")
    sitemap_content = generate_sitemap(posts)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    # Generate RSS feed
    print("Generating RSS feed...")
    rss_content = generate_rss_feed(posts)
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    # Generate robots.txt
    print("Generating robots.txt...")
    robots_path = './robots.txt'
    robots_content = generate_robots_txt()
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print("Blog generation complete!")
    print(f"- Generated {len(posts)} blog posts")
    print(f"- Created blog index at {os.path.join(output_dir, 'index.html')}")
    print(f"- Created sitemap at {sitemap_path}")
    print(f"- Created RSS feed at {rss_path}")
    print(f"- Created robots.txt at {robots_path}")

if __name__ == "__main__":
    main()