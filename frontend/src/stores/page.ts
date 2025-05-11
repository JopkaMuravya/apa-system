import { defineStore } from 'pinia';

export const usePageStore = defineStore('page', {
  state: () => ({
    title: 'Главная',
    currentSubject: null as null | { id: number; name: string },
    currentGroups: [] as Array<{ id: number; name: string }>
  }),
  actions: {
    setSubject(subject: { id: number; name: string }, groups: Array<{ id: number; name: string }>) {
      this.title = subject.name;
      this.currentSubject = subject;
      this.currentGroups = groups;
    },
    resetToHome() {
      this.title = 'Главная';
      this.currentSubject = null;
      this.currentGroups = [];
    }
  }
});
