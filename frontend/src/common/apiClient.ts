import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';

// Определяем типы для конфигурации клиента
interface ApiClientOptions {
  baseURL: string;
}

// Создаем класс для API-клиента
class ApiClient {
  private client: AxiosInstance;

  constructor(options: ApiClientOptions) {
    this.client = axios.create({
      baseURL: options.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Добавляем перехватчик для добавления токена в заголовки
    this.client.interceptors.request.use((config: InternalAxiosRequestConfig) => {
      const token = localStorage.getItem('jwtToken');
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Метод для выполнения GET-запросов
  public get<T>(url: string, config?: InternalAxiosRequestConfig): Promise<T> {
    return this.client.get<T>(url, config).then((response) => response.data);
  }

  // Метод для выполнения POST-запросов
  public post<T>(url: string, data?: any, config?: InternalAxiosRequestConfig): Promise<T> {
    return this.client.post<T>(url, data, config).then((response) => response.data);
  }

  // Метод для выполнения PUT-запросов
  public put<T>(url: string, data?: any, config?: InternalAxiosRequestConfig): Promise<T> {
    return this.client.put<T>(url, data, config).then((response) => response.data);
  }

  // Метод для выполнения DELETE-запросов
  public delete<T>(url: string, config?: InternalAxiosRequestConfig): Promise<T> {
    return this.client.delete<T>(url, config).then((response) => response.data);
  }
}

// Экспортируем экземпляр клиента
//АДРЕС СЕРВЕРА МОЖЕТ ИЗМЕНИТЬСЯ, ИЗМЕНИТЬ ПРИ НЕОБХОДИМОСТИ
const apiClient = new ApiClient({ baseURL: 'http://192.168.0.124:5000' }); // Замените на URL вашего бэкенда

export default apiClient;