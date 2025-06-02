<template>
  <div class="group-detail">
    <div v-if="loading">Загрузка данных...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="students-table">
        <thead>
          <tr>
            <th>№</th>
            <th>Название</th>
            <th>Преподаватель</th>
            <th class="action-header">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, index) in subjects" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ entry.subject_name }}</td>
            <td>{{ entry.teacher_name }}</td>
            <td class="action-buttons">
              <button class="edit-button">
                <img src="../assets/icons/edit.png" alt="Редактировать" />
              </button>
              <button class="delete-button">
                <img src="../assets/icons/delete.png" alt="Удалить" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <button class="add-student-button">
        Добавить предмет
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'

export default defineComponent({
  name: 'GroupSubjects',
  setup() {
    const route = useRoute()
    const groupId = route.params.id
    const subjects = ref<{ subject_name: string; teacher_name: string }[]>([])
    const loading = ref(true)
    const error = ref('')

    const fetchSubjects = async () => {
      try {
        const { data } = await api.get(`/api/groups/${groupId}/subject_teachers/`)
        subjects.value = data
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        error.value = e.response?.data?.detail || 'Ошибка при загрузке предметов'
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchSubjects)

    return {
      subjects,
      loading,
      error
    }
  }
})
</script>

<style scoped>
.group-detail h3 {
  margin-bottom: 15px;
}

.error {
  color: red;
  margin-top: 10px;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.students-table th {
  background: #6995D0;
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: bold;
  position: relative;
  border: none;
}

.students-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.students-table tr:hover {
  background-color: rgba(105, 149, 208, 0.1);
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

.delete-button,
.edit-button,
.save-button,
.cancel-button {
  border: none;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  padding: 4px;
  cursor: pointer;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-button,
.save-button {
  background-color: #5cb85c;
}
.edit-button:hover,
.save-button:hover {
  background-color: #4cae4c;
}
.cancel-button,
.delete-button {
  background-color: #d9534f;
}
.cancel-button:hover,
.delete-button:hover {
  background-color: #c9302c;
}

img {
  width: 16px;
  height: 16px;
}

input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-modal {
  background: white;
  padding: 25px 30px;
  border-radius: 10px;
  text-align: center;
  min-width: 280px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.error-modal h2 {
  margin: 0 0 10px;
  font-size: 24px;
}

.error-modal p {
  margin: 0 0 15px;
  font-size: 14px;
  color: #333;
}

.error-modal button {
  background-color: #6995d0;
  color: white;
  padding: 6px 14px;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.error-modal button:hover {
  background-color: #527cbf;
}

.add-student-button {
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

.add-student-button:hover {
  background-color: #527cbf;
}

</style>
