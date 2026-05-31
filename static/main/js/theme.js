function toggleTheme() {
    document.body.classList.toggle('light-theme');
    if (document.body.classList.contains('light-theme')) {
        localStorage.setItem('theme', 'light');
        document.cookie = "theme=light; path=/";
    } else {
        localStorage.setItem('theme', 'dark');
        document.cookie = "theme=dark; path=/";
    }
    window.location.reload();
}

if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-theme');
}
