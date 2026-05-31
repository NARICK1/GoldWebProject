function createSparkles() {
    const container = document.getElementById('summerScene');
    if (!container) return;

    const sparkleCount = 80;

    for (let i = 0; i < sparkleCount; i++) {
        const sparkle = document.createElement('div');
        sparkle.classList.add('sparkle');

        sparkle.style.left = Math.random() * 100 + '%';
        sparkle.style.top = Math.random() * 70 + '%';
        sparkle.style.animationDelay = Math.random() * 5 + 's';
        sparkle.style.animationDuration = (Math.random() * 3 + 2) + 's';

        const size = Math.random() * 4 + 2;
        sparkle.style.width = size + 'px';
        sparkle.style.height = size + 'px';

        container.appendChild(sparkle);
    }
}

window.addEventListener('DOMContentLoaded', createSparkles);
