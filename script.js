// Global variables
let allProjects = [];
let allReviews = [];
let showAllProjects = false;
let showAllReviews = false;

// WhatsApp Popup Toggle
function toggleWA() {
    const popup = document.getElementById("waPopup");
    popup.style.display = popup.style.display === "block" ? "none" : "block";
}

// Load projects from external JSON
async function loadProjects() {
    try {
        const response = await fetch('projects.json');
        allProjects = await response.json();

        // Generate dynamic filters from unique categories
        generateProjectFilters(allProjects);

        // Render initial projects (first 3)
        renderProjects(allProjects, 'all');
    } catch (error) {
        console.error('Error loading projects:', error);
        document.getElementById('projectsGrid').innerHTML = '<p style="color: var(--text-secondary); text-align: center;">Failed to load projects</p>';
    }
}

// Generate project filters dynamically from categories
function generateProjectFilters(projects) {
    const categories = ['all', ...new Set(projects.map(p => p.category))];
    const filtersContainer = document.querySelector('.project-filters');
    filtersContainer.innerHTML = '';

    categories.forEach((category, index) => {
        const btn = document.createElement('button');
        btn.className = `filter-btn ${index === 0 ? 'active' : ''}`;
        btn.dataset.filter = category;
        btn.textContent = category.charAt(0).toUpperCase() + category.slice(1);

        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            showAllProjects = false; // Reset when filter changes
            renderProjects(allProjects, category);
        });

        filtersContainer.appendChild(btn);
    });
}

// Load reviews from external JSON
async function loadReviews() {
    try {
        const response = await fetch('reviews.json');
        allReviews = await response.json();
        renderTestimonials(allReviews);
    } catch (error) {
        console.error('Error loading reviews:', error);
        document.getElementById('testimonialsGrid').innerHTML = '<p style="color: var(--text-secondary); text-align: center;">Failed to load testimonials</p>';
    }
}

// Render projects with "See More" functionality
function renderProjects(projects, filter = 'all') {
    const grid = document.getElementById('projectsGrid');
    grid.innerHTML = '';

    const filteredProjects = filter === 'all'
        ? projects
        : projects.filter(p => p.category === filter);

    const projectsToShow = showAllProjects ? filteredProjects : filteredProjects.slice(0, 4);

    projectsToShow.forEach(project => {
        const card = document.createElement('div');
        card.className = 'project-card';
        card.innerHTML = `
            <div class="project-header">
                <div class="project-icon">
                    <i class="${project.icon}"></i>
                </div>
                <h3 class="project-title">${project.title}</h3>
            </div>
            <p class="project-description">${project.description}</p>
            <div class="project-tags">
                ${project.tags.map(tag => `<span class="project-tag">${tag}</span>`).join('')}
            </div>
            <div class="project-links">
                ${project.github ? `<a href="${project.github}" class="project-link" target="_blank"><i class="fab fa-github"></i> Code</a>` : ''}
                ${project.demo ? `<a href="${project.demo}" class="project-link" target="_blank"><i class="fas fa-external-link-alt"></i> Demo</a>` : ''}
            </div>
        `;
        grid.appendChild(card);
    });

    // Add "See More" button if there are more than 4 projects
    if (filteredProjects.length > 4) {
        const seeMoreBtn = document.createElement('button');
        seeMoreBtn.className = 'see-more-btn';
        seeMoreBtn.innerHTML = showAllProjects
            ? '<i class="fas fa-chevron-up"></i> Show Less'
            : `<i class="fas fa-chevron-down"></i> See More (${filteredProjects.length - 4} more)`;

        seeMoreBtn.addEventListener('click', () => {
            showAllProjects = !showAllProjects;
            renderProjects(projects, filter);
        });

        grid.appendChild(seeMoreBtn);
    }
}

// Render testimonials with "See More" functionality
function renderTestimonials(testimonials) {
    const grid = document.getElementById('testimonialsGrid');
    grid.innerHTML = '';

    const testimonialsToShow = showAllReviews ? testimonials : testimonials.slice(0, 4);

    testimonialsToShow.forEach(testimonial => {
        const card = document.createElement('div');
        card.className = 'testimonial-card';

        const platformIcon = testimonial.platform === 'linkedin'
            ? 'fab fa-linkedin'
            : 'fab fa-google';

        const stars = Array(testimonial.rating).fill('<i class="fas fa-star"></i>').join('');

        card.innerHTML = `
            <div class="testimonial-header">
                <div class="testimonial-avatar">${testimonial.avatar}</div>
                <div class="testimonial-info">
                    <div class="testimonial-name">${testimonial.name}</div>
                    <div class="testimonial-position">${testimonial.position}</div>
                </div>
                <div class="testimonial-platform">
                    <i class="${platformIcon}"></i>
                </div>
            </div>
            <div class="testimonial-rating">${stars}</div>
            <p class="testimonial-content">"${testimonial.content}"</p>
        `;
        grid.appendChild(card);
    });

    // Add "See More" button if there are more than 4 testimonials
    if (testimonials.length > 4) {
        const seeMoreBtn = document.createElement('button');
        seeMoreBtn.className = 'see-more-btn';
        seeMoreBtn.innerHTML = showAllReviews
            ? '<i class="fas fa-chevron-up"></i> Show Less'
            : `<i class="fas fa-chevron-down"></i> See More (${testimonials.length - 4} more)`;

        seeMoreBtn.addEventListener('click', () => {
            showAllReviews = !showAllReviews;
            renderTestimonials(testimonials);
        });

        grid.appendChild(seeMoreBtn);
    }
}

// Theme Switcher
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

// Create floating particles
for (let i = 0; i < 15; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 8 + 's';
    particle.style.animationDuration = (Math.random() * 5 + 6) + 's';
    document.body.appendChild(particle);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    loadReviews();
});

// Mobile Navbar Toggle
function toggleNav() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    navbar.classList.toggle('show');
    navToggle.classList.toggle('active');
}

// Close navbar on mobile when clicking a link
function closeNavOnMobile() {
    if (window.innerWidth <= 768) {
        const navbar = document.getElementById('navbar');
        const navToggle = document.getElementById('navToggle');
        navbar.classList.remove('show');
        navToggle.classList.remove('active');
    }
}

// Close navbar when clicking outside
document.addEventListener('click', function(e) {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    
    if (window.innerWidth <= 768) {
        if (!navbar.contains(e.target) && !navToggle.contains(e.target)) {
            navbar.classList.remove('show');
            navToggle.classList.remove('active');
        }
    }
});

// Scroll to Top Button
const scrollToTopBtn = document.getElementById('scrollToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.add('show');
    } else {
        scrollToTopBtn.classList.remove('show');
    }
});

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Smooth scroll for navbar links
document.querySelectorAll('.navbar a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Add IDs to sections for navbar navigation
document.addEventListener('DOMContentLoaded', () => {
    // Add ID to card for home
    if (document.querySelector('.card')) {
        document.querySelector('.card').id = 'home';
    }
    
    // Add ID to about section
    if (document.querySelector('.about')) {
        document.querySelector('.about').id = 'about';
    }
    
    // Add ID to services section
    if (document.querySelector('.services')) {
        document.querySelector('.services').id = 'services';
    }
    
    // Add ID to projects section
    if (document.querySelector('.projects')) {
        document.querySelector('.projects').id = 'projects';
    }
    
    // Add ID to skills section
    if (document.querySelector('.skills')) {
        document.querySelector('.skills').id = 'skills';
    }
});