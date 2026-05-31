function createStars() {
    const container = document.getElementById('starField');
    if (!container) return;

    for (let i = 0; i < 250; i++) {
        const star = document.createElement('div');
        star.classList.add('star-small');
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.width = Math.random() * 2.5 + 0.5 + 'px';
        star.style.height = star.style.width;
        star.style.animationDelay = Math.random() * 5 + 's';
        star.style.animationDuration = Math.random() * 3 + 2 + 's';
        container.appendChild(star);
    }

    for (let i = 0; i < 40; i++) {
        const star = document.createElement('div');
        star.classList.add('star-big');
        star.innerHTML = '✦';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.fontSize = (Math.random() * 10 + 8) + 'px';
        star.style.animationDelay = Math.random() * 6 + 's';
        star.style.animationDuration = Math.random() * 4 + 3 + 's';
        container.appendChild(star);
    }
}

function validateEmail(email) {
    if (!email) return true;
    if (/[а-яА-ЯёЁ]/.test(email)) return false;
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(ru|com|net|org|ua|by|kz|uz|info|biz|me|site)$/i;
    return regex.test(email);
}

document.addEventListener('DOMContentLoaded', function () {
    createStars();

    const emailInput = document.getElementById('author_email');
    if (emailInput) {
        emailInput.addEventListener('input', function () {
            const email = this.value;
            const errorDiv = document.getElementById('emailError');
            if (!email) {
                errorDiv.textContent = '';
                return;
            }
            if (/[а-яА-ЯёЁ]/.test(email)) {
                errorDiv.textContent = '❌ Email не должен содержать русские буквы!';
            } else if (!validateEmail(email)) {
                errorDiv.textContent = '❌ Неверный формат email!';
            } else {
                errorDiv.textContent = '✅ Email корректен';
            }
        });
    }

    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function (e) {
            const email = document.getElementById('author_email').value;
            if (email && !validateEmail(email)) {
                e.preventDefault();
                alert('❌ Введите корректный email!');
            }
        });
    }

    const materialSelect = document.getElementById('material');
    if (materialSelect) {
        materialSelect.addEventListener('change', function () {
            const colors = {
                'gold': 'gold', 'silver': 'silver', 'rose': 'pink',
                'platinum': '#e5e5e5', 'black': 'black', 'meteorite': '#2d1b4e'
            };
            const names = {
                'gold': '🟡 Золото', 'silver': '⚪ Серебро', 'rose': '🌸 Розовое золото',
                'platinum': '🤍 Платина', 'black': '⚫ Чёрное золото', 'meteorite': '☄️ Метеорит'
            };
            const preview = document.getElementById('materialPreview');
            if (preview) {
                preview.innerHTML = '<div style="display: flex; align-items: center; gap: 10px;">' +
                    '<div style="width: 30px; height: 30px; border-radius: 50%; background: ' + colors[this.value] + '; border: 1px solid white; box-shadow: 0 0 8px ' + colors[this.value] + ';"></div>' +
                    '<span style="color: white;">' + names[this.value] + '</span>' +
                    '</div>';
            }
        });
        materialSelect.dispatchEvent(new Event('change'));
    }

    const stars = document.querySelectorAll('#ratingPreview .rating-star');
    const ratingInput = document.getElementById('ratingValue');

    stars.forEach(function (star) {
        star.addEventListener('click', function () {
            const val = parseInt(this.dataset.value);
            ratingInput.value = val;
            stars.forEach(function (s, i) { s.textContent = i < val ? '⭐' : '☆'; });
        });
        star.addEventListener('mouseenter', function () {
            const val = parseInt(this.dataset.value);
            stars.forEach(function (s, i) { s.textContent = i < val ? '⭐' : '☆'; });
        });
    });

    const ratingPreview = document.getElementById('ratingPreview');
    if (ratingPreview) {
        ratingPreview.addEventListener('mouseleave', function () {
            const val = parseInt(ratingInput.value);
            stars.forEach(function (s, i) { s.textContent = i < val ? '⭐' : '☆'; });
        });
    }

    window.openModal = function () {
        document.getElementById('reviewModal').style.display = 'flex';
    };

    window.closeModal = function () {
        document.getElementById('reviewModal').style.display = 'none';
        const form = document.getElementById('reviewForm');
        if (form) form.reset();
        document.getElementById('ratingValue').value = 5;
        stars.forEach(function (s, i) { s.textContent = i < 5 ? '⭐' : '☆'; });
    };

    window.onclick = function (e) {
        const modal = document.getElementById('reviewModal');
        if (e.target === modal) closeModal();
    };
});
