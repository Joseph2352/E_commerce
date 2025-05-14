function scrollItems(id, direction) {
    const container = document.getElementById(id);
    if (!container) return;
    
    const scrollAmount = 220;
    container.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}

function checkScroll(id) {
    const container = document.getElementById(id);
    if (!container) return;

    const prevButton = container.parentElement.querySelector('.prev');
    const nextButton = container.parentElement.querySelector('.next');

    prevButton.classList.toggle('hidden', container.scrollLeft === 0);
    nextButton.classList.toggle('hidden', container.scrollLeft + container.clientWidth >= container.scrollWidth);
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.item-category, .items').forEach((slider) => {
        checkScroll(slider.id);
    });
});

window.addEventListener("resize", () => {
    document.querySelectorAll('.item-category, .items').forEach((slider) => {
        checkScroll(slider.id);
    });
});
