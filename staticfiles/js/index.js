document.addEventListener('DOMContentLoaded', () => {
    const scroll = document.querySelector('.scroll-hint a'); // Select only the scroll button
    if (!scroll) return; // Prevent errors if element is missing

    const sections = ['about', 'blog', 'contact-us'];
    let currentSection = 0;

    function updateButtonText() {
        const yellowSection = document.getElementById('contact-us');
        if (!yellowSection) return; // Prevent errors if section doesn't exist

        const isAtYellow = window.scrollY >= yellowSection.offsetTop - (window.innerHeight / 2);
        scroll.innerHTML = isAtYellow ? "Scroll up!" : "Scroll down!";
    }

    window.addEventListener('scroll', updateButtonText);

    scroll.addEventListener('click', (e) => {
        e.preventDefault(); // Prevents default anchor behavior

        currentSection = (currentSection + 1) % sections.length;
        const nextSection = document.getElementById(sections[currentSection]);
        if (!nextSection) return;

        nextSection.scrollIntoView({
            behavior: 'smooth'
        });

        scroll.innerHTML = (currentSection === sections.length - 1) ? "Scroll up!" : "Scroll down!";
    });
});