function updateBurgerDropdown() {
    const dropdown = document.getElementById('burgerDropdown');
    const navMenu = document.querySelector('.nav-menu');
    if (!dropdown || !navMenu) return;
    dropdown.innerHTML = '';
    // Ajoute les liens masqués dans le dropdown
    navMenu.querySelectorAll('li').forEach(li => {
        const style = window.getComputedStyle(li);
        if (style.display === 'none') {
            const a = li.querySelector('a');
            if (a) {
                const clone = a.cloneNode(true);
                dropdown.appendChild(clone);
            }
        }
    });
}

const burgerBtn = document.getElementById('burgerBtn');
const burgerDropdown = document.getElementById('burgerDropdown');
if (burgerBtn && burgerDropdown) {
    burgerBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        updateBurgerDropdown();
        burgerDropdown.style.display = burgerDropdown.style.display === 'flex' ? 'none' : 'flex';
    });
    document.addEventListener('click', function(e) {
        if (!burgerDropdown.contains(e.target) && e.target !== burgerBtn) {
            burgerDropdown.style.display = 'none';
        }
    });
    window.addEventListener('resize', function() {
        burgerDropdown.style.display = 'none';
    });
} 