<template>
  <aside class="Student-main">
    <div class="subjects-container">
      <button v-for="subject in subjects" :key="subject.id" class="subjects-info" @click="goToSubjectDetail(subject.id)">
        <img class="subject-icon" :src="subjectIcon" alt="Subject" />
        <p class="subject">{{ subject.name }}</p>
      </button>
    </div>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </aside>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import subjectIcon from '../assets/icons/programs.png';
import { api } from '../boot/axios';

export default {
  name: 'StudentSubjectsList',
  setup() {
    const subjects = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const router = useRouter();

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

    const goToSubjectDetail = (id) => {
      const subject = subjects.value.find(s => s.id === id);
      router.push({ name: 'student-subject-detail', params: { id }, query: { name: subject ? subject.name : '' } });
    };

    onMounted(() => {
      fetchSubjects();
    });

    return {
      subjects,
      loading,
      error,
      subjectIcon,
      goToSubjectDetail,
    };
  },
};
</script>

<style scoped>
.Student-main {
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
</style>
