document.addEventListener('DOMContentLoaded', () => {
    const scrollBtn = document.getElementById('scroll-btn');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('nav ul li a');
    let currentSection = 0;

    // Update button text based on the current section
    function updateButtonText() {
        const isAtEnd = currentSection === sections.length - 1;
        scrollBtn.innerHTML = isAtEnd ? "Scroll up!" : "Scroll down!";
    }

    // Function to scroll to the next section
    function scrollToNextSection() {
        if (currentSection < sections.length - 1) {
            currentSection++;
            sections[currentSection].scrollIntoView({
                behavior: 'smooth'
            });
            updateButtonText();
        }
    }

    // Function to scroll to the previous section
    function scrollToPreviousSection() {
        if (currentSection > 0) {
            currentSection--;
            sections[currentSection].scrollIntoView({
                behavior: 'smooth'
            });
            updateButtonText();
        }
    }

    // Handle button click event to scroll up or down
    scrollBtn.addEventListener('click', (e) => {
        e.preventDefault();

        if (currentSection === sections.length - 1) {
            scrollToPreviousSection();
        } else {
            scrollToNextSection();
        }
    });

    // Handle manual scrolling and update the button text
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        const sectionHeight = window.innerHeight / 2;

        sections.forEach((section, index) => {
            if (scrollPosition >= section.offsetTop - sectionHeight && scrollPosition < section.offsetTop + section.offsetHeight - sectionHeight) {
                currentSection = index;
            }
        });

        updateButtonText();
    });

    // Add click event listener to the navigation links for smooth scrolling
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();

            const targetId = link.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            targetSection.scrollIntoView({
                behavior: 'smooth'
            });

            // Update current section index based on the section ID
            currentSection = Array.from(sections).findIndex(section => section.id === targetId);
            updateButtonText();
        });
    });

    // Initialize button text on page load
    updateButtonText();
});