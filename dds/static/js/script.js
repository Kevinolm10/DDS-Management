document.addEventListener('DOMContentLoaded', () => {
    const scrollBtn = document.getElementById('scroll-btn');
    const sections = document.querySelectorAll('section'); // All sections
    let currentSection = 0; // Track which section the user is on

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
            updateButtonText(); // Update button text after scroll
        }
    }

    // Function to scroll to the previous section
    function scrollToPreviousSection() {
        if (currentSection > 0) {
            currentSection--;
            sections[currentSection].scrollIntoView({
                behavior: 'smooth'
            });
            updateButtonText(); // Update button text after scroll
        }
    }

    // Handle button click event to scroll up or down
    scrollBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent the default anchor action

        if (currentSection === sections.length - 1) {
            scrollToPreviousSection(); // Scroll up if at the last section
        } else {
            scrollToNextSection(); // Scroll down to the next section
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

        updateButtonText(); // Update button text based on scroll position
    });

    // Initialize button text on page load
    updateButtonText();
});