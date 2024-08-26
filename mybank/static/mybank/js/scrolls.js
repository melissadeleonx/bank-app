// Scroll animation of sections using the handlescroll function, adapted from my previous projects
// Index frontpage animation - visible element as well as transform css elements
document.addEventListener('DOMContentLoaded', function () {
    const card = document.getElementById('dashboardCard-section');
    const welcomeSection = document.getElementById('welcomeSection');
    const cardColumn = document.getElementById('cardColumn');
    const textColumn = document.getElementById('textColumn');
    const cardColumnMobile = document.getElementById('cardColumnMobile');
    const textColumnMobile = document.getElementById('textColumnMobile');

    function handleScroll() {
        const cardPosition = card.getBoundingClientRect().top;
        const sectionPosition = welcomeSection.getBoundingClientRect().top;
        const cardColumnPosition = cardColumn.getBoundingClientRect().top;
        const textColumnPosition = textColumn.getBoundingClientRect().top;
        const cardColumnMobilePosition = cardColumnMobile.getBoundingClientRect().top;
        const textColumnMobilePosition = textColumnMobile.getBoundingClientRect().top;
        const viewportHeight = window.innerHeight;


        // Handle welcomeSection visibility
        if (sectionPosition < viewportHeight * 0.75) {
            welcomeSection.classList.add('visible');
        } else {
            welcomeSection.classList.remove('visible');
        }

        // Handle card visibility
        if (cardPosition < viewportHeight * 0.75) {
            card.classList.add('visible');
        } else {
            card.classList.remove('visible');
        }

        // Handle cardColumn visibility
        if (cardColumnPosition < viewportHeight * 0.75) {
            cardColumn.classList.add('visible');
        } else {
            cardColumn.classList.remove('visible');
        }

        // Handle textColumn visibility
        if (textColumnPosition < viewportHeight * 0.75) {
            textColumn.classList.add('visible');
        } else {
            textColumn.classList.remove('visible');
        }

        // Handle cardColumnMobile visibility
        if (cardColumnMobilePosition < viewportHeight * 0.75) {
            cardColumnMobile.classList.add('visible');
        } else {
            cardColumnMobile.classList.remove('visible');
        }

        // Handle textColumnMobile visibility
        if (textColumnMobilePosition < viewportHeight * 0.75) {
            textColumnMobile.classList.add('visible');
        } else {
            textColumnMobile.classList.remove('visible');
        }

        }

    window.addEventListener('scroll', handleScroll);

    handleScroll();
});
