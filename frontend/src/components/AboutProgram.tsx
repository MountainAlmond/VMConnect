// AboutProgram.tsx
import React from 'react';
import { useTranslation } from 'react-i18next';

export const AboutProgram: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const { t } = useTranslation(); // Используем хук для перевода

  return (
    <div className="about-program-modal">
      <div className="about-program-content">
        {/* Заголовок */}
        <h2>{t('about_program.title')}</h2>

        {/* Описание программы */}
        <p>{t('about_program.description')}</p>

        {/* Создатели */}
        <p>
          <strong>{t('about_program.creators')}:</strong>
          <strong>{t('about_program.developers.kaf')}:</strong>
          <ul>
            <li>{t('about_program.developers.na_zaelskaya')}</li>
            <li>{t('about_program.developers.do_povyshev')}</li>
            <li>{t('about_program.developers.na_lapin')}</li>
          </ul>
        </p>

        {/* Версия программы */}
        <p>
          <strong>{t('about_program.version')}:</strong> 1.0.0
        </p>

        {/* Кнопка закрытия */}
        <button className="about-program-close-button" onClick={onClose}>
          {t('about_program.close_button')}
        </button>
      </div>
    </div>
  );
};