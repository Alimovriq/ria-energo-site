// ==================== ГЛОБАЛЬНЫЕ ФУНКЦИИ ====================

/**
 * Переключение видимости пароля
 */
function togglePasswordVisibility(inputElement, iconElement) {
    if (inputElement.type === 'password') {
        inputElement.type = 'text';
        iconElement.classList.replace('bi-eye-slash', 'bi-eye');
    } else {
        inputElement.type = 'password';
        iconElement.classList.replace('bi-eye', 'bi-eye-slash');
    }
}

/**
 * Валидация формы регистрации
 */
function validateRegistrationForm(event, form) {
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }

    const password = document.getElementById('password')?.value;
    const confirmPassword = document.getElementById('confirmPassword')?.value;

    if (password && confirmPassword && password !== confirmPassword) {
        document.getElementById('confirmPassword').setCustomValidity('Пароли не совпадают');
    } else {
        document.getElementById('confirmPassword')?.setCustomValidity('');
    }

    form.classList.add('was-validated');
}

/**
 * Валидация формы входа
 */
function validateLoginForm(event, form) {
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }

    form.classList.add('was-validated');
}

// ==================== ИНИЦИАЛИЗАЦИЯ ПО СТРАНИЦАМ ====================

/**
 * Инициализация для страницы регистрации
 */
function initRegistrationPage() {
    // Проверяем, что мы на нужной странице
    if (!document.getElementById('registrationForm')) return;

    document.getElementById('togglePassword')?.addEventListener('click', function() {
        const passwordInput = document.getElementById('password');
        const icon = this;
        togglePasswordVisibility(passwordInput, icon);
    });

    document.getElementById('toggleConfirmPassword')?.addEventListener('click', function() {
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const icon = this;
        togglePasswordVisibility(confirmPasswordInput, icon);
    });

    const form = document.getElementById('registrationForm');
    form?.addEventListener('submit', function(event) {
        validateRegistrationForm(event, form);
    });
}

/**
 * Инициализация для страницы входа
 */
function initLoginPage() {
    if (!document.getElementById('loginForm')) return;

    // Обработчик видимости пароля (без изменений)
    document.getElementById('toggleLoginPassword')?.addEventListener('click', function() {
        const passwordInput = document.getElementById('loginPassword');
        const icon = this;
        togglePasswordVisibility(passwordInput, icon);
    });

    const form = document.getElementById('loginForm');

    // Валидация формы (без изменений)
    form?.addEventListener('submit', function(event) {
        validateLoginForm(event, form);
    });

    // Добавляем обработчик AJAX (исправленный)
    form?.addEventListener('submit', async function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add('was-validated');
            return;
        }

        event.preventDefault();

        try {
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;

            const formData = new FormData(form);
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            // Получаем текст ответа для дебага
            const responseText = await response.text();
            console.log('Raw response:', responseText);

            // Пробуем распарсить JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (e) {
                throw new Error('Invalid server response');
            }

            // Проверяем статус ответа
            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            // Редирект при успехе
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                window.location.href = '/';
            }

        } catch (error) {
            console.error('Login error:', error);
            alert(error.message || 'Login error');
        } finally {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
            }
        }
    });
}

/**
 * Инициализация для других страниц
 */
function initOtherPage() {
    // Код для других страниц...
}

// ==================== ЗАПУСК ПРИ ЗАГРУЗКЕ ====================
document.addEventListener('DOMContentLoaded', function() {
    // Определяем текущую страницу и запускаем нужный инициализатор
    if (document.body.classList.contains('registration-page')) {
        initRegistrationPage();
    }
    else if (document.body.classList.contains('login-page')) {
        initLoginPage();
    }
    else if (document.body.classList.contains('product-page')) {
        initProductPage();
    }
    // Добавь другие страницы по аналогии
});