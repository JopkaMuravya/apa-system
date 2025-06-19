<template>
  <aside class="Teacher-main">
    <div v-if="!pageStore.currentSubject" class="subjects-container">
      <button v-for="subject in filteredSubjects" :key="subject.id" class="subjects-info" @click="showGroups(subject)">
        <img class="subject-icon" :src="SubjectIcon" alt="Subject" />
        <p class="subject">{{ subject.name }}</p>
      </button>
    </div>
    <div v-else class="subjects-container">
      <button v-for="group in pageStore.currentGroups" :key="group.id" class="groups-info" @click="goToTeacherGrades(group)">
        <p class="subject">{{ group.name }}</p>
      </button>
    </div>
  </aside>
</template>

<script>
import { onMounted } from 'vue';
import { usePageStore } from '../stores/page';
import SubjectIcon from '../assets/icons/programs.png';
import AddIcon from '../assets/icons/add_blue.png';
import AddIcon2 from '../assets/icons/add_red.png';
import { api } from '../boot/axios';
import { useRouter } from 'vue-router';

export default {
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      SubjectIcon,
      AddIcon,
      AddIcon2,
      currentAddIcon: AddIcon,
      subjects: [],
      loading: false,
      error: null
    };
  },
  setup() {
    const pageStore = usePageStore();
    const router = useRouter();

    onMounted(() => {
      pageStore.setIsTeacher(true);
    });

    return { pageStore, router };
  },
  created() {
    this.fetchTeacherSubjects();
  },
  methods: {
    async fetchTeacherSubjects() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('/api/teacher/subjects/');
        this.subjects = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке предметов:', error);
        this.error = 'Не удалось загрузить список предметов';
      } finally {
        this.loading = false;
      }
    },
    async showGroups(subject) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`/api/teacher/subjects/${subject.id}/groups/`);
        this.pageStore.setSubject(subject, response.data);
      } catch (error) {
        console.error('Ошибка при загрузке групп:', error);
        this.error = 'Не удалось загрузить список групп';
      } finally {
        this.loading = false;
      }
    },
    hoverAdd() {
      this.currentAddIcon = this.AddIcon2;
    },
    unhoverAdd() {
      this.currentAddIcon = this.AddIcon;
    },
    goToTeacherGrades(group) {
      this.router.push({
        name: 'teacher-grades',
        query: {
          groupId: group.id,
          groupName: group.name,
          subjectId: this.pageStore.currentSubject.id,
          subjectName: this.pageStore.currentSubject.name
        }
      });
    },
  },
  computed: {
    filteredSubjects() {
      let filtered = this.subjects

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()

        filtered = filtered.filter(subject => subject.name.toLowerCase().includes(query))
      }

      return filtered
    }
  },
};
</script>

<style scoped>
.Teacher-main {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: #ffffff;
  font-family: 'Arial', sans-serif;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}

.subjects-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-start;
  align-content: flex-start;
  
  margin-left: 80px;
  width: calc(100% - 80px);
  height: 100%;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;

  
  scrollbar-width: auto;
  scrollbar-color: rgba(0, 0, 0, 0.4) transparent;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.3);
  }
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
  cursor: pointer;
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

@media (max-width: 480px) {
  .subjects-container {
    margin-left: 0px;
    justify-content: center;
    width: 100%;
  }

  .subjects-info, .groups-info {
    width: 90%;
    max-width: none;
    height: 140px;
    margin: 0 auto 15px;
  }

  .subject {
    font-size: 20px;
  }
}
</style>