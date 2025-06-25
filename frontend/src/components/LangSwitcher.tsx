// LanguageSwitcher.tsx
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

interface LanguageSwitcherProps {
  supportedLanguages: { [key: string]: { label: string; flag: string } };
}

export const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({ supportedLanguages }) => {
  const { i18n } = useTranslation();
  const languageKeys = Object.keys(supportedLanguages);
  const [currentLanguageIndex, setCurrentLanguageIndex] = useState(
    languageKeys.indexOf(i18n.language)
  );

  // Функция для переключения языка
  const handleLanguageChange = () => {
    const nextIndex = (currentLanguageIndex + 1) % languageKeys.length;
    const nextLanguage = languageKeys[nextIndex];
    i18n.changeLanguage(nextLanguage);
    setCurrentLanguageIndex(nextIndex);
  };

  const currentLanguageKey = languageKeys[currentLanguageIndex];

  return (
    <div className="language-switcher">
      {/* Кнопка с текущим языком */}
      <button className="active" onClick={handleLanguageChange}>
        <img
          src={supportedLanguages[currentLanguageKey].flag}
          alt={supportedLanguages[currentLanguageKey].label}
        />
      </button>
    </div>
  );
};