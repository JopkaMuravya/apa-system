import { defineStore } from 'pinia';
import { api } from '../boot/axios';

interface User {
  id: number;
  fullName: string;
  email: string;
  role: string; // 'teacher', 'student', 'admin' и т. д.
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null, // Текущий пользователь (изначально null)
    isAuthenticated: false,    // Флаг авторизации
  }),

  getters: {
    // Геттер для имени пользователя
    userName: (state) => state.user?.fullName || 'Гость',
    
    // Геттер для проверки роли (например, является ли преподавателем)
    isTeacher: (state) => state.user?.role === 'teacher',
  },

  actions: {
    // 🔹 Загрузка данных пользователя (например, после входа в систему)
    async fetchUser() {
      try {
        const response = await api.get('/api/auth/user/');
        this.user = response.data;
        this.isAuthenticated = true;
      } catch (error) {
        console.error('Ошибка загрузки пользователя:', error);
        this.logout();
      }
    },

    // 🔹 Выход из системы (очистка данных)
    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token'); // Если используется JWT
    },

    // 🔹 Обновление профиля (если нужно)
    async updateProfile(updatedData: Partial<User>) {
      try {
        const response = await api.patch('/api/auth/user/', updatedData);
        this.user = { ...this.user, ...response.data };
      } catch (error) {
        console.error('Ошибка обновления профиля:', error);
      }
    },
  },
});