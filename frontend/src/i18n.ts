import i18n from "i18next";
import { initReactI18next } from "react-i18next";


const resources = {
  en: {
    translation: {
      auth_form: {
        "Login": "Login",
        "Registration": "Registration",
        "Username": "username",
        "Password": "password",
        "Enter": "Login",
        "Dont_have": "Don't have an account?",
        "Here": "Register here",
        "Already": "Already have an account?",
        "If_forget": "*Don't have an account or forget password? Please contact your system administrator.",
        "Change_password_link": "Change base password",
        "Change_password": "Change password",
        "Old_password": "Old password",
        "New_password": "New password",
        "Confirm_password": "Confirm password",
        "Change": "Change",
        "Back_to_login": "Back to login",

        //информация об ошибках и прочие информационные сообщения
        "Username_is_req": "Username is required",
        "Password_is_req": "Password is required",
        "Old_password_is_req": "Enter old password",
        "New_password_is_req": "Enter new password",
        "Confirm_password_is_req": "Enter confirm password",
        "Password_min_length": "Min length is 8 symbols",
        "Passwords_must_match": "Passwords must match",
      },
      novnc: {
        "Title": "Connection managment",
        "Connect": "Connect to noVNC console",
        "DetachISO": "Detach ISO",
        "StopVM": "Shutdown VM",
        "StartVM": "Start VM"
      },
      admin: {
        "Admin_panel": "Administration panel",
        "Create_new_user": "Create new user",
        "Users_list": "Users list",
        "ID": "ID",
        "Role_ID": "Role ID",
        "VM_name": "VM name",
        "NoVNC_port": "NoVNC port",
        "VNC_port": "VNC port",
        "Actions": "Actions",
        "Delete": "Delete",
        "Create": "Create",
        "About_program": "About program",
      },
      "about_program": {
        "title": "About the program",
        "description": "This application is designed for managing users and virtual machines and the organization of secure remote access to them. It provides administrators with a convenient interface for creating, deleting, and monitoring users.",
        "creators": "Creators",
        "developers": {
          "do_povyshev": "Povyshyov Denis Olegovich - System and Backend Developer",
          "na_lapin": "Lapin Nikolay Alexandrovich - Web Interface Developer, Tester"
        },
        "version": "Version",
        "close_button": "Close"
      }

    }
  },
  ru: {
    translation: {
      auth_form: {
        "Login": "Вход",
        "Registration": "Регистрация",
        "Username": "имя пользователя",
        "Password": "пароль",
        "Enter": "Войти",
        "Dont_have": "Еще нет аккаунта?",
        "Here": "Зарегестрироваться",
        "Already": "Уже есть аккаунт?",
        "If_forget": "*Еще нет аккаунта или забыли пароль? Пожалуйста, обратитесь к вашему системному администратору",
        "Change_password_link": "Сменить стандартный пароль",
        "Change_password": "Сменить пароль",
        "Old_password": "Старый пароль",
        "New_password": "Новый пароль",
        "Confirm_password": "Подтверждение пароля",
        "Change": "Сменить",
        "Back_to_login": "Вернуться к форме входа",

        //информация об ошибках и прочие информационные сообщения
        "Username_is_req": "Имя обязательно",
        "Password_is_req": "Пароль обязателен",
        "Old_password_is_req": "Введите старый пароль",
        "New_password_is_req": "Введите новый пароль",
        "Confirm_password_is_req": "Введите подтверждение пароля",
        "Password_min_length": "Минимальная длина 8 символов",
        "Passwords_must_match": "Пароли должны совпадать",
      },
      novnc: {
        "Title": "Управление соединением",
        "Connect": "Подключиться к консоли noVNC",
        "DetachISO": "Извечь ISO",
        "StopVM": "Выключить ВМ",
        "StartVM": "Запустить ВМ"
      },
      admin: {
        "Admin_panel": "Панель администратора",
        "Create_new_user": "Создать нового пользователя",
        "Users_list": "Список пользователей",
        "ID": "ID",
        "Role_ID": "ID Роли",
        "VM_name": "Имя ВМ",
        "NoVNC_port": "Порт NoVNC",
        "VNC_port": "Порт VNC",
        "Actions": "Действия",
        "Delete": "Удалить",
        "Create": "Создать",
        "About_program": "О программе",

      },
      "about_program": {
        "title": "О программе",
        "description": "Данное приложение предназначено для управления пользователями и виртуальными машинами и организации безопасного удаленного подключения к ним. Оно предоставляет администраторам удобный интерфейс для создания, удаления и мониторинга пользователей.",
        "creators": "Создатели",
        "developers": {
          "do_povyshev": "Повышев Денис Олегович  - Системный, бекенд разработчик",
          "na_lapin": "Лапин Николай Александрович - Разработчик веб-интерфейса, тестировщик"
        },
        "version": "Версия",
        "close_button": "Закрыть"
      }
    }
  }
};

i18n
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    resources,
    lng: "ru", // language to use, more information here: https://www.i18next.com/overview/configuration-options#languages-namespaces-resources
    // you can use the i18n.changeLanguage function to change the language manually: https://www.i18next.com/overview/api#changelanguage
    // if you're using a language detector, do not define the lng option

    interpolation: {
      escapeValue: false // react already safes from xss
    }
  });

  export default i18n;