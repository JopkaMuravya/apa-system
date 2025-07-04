<template>
  <aside class="Student-main">
    <div class="subjects-container">
      <button v-for="subject in filteredSubjects" :key="subject.id" class="subjects-info" @click="goToSubjectDetail(subject.id)">
        <img class="subject-icon" :src="subjectIcon" alt="Subject" />
        <p class="subject">{{ subject.name }}</p>
      </button>
    </div>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </aside>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
const subjectIcon = new URL('../assets/icons/programs.png', import.meta.url).href;
import { api } from '../boot/axios';

export default {
  name: 'StudentSubjectsList',
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const subjects = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const router = useRouter();
    const groupId = ref(null);

    const fetchSubjects = async () => {
      loading.value = true;
      error.value = null;
      try {
        const response = await api.get('/api/student/subjects/');
        subjects.value = response.data;
      } catch (err) {
        error.value = 'Ошибка при загрузке предметов';
      } finally {
        loading.value = false;
      }
    };

    const fetchCurrentUserGroup = async () => {
      try {
        const response = await api.get('/api/current-user/');
        if (response.data.group && response.data.group.id) {
          groupId.value = response.data.group.id;
        }
      } catch (err) {
        console.error('Ошибка при загрузке данных пользователя:', err);
      }
    };

    const goToSubjectDetail = (id) => {
      const subject = subjects.value.find(s => s.id === id);
      if (groupId.value) {
        router.push({
          name: 'student-grades',
          query: {
            subjectId: id,
            subjectName: subject ? subject.name : '',
            groupId: groupId.value
          }
        });
      } else {
        router.push({
          name: 'student-grades',
          query: {
            subjectId: id,
            subjectName: subject ? subject.name : ''
          }
        });
      }
    };

    const filteredSubjects = computed(() => {
      let filtered = subjects.value

      if (props.searchQuery) {
        const query = props.searchQuery.toLowerCase()
        filtered = filtered.filter(subject => subject.name.toLowerCase().includes(query))
      }

      return filtered
    })

    onMounted(() => {
      fetchSubjects();
      fetchCurrentUserGroup();
    });

    return {
      subjects,
      loading,
      error,
      subjectIcon,
      goToSubjectDetail,
      filteredSubjects,
    };
  },
};
</script>

<style scoped>
.Student-main {
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
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;

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

.loading {
  margin-top: 10px;
  font-weight: bold;
}

.error {
  color: red;
  margin-top: 10px;
}

@media (max-width: 480px) {
  .subjects-container {
    margin-left: 0px;
    justify-content: center;
    width: 100%;
  }

  .subjects-info {
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