import { defineStore } from 'pinia';

export const usePageStore = defineStore('page', {
  state: () => ({
    currentSubject: null as Subject | null,
    currentGroups: [] as Group[],
    sidebarTitle: 'Главная',
    showBackButton: false,
    isTeacher: false, // Добавляем флаг для определения типа пользователя
  }),
  actions: {
    setSubject(subject: Subject, groups: Group[]) {
      this.currentSubject = subject;
      this.currentGroups = groups;
      this.sidebarTitle = subject.name;
      this.showBackButton = true;
      this.isTeacher = true; // Устанавливаем флаг при входе преподавателя
    },
    clearSubject() {
      this.currentSubject = null;
      this.currentGroups = [];
      this.sidebarTitle = 'Главная';
      this.showBackButton = false;
    },
    setTitle(title: string) {
      this.sidebarTitle = title;
    },
    setIsTeacher(value: boolean) {
      this.isTeacher = value;
    },
  },
});

interface Subject {
  id: number;
  name: string;
}

interface Group {
  id: number;
  name: string;
}
