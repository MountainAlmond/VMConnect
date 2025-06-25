//подключение библиотек

import * as React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

//подключение модулей
import { I18nextProvider } from 'react-i18next';
import i18next from 'i18next';
import { AuthPage} from './components/AuthForm';
import { NoVncLink } from './components/NoVncLink';
import { AdminPanel } from './components/AdminPanel';

// import { EntityList } from './components/EntityList';


//подключение стилей компонентов


import './components/styles/Wallpaper.css';
import './components/styles/UserComponent.css';
import './components/styles/LangSwitcher.css';
import './components/styles/AuthForm.css';
import './components/styles/NoVncLink.css';
import './components/styles/AdminPanel.css';
import './components/styles/AboutProgram.css'

import './common/commonStyles/CommonBackground.css';

class App extends React.Component<{}, {}> {
  render() {
    // Проверяем наличие JWT-токена
    const token = localStorage.getItem('jwtToken');
    const username = localStorage.getItem('username');

    if (!token) {
      // Если токена нет, отображаем форму авторизации
      return (
        <I18nextProvider i18n={i18next}>
          <div className="wallpaper">
            <AuthPage />
          </div>
        </I18nextProvider>
      );
    }

    // Проверяем, является ли пользователь администратором
    const isAdmin = username === 'admin'; // Предполагаем, что имя администратора "admin"

    return (
      <I18nextProvider i18n={i18next}>
        <BrowserRouter basename="/">
          {isAdmin ? (
            // Если пользователь администратор, отображаем AdminPanel
            <AdminPanel />
          ) : (
            // Если обычный пользователь, отображаем основное приложение
            <NoVncLink />
          )}
        </BrowserRouter>
      </I18nextProvider>
    );
  }
}

export default App;
