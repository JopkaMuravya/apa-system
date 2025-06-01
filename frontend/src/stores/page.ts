import { defineStore } from 'pinia';

interface Subject {
  id: number;
  name: string;
}

interface Group {
  id: number;
  name: string;
}

interface Teacher {
  id: number;
  full_name: string;
}

type ListType = 'groups' | 'teachers' | null;

export const usePageStore = defineStore('page', {
  state: () => ({
    title: 'Главная' as string,
    currentSubject: null as Subject | null,
    currentList: [] as Array<Group | Teacher>,
    listType: null as ListType,
  }),
  actions: {
    setSubjectWithGroups(subject: Subject, groups: Group[]) {
      this.title = subject.name;
      this.currentSubject = subject;
      this.currentList = groups;
      this.listType = 'groups';
    },
    setSubjectWithTeachers(subject: Subject, teachers: Teacher[]) {
      this.title = subject.name;
      this.currentSubject = subject;
      this.currentList = teachers;
      this.listType = 'teachers';
    },
    resetToHome() {
      this.title = 'Главная';
      this.currentSubject = null;
      this.currentList = [];
      this.listType = null;
    }
  }
});
