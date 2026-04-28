const ThemeManager = (() => {
    const validModes = ['system', 'light', 'dark'];
    const validAccents = ['emerald', 'indigo', 'rose', 'amber'];

    function getDefaults() {
        const root = document.documentElement;
        return {
            mode: root.dataset.defaultThemeMode || 'system',
            accent: root.dataset.defaultThemeAccent || 'emerald'
        };
    }

    function getStoredPreferences() {
        try {
            const raw = localStorage.getItem('uiThemePreferences');
            if (!raw) {
                return null;
            }
            const parsed = JSON.parse(raw);
            return {
                mode: validModes.includes(parsed.mode) ? parsed.mode : null,
                accent: validAccents.includes(parsed.accent) ? parsed.accent : null
            };
        } catch (error) {
            return null;
        }
    }

    function getPreferences() {
        const defaults = getDefaults();
        const stored = getStoredPreferences() || {};
        return {
            mode: stored.mode || defaults.mode,
            accent: stored.accent || defaults.accent
        };
    }

    function getEffectiveMode(mode) {
        if (mode === 'system') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        return validModes.includes(mode) ? mode : 'light';
    }

    function savePreferences(preferences) {
        localStorage.setItem('uiThemePreferences', JSON.stringify(preferences));
    }

    function syncPreferences(preferences) {
        if (!window.fetch) {
            return;
        }
        fetch('/settings/theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preferences)
        }).catch(() => {});
    }

    function refreshControls(preferences) {
        document.querySelectorAll('[data-theme-mode-choice]').forEach((element) => {
            const selected = element.dataset.themeModeChoice === preferences.mode;
            element.classList.toggle('ring-2', selected);
            element.classList.toggle('ring-offset-2', selected);
            element.classList.toggle('ring-slate-900', selected);
            element.classList.toggle('scale-[1.02]', selected);
            element.setAttribute('aria-pressed', selected ? 'true' : 'false');
        });

        document.querySelectorAll('[data-theme-accent-choice]').forEach((element) => {
            const selected = element.dataset.themeAccentChoice === preferences.accent;
            element.classList.toggle('ring-2', selected);
            element.classList.toggle('ring-offset-2', selected);
            element.classList.toggle('ring-slate-900', selected);
            element.classList.toggle('scale-[1.02]', selected);
            element.setAttribute('aria-pressed', selected ? 'true' : 'false');
        });

        const modeInput = document.getElementById('selectedThemeMode');
        const accentInput = document.getElementById('selectedThemeAccent');
        if (modeInput) {
            modeInput.value = preferences.mode;
        }
        if (accentInput) {
            accentInput.value = preferences.accent;
        }
    }

    function applyTheme(preferences) {
        const root = document.documentElement;
        root.dataset.themeMode = getEffectiveMode(preferences.mode);
        root.dataset.userThemeMode = preferences.mode;
        root.dataset.themeAccent = preferences.accent;
        refreshControls(preferences);
    }

    function setTheme(nextPreferences) {
        const current = getPreferences();
        const preferences = {
            mode: validModes.includes(nextPreferences.mode) ? nextPreferences.mode : current.mode,
            accent: validAccents.includes(nextPreferences.accent) ? nextPreferences.accent : current.accent
        };
        savePreferences(preferences);
        applyTheme(preferences);
        syncPreferences(preferences);
        return preferences;
    }

    function initializeControls() {
        document.querySelectorAll('[data-theme-mode-choice]').forEach((element) => {
            element.addEventListener('click', () => {
                setTheme({
                    mode: element.dataset.themeModeChoice,
                    accent: getPreferences().accent
                });
            });
        });

        document.querySelectorAll('[data-theme-accent-choice]').forEach((element) => {
            element.addEventListener('click', () => {
                setTheme({
                    mode: getPreferences().mode,
                    accent: element.dataset.themeAccentChoice
                });
            });
        });
    }

    function initialize() {
        applyTheme(getPreferences());
        initializeControls();
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', () => {
                const preferences = getPreferences();
                if (preferences.mode === 'system') {
                    applyTheme(preferences);
                }
            });
        }
    }

    return {
        initialize,
        setTheme,
        getPreferences
    };
})();

document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.initialize();
});
