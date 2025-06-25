import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { LanguageSwitcher } from './LangSwitcher';
import { useTranslation } from 'react-i18next';
import * as Yup from 'yup';
import apiClient from '../common/apiClient'; 

const supportedLanguages = {
  en: { label: 'English', flag: './assets/flags/en.png' },
  ru: { label: 'Русский', flag: './assets/flags/ru.png' },
};

// Интерфейсы для типизации данных
interface AuthFormValues {
  username: string;
  password: string;
}

interface ChangePasswordFormValues {
  username: string; // Добавлено поле для имени пользователя
  oldPassword: string;
  newPassword: string;
  confirmPassword: string;
}

interface LoginResponse {
  access_token: string;
  username: string;
}

export const AuthPage: React.FC = () => {
  const { t } = useTranslation();
  const [isLoginForm, setIsLoginForm] = useState(true);

  // Переключение между формами
  const toggleForm = () => {
    setIsLoginForm((prev) => !prev);
  };

  return (
    <div className="auth-page">
      {isLoginForm ? (
        <AuthForm toggleForm={toggleForm} />
      ) : (
        <ChangePasswordForm toggleForm={toggleForm} />
      )}
    </div>
  );
};

const AuthForm: React.FC<{ toggleForm: () => void }> = ({ toggleForm }) => {
  const { t } = useTranslation();

  const validationSchema = Yup.object().shape({
    username: Yup.string().required(t('auth_form.Username_is_req')),
    password: Yup.string().required(t('auth_form.Password_is_req')),
  });

  const handleSubmit = async (values: AuthFormValues) => {
    try {
      const response = await apiClient.post<LoginResponse>('/login', values);
      const { access_token, username } = response;

      console.log(username);

      // Сохраняем токен в localStorage
      localStorage.setItem('jwtToken', access_token);
      localStorage.setItem('username', username);

      alert('Login successful');
      window.location.reload();
    } catch (error: any) {
      console.error('Error:', error.response?.data?.msg || 'Unknown error');
      alert('Invalid username or password');
    }
  };

  return (
    <div className="form-container">
      <h2>{t('auth_form.Login')}</h2>
      <Formik
        initialValues={{ username: '', password: '' }}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="input-group">
              <label>{t('auth_form.Username')}</label>
              <Field type="text" name="username" className="input" />
              <ErrorMessage name="username" component="div" className="error" />
            </div>
            <div className="input-group">
              <label>{t('auth_form.Password')}</label>
              <Field type="password" name="password" className="input" />
              <ErrorMessage name="password" component="div" className="error" />
            </div>
            <button type="submit" className="button-login" disabled={isSubmitting}>
              {t('auth_form.Enter')}
            </button>
            <LanguageSwitcher supportedLanguages={supportedLanguages} />
          </Form>
        )}
      </Formik>
      <p>
        {t('auth_form.If_forget')}{' '}
        <a href="#" onClick={(e) => {
          e.preventDefault();
          toggleForm();
        }} style={{ color: 'blue' }}>
          {t('auth_form.Change_password_link')}
        </a>
      </p>
    </div>
  );
};

export const ChangePasswordForm: React.FC<{ toggleForm: () => void }> = ({ toggleForm }) => {
  const { t } = useTranslation();

  const ChangePasswordSchema = Yup.object().shape({
    username: Yup.string().required(t('auth_form.Username_is_req')), // Валидация имени пользователя
    oldPassword: Yup.string().required(t('auth_form.Old_password_is_req')),
    newPassword: Yup.string()
      .min(6, t('auth_form.Password_min_length'))
      .required(t('auth_form.New_password_is_req')),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref('newPassword'), ''], t('auth_form.Passwords_must_match'))
      .required(t('auth_form.Confirm_password_is_req')),
  });

  const handleSubmit = async (values: ChangePasswordFormValues) => {
    try {
      await apiClient.post('/change-password', values);
      alert(t('auth_form.Password_changed_success'));
      window.location.reload();
    } catch (error: any) {
      console.error('Error:', error.response?.data?.msg || 'Unknown error');
      alert(error.response?.data?.msg || t('auth_form.Unknown_error'));
    }
  };

  return (
    <div className="form-container">
      <h2>{t('auth_form.Change_password')}</h2>
      <Formik
        initialValues={{
          username: '',
          oldPassword: '',
          newPassword: '',
          confirmPassword: '',
        }}
        validationSchema={ChangePasswordSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="input-group">
              <label>{t('auth_form.Username')}</label>
              <Field type="text" name="username" className="input" />
              <ErrorMessage name="username" component="div" className="error" />
            </div>
            <div className="input-group">
              <label>{t('auth_form.Old_password')}</label>
              <Field type="password" name="oldPassword" className="input" />
              <ErrorMessage name="oldPassword" component="div" className="error" />
            </div>
            <div className="input-group">
              <label>{t('auth_form.New_password')}</label>
              <Field type="password" name="newPassword" className="input" />
              <ErrorMessage name="newPassword" component="div" className="error" />
            </div>
            <div className="input-group">
              <label>{t('auth_form.Confirm_password')}</label>
              <Field type="password" name="confirmPassword" className="input" />
              <ErrorMessage name="confirmPassword" component="div" className="error" />
            </div>
            <button type="submit" className="button-login" disabled={isSubmitting}>
              {t('auth_form.Change')}
            </button>
          </Form>
        )}
      </Formik>
      <p>
        <a href="#" onClick={(e) => {
          e.preventDefault();
          toggleForm();
        }} style={{ color: 'blue' }}>
          {t('auth_form.Back_to_login')}
        </a>
      </p>
    </div>
  );
};