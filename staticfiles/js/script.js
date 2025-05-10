document.addEventListener('DOMContentLoaded', () => {
    const scrollBtn = document.getElementById('scroll-btn');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav ul li a');
    const header = document.querySelector('header'); // Hämta headern
    const headerHeight = header.offsetHeight; // Hämta headerns höjd

    let currentSection = 0;

    // Uppdatera knappens synlighet baserat på den aktuella sektionen
    function updateButtonVisibility() {
        const isAtEnd = currentSection === sections.length - 1;

        if (isAtEnd) {
            scrollBtn.classList.add('hidden');
        } else {
            scrollBtn.classList.remove('hidden');
        }
    }

    // Scrolla till nästa sektion
    function scrollToNextSection() {
        if (currentSection < sections.length - 1) {
            currentSection++;
            sections[currentSection].scrollIntoView({
                behavior: 'smooth'
            });
            updateButtonVisibility();
        }
    }

    // Scrolla till toppen av sidan
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

    // Uppdatera sektionens index när man scrollar
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

    // Smidig scroll när man klickar på navigeringslänkar
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const targetId = link.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            // Scrolla till sektionen och ta hänsyn till headerns höjd
            window.scrollTo({
                top: targetSection.offsetTop - headerHeight, // Subtrahera headerns höjd för korrekt position
                behavior: 'smooth'
            });

            currentSection = Array.from(sections).findIndex(section => section.id === targetId);
            updateButtonVisibility();
        });
    });

    // Initial setup
    updateButtonVisibility();
});
