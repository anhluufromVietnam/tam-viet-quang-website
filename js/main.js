// Tâm Việt Quang - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Smooth Scroll for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    mobileMenuBtn.classList.remove('active');
                }
            }
        });
    });

    // Navbar Background on Scroll
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });

    // Intersection Observer for Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    document.querySelectorAll('.sector-card, .feature-card, .product-card, .stat-item').forEach(el => {
        observer.observe(el);
    });

    // Form Submission Handler
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                company: formData.get('company'),
                message: formData.get('message'),
                timestamp: new Date().toISOString()
            };
            
            // Save to localStorage
            let contacts = JSON.parse(localStorage.getItem('tvq_contacts') || '[]');
            contacts.push(data);
            localStorage.setItem('tvq_contacts', JSON.stringify(contacts));
            
            // Log to console for debugging
            console.log('Contact saved:', data);
            console.log('All contacts:', contacts);
            
            // Show success message
            const successMsg = document.createElement('div');
            successMsg.className = 'success-message';
            successMsg.innerHTML = `
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: linear-gradient(135deg, #4B4ACB 0%, #4CAF75 100%);
                    color: white;
                    padding: 2rem 3rem;
                    border-radius: 1rem;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                    z-index: 10000;
                    text-align: center;
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                    <h3 style="margin-bottom: 0.5rem;">Gửi thành công!</h3>
                    <p style="opacity: 0.9;">Cảm ơn bạn đã liên hệ. Chúng tôi sẽ phản hồi sớm nhất.</p>
                </div>
            `;
            document.body.appendChild(successMsg);
            
            // Remove message after 3 seconds
            setTimeout(() => {
                successMsg.remove();
            }, 3000);
            
            // Reset form
            this.reset();
        });
    }

    // Counter Animation for Stats
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }
        
        updateCounter();
    }

    // Animate stats when visible
    const statsSection = document.querySelector('.stats');
    let statsAnimated = false;

    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !statsAnimated) {
                statsAnimated = true;
                
                // Animate the 89% stat
                const statNumbers = document.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const text = stat.textContent;
                    if (text.includes('%')) {
                        stat.textContent = '0%';
                        animateCounter(stat, 89);
                        setTimeout(() => stat.textContent = '89%', 2000);
                    }
                });
            }
        });
    }, { threshold: 0.5 });

    if (statsSection) {
        statsObserver.observe(statsSection);
    }

    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        .sector-card,
        .feature-card,
        .product-card,
        .stat-item {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        .nav-links.active {
            display: flex !important;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            flex-direction: column;
            background: white;
            padding: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            gap: 1rem;
        }
        
        .mobile-menu-btn.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .mobile-menu-btn.active span:nth-child(2) {
            opacity: 0;
        }
        
        .mobile-menu-btn.active span:nth-child(3) {
            transform: rotate(-45deg) translate(5px, -5px);
        }
    `;
    document.head.appendChild(style);

    console.log('🚀 Tâm Việt Quang website loaded successfully!');
});
