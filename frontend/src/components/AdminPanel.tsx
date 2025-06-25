import React, { useState, useEffect } from 'react';
import apiClient from '../common/apiClient';
import { LanguageSwitcher } from './LangSwitcher';
import { UserComponent } from './UserComponent';
import { useTranslation } from 'react-i18next';
import { AboutProgram } from './AboutProgram'; // Импортируем новый компонент

interface User {
  id: number;
  username: string;
  role_id: number;
  vm_name: string | null;
  novnc_port: number | null;
  vnc_port: number | null;
}

export const AdminPanel: React.FC = () => {
  const { t } = useTranslation();
  const [users, setUsers] = useState<User[]>([]);
  const [newUser, setNewUser] = useState({ username: '', password: '' });
  const [isAboutOpen, setIsAboutOpen] = useState(false); // Состояние для модального окна

  const supportedLanguages = {
    en: { label: 'English', flag: './assets/flags/en.png' },
    ru: { label: 'Русский', flag: './assets/flags/ru.png' },
  };

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const fetchedUsers: User[] = await apiClient.get('/admin/users');
        setUsers(fetchedUsers);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
    fetchUsers();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/admin/create_user', newUser);
      alert(t('admin.User_created_successfully'));
      setNewUser({ username: '', password: '' });

      const updatedUsers: User[] = await apiClient.get('/admin/users');
      setUsers(updatedUsers);
    } catch (error) {
      console.error('Error creating user:', error);
      alert(t('admin.Error_creating_user'));
    }
  };

  const handleDeleteUser = async (username: string) => {
    try {
      await apiClient.delete(`/admin/delete_user/${username}`);
      alert(t('admin.User_deleted_successfully'));

      const updatedUsers: User[] = await apiClient.get('/admin/users');
      setUsers(updatedUsers);
    } catch (error) {
      console.error('Error deleting user:', error);
      alert(t('admin.Error_deleting_user'));
    }
  };

  return (
    <div className="admin-panel">
      <h2 className="admin-title">{t('admin.Admin_panel')}</h2>
      <LanguageSwitcher supportedLanguages={supportedLanguages} />
      <UserComponent userName={localStorage.getItem('username')} />

      {/* Кнопка "О программе" */}
      <button
        className="admin-about-button"
        onClick={() => setIsAboutOpen(true)}
      >
        {t('admin.About_program')}
      </button>

      {/* Форма создания нового пользователя */}
      <form onSubmit={handleCreateUser} className="admin-create-user-form">
        <h3>{t('admin.Create_new_user')}</h3>
        <div className="input-group">
          <label>{t('auth_form.Username')}</label>
          <input
            type="text"
            value={newUser.username}
            onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
            required
          />
        </div>
        <div className="input-group">
          <label>{t('auth_form.Password')}</label>
          <input
            type="password"
            value={newUser.password}
            onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
            required
          />
        </div>
        <button type="submit" className="admin-button-create">
          {t('admin.Create')}
        </button>
      </form>

      {/* Таблица пользователей */}
      <h3>{t('admin.Users_list')}</h3>
      <table className="admin-users-table">
        <thead>
          <tr>
            <th>{t('admin.ID')}</th>
            <th>{t('auth_form.Username')}</th>
            <th>{t('admin.Role_ID')}</th>
            <th>{t('admin.VM_name')}</th>
            <th>{t('admin.NoVNC_port')}</th>
            <th>{t('admin.VNC_port')}</th>
            <th>{t('admin.Actions')}</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.role_id}</td>
              <td>{user.vm_name || '-'}</td>
              <td>{user.novnc_port || '-'}</td>
              <td>{user.vnc_port || '-'}</td>
              <td>
                {user.username !== 'admin' && (
                  <button
                    onClick={() => handleDeleteUser(user.username)}
                    className="admin-button-delete"
                  >
                    {t('admin.Delete')}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Модальное окно "О программе" */}
      {isAboutOpen && (
        <AboutProgram onClose={() => setIsAboutOpen(false)} />
      )}
    </div>
  );
};