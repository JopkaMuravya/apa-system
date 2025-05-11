<template>
  <aside class="Teacher-main">
    <div v-if="!pageStore.currentSubject" class="subjects-container">
      <button v-for="subject in subjects" :key="subject.id" class="subjects-info" @click="showGroups(subject)">
        <img class="subject-icon" :src="SubjectIcon" alt="Subject" />
        <p class="subject">{{ subject.name }}</p>
      </button>
      <button class="new-subject-button" @click="subject" @mouseover="hoverAdd" @mouseleave="unhoverAdd">
        <img :src="currentAddIcon" alt="Новый предмет" />
      </button>
    </div>
    <div v-else class="subjects-container">
      <!--<h2>Группы для {{ currentSubject.name }}</h2>-->
      <div v-for="group in pageStore.currentGroups" :key="group.id" class="groups-info">
        <p class="subject">{{ group.name }}</p>
      </div>
      <button class="new-group-button" @click="subject" @mouseover="hoverAdd" @mouseleave="unhoverAdd">
        <img :src="currentAddIcon" alt="Новая группа" />
      </button>
    </div>
</aside>
</template>

  <script>
    import { usePageStore } from '../stores/page';
    import SubjectIcon from '../assets/icons/programs.png';
    import AddIcon from '../assets/icons/add_blue.png';
    import AddIcon2 from '../assets/icons/add_red.png';
  
  export default {
    data() {
      return {
        SubjectIcon,
        AddIcon,
        AddIcon2,
        currentAddIcon: AddIcon,
        subjects: [
          { id: 1, name: 'Консультация по дисциплине "Основы алгоритмизации и программирования"' },
          { id: 2, name: 'Основы алгоритмизации и программирования' },
        ],
        groups: [
          { id: 1, name: 'Б9123-01.03.02сп' },
          { id: 2, name: 'Б9123-01.03.02ии' },
          { id: 3, name: 'Б9123-02.03.01сцт' },
          { id: 4, name: 'Б9123-09.03.03пикд' },
        ],
      };
    },
    setup() {
      const pageStore = usePageStore();
      return { pageStore };
    },
    methods: {
      showGroups(subject) {
        this.pageStore.setSubject(subject, this.groups);
      },
      addSubject() {
        // Логика для добавления нового предмета
      },
      hoverAdd() {
        this.currentAddIcon = this.AddIcon2;
      },
      unhoverAdd() {
        this.currentAddIcon = this.AddIcon;
      }
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

    .new-subject-button {
      height: 40px;
      background: #ffffff;
      border-radius: 5px;
      padding: 5px;
      cursor: pointer;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      justify-content: center;
      text-align: center;
      margin: 100px 5px;
      border: 2px solid #6995D0;
      transform: scale(1);
      transition: all 0.3s ease;
    }
    .new-group-button {
      height: 40px;
      background: #ffffff;
      border-radius: 5px;
      padding: 5px;
      cursor: pointer;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      justify-content: center;
      text-align: center;
      margin: 40px 5px;
      border: 2px solid #6995D0;
      transform: scale(1);
      transition: all 0.3s ease;
    }

    .new-subject-button:hover, .new-group-button:hover {
      transform: scale(1.03);
      box-shadow: 0 25px 25px rgba(0, 0, 0, 0.15);
    }

    .new-subject-button img, .new-group-button img {
      width: 26px;
      height: 26px;
    }

  </style>  
