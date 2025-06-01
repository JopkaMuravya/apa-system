<template>
  <aside class="Teacher-main">
    <div v-if="!pageStore.currentSubject" class="subjects-container">
      <button v-for="subject in subjects" :key="subject.id" class="subjects-info" @click="showTeachers(subject)">
        <img class="subject-icon" :src="SubjectIcon" alt="Subject" />
        <p class="subject">{{ subject.name }}</p>
      </button>
    </div>
    <div v-else class="subjects-container">
      <div v-for="item in pageStore.currentList" :key="item.id" class="groups-info">
        <p class="subject">{{ item.name }}</p>
      </div>
    </div>
</aside>
</template>

  <script>
    import { usePageStore } from '../stores/page';
    import SubjectIcon from '../assets/icons/programs.png';
  
  export default {
    data() {
      return {
        SubjectIcon,
        subjects: [
          { id: 1, name: 'Статистика' },
          { id: 2, name: 'Консультация по дисциплине "Основы алгоритмизации и программирования' },
          { id: 3, name: 'Основы алгоритмизации и программирования' },
          { id: 4, name: 'Базы данных' },
        ],
        teachers: [
          { id: 1, name: 'Сущенко А. А.' },
          { id: 2, name: 'Деревягин' },
          { id: 3, name: 'Месенев' },
          { id: 4, name: 'Ганжа' },
        ],
      };
    },
    setup() {
      const pageStore = usePageStore();
      return { pageStore };
    },
    methods: {
      showTeachers(subject) {
        this.pageStore.setSubjectWithTeachers(subject, this.teachers);
      },
    },
  };
  </script>
  
  <style scoped>
    .Teacher-main {
      display: flex;
      flex-direction: column;
      height: 100vh;
      background: #ffffff;
      font-family: 'Arial', sans-serif;
      position: relative;
      padding: 20px;
      overflow-y: auto;
    }

    .subjects-container {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      align-items: flex-start;
    }

    .subjects-info {
      background: rgba(0, 103, 177, 0.05);
      border-radius: 10px;
      width: 300px;
      height: 220px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 8px;
      text-align: center;
      border: 2px solid #6995D0;
      transition: all 0.3s ease;
      box-shadow: 0 20px 20px rgba(0, 0, 0, 0.1);
      flex-shrink: 0;
      cursor: pointer;
      transform: scale(1);
    }

      .subjects-info:hover {
        transform: scale(1.03);
        box-shadow: 0 25px 25px rgba(0, 0, 0, 0.15);
      }

    .groups-info {
      background: rgba(0, 103, 177, 0.1);
      border-radius: 10px;
      width: 300px;
      height: 120px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 8px;
      text-align: center;
      border: 2px solid #6995D0;
      transition: all 0.3s ease;
      box-shadow: 0 20px 20px rgba(0, 0, 0, 0.1);
      flex-shrink: 0;
      transform: scale(1);
    }

    .groups-info:hover {
      transform: scale(1.03);
      box-shadow: 0 25px 25px rgba(0, 0, 0, 0.15); 
    }

    .subject {
      color: #6995D0;
      font-size: 18px;
      margin: 5px 20px;
      text-decoration: underline;
      word-break: break-word;
    }

    .subject-icon {
      width: 40px;
      height: 40px;
    
    }

    

  </style>  
