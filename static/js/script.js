document.addEventListener('DOMContentLoaded', () => {
    const scrollBtn = document.getElementById('scroll-btn');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav ul li a');
    let currentSection = 0;

    // Update button visibility based on the current section
    function updateButtonVisibility() {
        const isAtEnd = currentSection === sections.length - 1;

        if (isAtEnd) {
            scrollBtn.classList.add('hidden');
        } else {
            scrollBtn.classList.remove('hidden');
        }
    }

    // Scroll to the next section
    function scrollToNextSection() {
        if (currentSection < sections.length - 1) {
            currentSection++;
            sections[currentSection].scrollIntoView({
                behavior: 'smooth'
            });
            updateButtonVisibility();
        }
    }

    // Scroll to the top of the page
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        currentSection = 0;
        updateButtonVisibility();
    }

    // Button click handler
    scrollBtn.addEventListener('click', (e) => {
        e.preventDefault();

        if (currentSection === sections.length - 1) {
            scrollToTop();
        } else {
            scrollToNextSection();
        }
    });

    // Update section index on scroll
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        const sectionHeight = window.innerHeight / 2;

        sections.forEach((section, index) => {
            if (
                scrollPosition >= section.offsetTop - sectionHeight &&
                scrollPosition < section.offsetTop + section.offsetHeight - sectionHeight
            ) {
                currentSection = index;
            }
        });

        updateButtonVisibility();
    });

    // Smooth scroll via nav links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const targetId = link.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            targetSection.scrollIntoView({
                behavior: 'smooth'
            });

            currentSection = Array.from(sections).findIndex(section => section.id === targetId);
            updateButtonVisibility();
        });
    });

    // Initial setup
    updateButtonVisibility();
});
