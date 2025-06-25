import React, { useState } from 'react';

interface UserComponentProps {
  userName: string | null;
  // onLogout: () => void; // Функция для обработки выхода
}

export const UserComponent: React.FC<UserComponentProps> = ({ userName}) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = () => {
    // Удаляем JWT-токен и username из localStorage
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username');
    // Закрываем выпадающее меню
    setIsOpen(false);

    // Перенаправляем на страницу входа/регистрации
    window.location.reload();
  };

  return (
    <div className="user-menu">
      {/* Добавляем атрибут title для всплывающей подсказки */}
      <button
        className="user-icon"
        onClick={toggleMenu}
        title={userName || 'Гость'} // Полное имя или "Гость", если имени нет
      >
        {/* Иконка пользователя и первая буква имени */}
        <i className="fas fa-user"></i>
        {userName ? userName.charAt(0).toUpperCase() : '?'}
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          <button className="logout-button" onClick={handleLogout}>
            Выйти
          </button>
        </div>
      )}
    </div>
  );
};