<template>
  <div class="tab-content">
    <div class="subjects-teachers">
      <div v-if="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else>
        <table class="subject-table">
          <thead>
            <tr>
              <th>Предмет</th>
              <th>Преподаватели</th>
              <th class="action-header">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subject in sortedSubjects" :key="subject.id">
              <td>{{ subject.name }}</td>
              <td>
                <ul class="teacher-list">
                  <li v-for="(teacher, index) in subject.teachers" :key="index">
                    {{ teacher }}
                  </li>
                </ul>
              </td>
              <td class="action-buttons">
                <button class="edit-button">
                  <img :src="EditIcon" alt="Редактировать" />
                </button>
                <button class="delete-button">
                  <img :src="DeleteIcon" alt="Удалить" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <button class="add-subject-button" @click="showAddModal = true">
          Добавить предмет
        </button>
        <AddSubjectModal v-if="showAddModal" @close="showAddModal = false" @subject-added="fetchSubjects" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from 'vue'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'
import EditIcon from '../assets/icons/edit.png'
import DeleteIcon from '../assets/icons/delete.png'
import AddSubjectModal from './AddSubjectModal.vue'

interface Subject {
  id: number
  name: string
  teachers: string[]
}

export default defineComponent({
  name: 'SubjectsTeachers',
  components: { AddSubjectModal },
  setup() {
    const subjects = ref<Subject[]>([])
    const loading = ref(true)
    const error = ref('')
    const showAddModal = ref(false)

    const fetchSubjects = async () => {
      try {
        const response = await api.get('/api/subjects/')
        subjects.value = response.data
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        error.value = e.response?.data?.detail || 'Ошибка при загрузке предметов'
      } finally {
        loading.value = false
      }
    }

    const sortedSubjects = computed(() =>
      [...subjects.value].sort((a, b) => a.name.localeCompare(b.name))
    )

    onMounted(fetchSubjects)

    return {
      subjects,
      sortedSubjects,
      loading,
      error,
      showAddModal,
      EditIcon,
      DeleteIcon,
      fetchSubjects
    }
  }
})
</script>

<style scoped>
.subjects-teachers {
  font-family: 'Arial', sans-serif;
}

.subject-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.subject-table th,
.subject-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
  vertical-align: top;
}

th.action-header,
td.action-buttons {
  width: 90px;
  text-align: center;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.edit-button,
.delete-button {
  border: none;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  padding: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-button {
  background-color: #5cb85c;
}
.edit-button:hover {
  background-color: #4cae4c;
}
.delete-button {
  background-color: #d9534f;
}
.delete-button:hover {
  background-color: #c9302c;
}

img {
  width: 16px;
  height: 16px;
}

.teacher-list {
  margin: 0;
  padding-left: 16px;
}

.add-subject-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #6995d0;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  float: right;
}

.add-subject-button:hover {
  background-color: #527cbf;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
