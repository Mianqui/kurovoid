function showAlert(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    let classes = 'toast-message rounded-lg px-4 py-3 text-sm font-medium shadow-lg transition-all duration-300 -translate-y-4 opacity-0 pointer-events-auto ';
    if (type === 'success') {
        classes += 'bg-emerald-950 border border-emerald-800 text-emerald-400';
    } else if (type === 'error') {
        classes += 'bg-red-950 border border-red-800 text-red-400';
    } else {
        classes += 'theme-bg-primary theme-border text-zinc-300';
    }
    toast.className = classes;
    toast.textContent = message;
    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.remove('-translate-y-4', 'opacity-0');
    });

    setTimeout(() => {
        toast.classList.add('opacity-0', '-translate-y-4');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toast-message').forEach(toast => {
        setTimeout(() => {
            toast.classList.add('opacity-0', '-translate-y-4');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    });

    const themeToggleBtn = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;
    const dashLogo = document.getElementById('dashLogo');

    const sunPath = 'M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z';
    const moonPath = 'M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z';
    
    const logoLight = dashLogo?.dataset?.logoLight || '';
    const logoDark = dashLogo?.dataset?.logoDark || '';

    function setTheme(theme) {
        htmlEl.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        if (themeIcon) {
            const path = theme === 'dark' ? sunPath : moonPath;
            themeIcon.querySelector('path')?.setAttribute('d', path);
        }
        if (dashLogo) {
            if (theme === 'light' && logoLight) dashLogo.src = logoLight;
            else if (theme === 'dark' && logoDark) dashLogo.src = logoDark;
        }
    }

    function toggleTheme() {
        const current = htmlEl.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
    }

    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }
});
