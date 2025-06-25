import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import apiClient from '../common/apiClient'; // Импортируем ApiClient
import { LanguageSwitcher } from './LangSwitcher';
import { UserComponent } from './UserComponent';
import { AboutProgram } from './AboutProgram'; // Импортируем компонент "О программе"

// Определяем интерфейс для ответа сервера
interface ApiResponse {
  message: string;
}

export const NoVncLink: React.FC = () => {
  const { t } = useTranslation();
  const [username, setUsername] = useState<string | null>(null);
  const [isAboutOpen, setIsAboutOpen] = useState(false); // Состояние для модального окна

  // Получаем имя пользователя из localStorage при монтировании компонента
  React.useEffect(() => {
    const user = localStorage.getItem('username');
    if (user) {
      setUsername(user);
    }
  }, []);

  const supportedLanguages = {
    en: { label: 'English', flag: './assets/flags/en.png' },
    ru: { label: 'Русский', flag: './assets/flags/ru.png' },
    /* add more languages as needed */
  };

  // Формируем ссылку на основе имени пользователя
  const getNoVncUrl = (username: string): string => {
    return `https://192.168.0.124/${username}/index.html?resize=remote&path=/${username}/websockify`;
  };

  // Функция для выполнения POST-запроса с использованием ApiClient
  const postRequest = async (endpoint: string, vmName: string) => {
    try {
      const response = await apiClient.post<ApiResponse>(`/api/vm/${endpoint}/${vmName}`);
      alert(response.message); // Показываем сообщение об успехе
    } catch (error) {
      if (error instanceof Error) {
        alert(`Error: ${error.message}`); // Обрабатываем ошибку как Error
      } else {
        alert(`Error: ${String(error)}`); // Преобразуем ошибку в строку
      }
    }
  };

  // Функция для извлечения ISO
  const detachIso = async () => {
    if (username) {
      await postRequest('detach-iso', `vm_${username}`);
    }
  };

  // Функция для выключения ВМ
  const stopVm = async () => {
    if (username) {
      await postRequest('stop', `vm_${username}`);
    }
  };

  // Функция для включения ВМ
  const startVm = async () => {
    if (username) {
      await postRequest('start', `vm_${username}`);
    }
  };

  // Если пользователь не найден, отображаем сообщение об ошибке
  if (!username) {
    return <p className="error">{t('novnc.NoUser')}</p>;
  }

  return (
    <div className="novnc-link-container">
      <h3>{t('novnc.Title')}</h3>
      <LanguageSwitcher supportedLanguages={supportedLanguages} />
      <UserComponent userName={localStorage.getItem('username') || ''} />

      {/* Кнопка "О программе" */}
      <button
        className="admin-about-button"
        onClick={() => setIsAboutOpen(true)}
      >
        {t('admin.About_program')}
      </button>

      <a
        href={getNoVncUrl(username)}
        target="_blank"
        rel="noopener noreferrer"
        className="novnc-button"
      >
        {t('novnc.Connect')}
      </a>

      {/* Кнопки управления ВМ */}
      <div className="vm-controls">
        <button onClick={detachIso} className="vm-control-button">
          {t('novnc.DetachISO')}
        </button>
        <button onClick={stopVm} className="vm-control-button">
          {t('novnc.StopVM')}
        </button>
        <button onClick={startVm} className="vm-control-button">
          {t('novnc.StartVM')}
        </button>
      </div>

      {/* Модальное окно "О программе" */}
      {isAboutOpen && (
        <AboutProgram onClose={() => setIsAboutOpen(false)} />
      )}
    </div>
  );
};