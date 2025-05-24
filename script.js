document.addEventListener('DOMContentLoaded', () => {
    // Add animation to cards when they come into view
    const cards = document.querySelectorAll('.card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        observer.observe(card);
    });

    // Enhanced download button effects
    const downloadBtn = document.querySelector('.download-btn');
    const downloadCard = document.querySelector('.download-card');
    
    if (downloadBtn && downloadCard) {
        // Add hover effect to download button
        downloadBtn.addEventListener('mouseover', () => {
            downloadBtn.style.transform = 'scale(1.05)';
            downloadCard.style.transform = 'scale(1.02)';
        });

        downloadBtn.addEventListener('mouseout', () => {
            downloadBtn.style.transform = 'scale(1)';
            downloadCard.style.transform = 'scale(1)';
        });

        // Add click effect with ripple
        downloadBtn.addEventListener('click', (e) => {
            const rect = downloadBtn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            downloadBtn.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);

            downloadBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                downloadBtn.style.transform = 'scale(1)';
            }, 200);
        });
    }

    // Animate footer decorations
    const decorations = document.querySelectorAll('.decoration-item');
    decorations.forEach((decoration, index) => {
        decoration.style.animationDelay = `${index * 0.5}s`;
    });

    // Add parallax effect to header
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        if (header) {
            header.style.transform = `translateY(${scrolled * 0.5}px)`;
            header.style.opacity = 1 - (scrolled * 0.003);
        }
    });

    // Add hover effect to tech stack items
    const techItems = document.querySelectorAll('.tech-item');
    techItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.style.transform = 'scale(1.05)';
        });
        item.addEventListener('mouseout', () => {
            item.style.transform = 'scale(1)';
        });
    });

    // Add hover effect to social links
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.transform = 'translateY(-3px)';
        });
        link.addEventListener('mouseout', () => {
            link.style.transform = 'translateY(0)';
        });
    });

    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}); 