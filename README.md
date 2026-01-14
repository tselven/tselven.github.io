# Personal Portfolio Website

A modern, responsive portfolio website featuring a clean design with dark/light mode toggle, animated elements, and integrated blog system.

## Features

- 🎨 Responsive design with mobile-first approach
- 🌙 Dark/Light mode toggle with persistent preference
- 📱 Mobile-friendly navigation
- 📝 Integrated blog system with Markdown support
- 🔍 SEO optimized with Open Graph meta tags
- 🚀 Fast loading with optimized assets
- 📊 Built-in analytics support (Google Analytics)

## Prerequisites

- Python 3.7+ (for blog system)
- Git
- A web server to host the site

## Installation

1. **Fork the repository:**
    - fork my repository into your github account

2. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-portfolio.git
   cd your-portfolio
   ```

3. **Customize the content:**

   ### Profile Information
   - Replace `thamilselven.jpg` with your own profile photo (recommended size: 400x400px)
   - Update your name, title, and location in `index.html`
   - Modify the description in the `<meta>` tags

   ### Social Links
   Edit the social links section in `index.html`:
   ```html
   <div class="social-links">
       <a href="YOUR_LINKEDIN_URL" class="social-btn" target="_blank" title="LinkedIn">
           <i class="fab fa-linkedin-in"></i>
       </a>
       <!-- Add or remove social links as needed -->
   </div>
   ```

   ### About Section
   Update the content in the "About Me" section with your own information.

   ### Projects Section
   Modify the projects in `projects.json`:
   ```json
   [
       {
           "title": "Your Project Title",
           "description": "Description of your project",
           "technologies": ["Tech1", "Tech2"],
           "links": {
               "live": "https://your-project-url.com",
               "source": "https://github.com/yourusername/your-project"
           }
       }
   ]
   ```

   ### Skills Section
   Update the skills list in `index.html` to reflect your own skills.

## Blog System Setup

The portfolio includes a custom Markdown-based blog system:

1. **Adding Blog Posts:**
   - Create new `.md` files in the `blog/posts/` directory
   - Use the following frontmatter format:
     ```markdown
     ---
     title: "Your Blog Post Title"
     date: "YYYY-MM-DD"
     description: "Brief description of your post"
     tags: ["tag1", "tag2", "tag3"]
     image: "https://example.com/image-url.jpg"  # Optional: for Open Graph tags
     ---
     
     # Your Blog Post Title
     
     Your content here...
     ```

2. **Building the Blog:**
   Run the build script to generate HTML from Markdown:
   ```bash
   python blog/scripts/build_blog.py
   ```

3. **Customizing Blog Templates:**
   - Edit `blog/scripts/build_blog.py` to customize the blog templates
   - Modify `blog/blog.css` to update the blog styling

## Customization Options

### Colors and Theme
Edit the CSS variables in `style.css` to customize the color scheme:
```css
:root {
  --primary: #your-primary-color;
  --secondary: #your-secondary-color;
  --accent: #your-accent-color;
  /* ... other variables */
}
```

### Google Analytics
To enable Google Analytics:
1. Get your GA4 Measurement ID
2. Update the tracking code in `index.html`:
   ```html
   <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_MEASUREMENT_ID"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'YOUR_GA_MEASUREMENT_ID');
   </script>
   ```

## Deployment

### GitHub Pages
1. Push your changes to the `main` branch
2. Go to your repository settings
3. In the "Pages" section, select "Deploy from a branch"
4. Select `main` branch and `/ (root)` folder
5. Click "Save"

### Other Hosting Services
Upload all files to your hosting provider. Make sure to upload:
- All HTML files
- `style.css`
- `script.js`
- `thamilselven.jpg` (or your profile image)
- `blog/` directory and its contents
- `projects.json`
- `reviews.json`

## File Structure

```
your-portfolio/
├── index.html              # Main portfolio page
├── style.css              # Main styles
├── script.js              # Main JavaScript
├── thamilselven.jpg       # Profile image
├── projects.json          # Projects data
├── reviews.json           # Testimonials data
├── LICENSE.md             # License information
├── README.md              # This file
├── blog/                  # Blog system
│   ├── index.html         # Blog homepage
│   ├── blog.css           # Blog styles
│   ├── posts/             # Blog posts in Markdown
│   └── scripts/           # Build scripts
├── privacy.html           # Privacy policy
└── terms.html             # Terms of service
```

## Contributing

Feel free to fork this repository and submit pull requests for improvements.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.