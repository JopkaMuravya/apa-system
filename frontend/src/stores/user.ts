import { defineStore } from 'pinia';
import { api } from '../boot/axios';

interface User {
  id: number;
  fullName: string;
  email: string;
  role: string;
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),

  getters: {
    userName: (state) => state.user?.fullName || 'Гость',
    
    isTeacher: (state) => state.user?.role === 'teacher',
  },

  actions: {
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

    logout() {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    },

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