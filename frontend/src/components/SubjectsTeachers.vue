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
            <tr v-for="subject in filteredSubjects" :key="subject.id">
              <td>{{ subject.name }}</td>
              <td>
                <ul class="teacher-list">
                  <li v-for="(teacher, index) in subject.teachers" :key="index">
                    {{ teacher.full_name }}
                  </li>
                </ul>
              </td>
              <td class="action-buttons">
                <button class="edit-button" @click="openEditModal(subject)">
                  <img :src="EditIcon" alt="Редактировать" />
                </button>
                <button class="delete-button" @click="openDeleteModal(subject)">
                  <img :src="DeleteIcon" alt="Удалить" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <button class="add-subject-button" @click="showAddModal = true">
          Добавить предмет
        </button>

        <AddSubjectModal
          v-if="showAddModal"
          @close="showAddModal = false"
          @subject-added="fetchSubjects"
        />

        <EditSubjectModal
          v-if="showEditModal && subjectToEdit"
          :subject-id="subjectToEdit.id"
          :initial-name="subjectToEdit.name"
          :initial-teachers="subjectToEdit.teachers.map(t => t.id)"
          @close="closeEditModal"
          @subject-updated="fetchSubjects"
        />

        <div v-if="showDeleteModal" class="modal-backdrop">
          <div class="error-modal">
            <h2>Подтверждение</h2>
            <p>Удалить предмет "{{ subjectToDelete?.name }}"?</p>
            <div class="modal-actions">
              <button @click="confirmDelete">Да</button>
              <button @click="cancelDelete">Нет</button>
            </div>
          </div>
        </div>

        <div v-if="showErrorModal" class="modal-backdrop">
          <div class="error-modal">
            <h2>Ошибка</h2>
            <p>{{ modalErrorMessage }}</p>
            <button @click="showErrorModal = false">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'
import AddSubjectModal from './AddSubjectModal.vue'
import EditSubjectModal from './EditSubjectModal.vue'
import EditIcon from '../assets/icons/edit.png'
import DeleteIcon from '../assets/icons/delete.png'

interface Subject {
  id: number
  name: string
  teachers: { id: number; full_name: string }[]
}

export default defineComponent({
  name: 'SubjectsTeachers',
  components: { AddSubjectModal, EditSubjectModal },
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const subjects = ref<Subject[]>([])
    const loading = ref(true)
    const error = ref('')
    const showAddModal = ref(false)

    const showEditModal = ref(false)
    const subjectToEdit = ref<Subject | null>(null)

    const showDeleteModal = ref(false)
    const subjectToDelete = ref<Subject | null>(null)

    const showErrorModal = ref(false)
    const modalErrorMessage = ref('')

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

    const filteredSubjects = computed(() => {
      let filtered = subjects.value

      if (props.searchQuery) {
        const query = props.searchQuery.toLowerCase()

        filtered = filtered.filter(subject =>
          subject.name.toLowerCase().includes(query) ||
          subject.teachers.some(teacher =>
            teacher.full_name.toLowerCase().includes(query)))
      }

      return [...filtered].sort((a, b) => a.name.localeCompare(b.name))
    })

    const openDeleteModal = (subject: Subject) => {
      subjectToDelete.value = subject
      showDeleteModal.value = true
    }

    const cancelDelete = () => {
      showDeleteModal.value = false
      subjectToDelete.value = null
    }

    const confirmDelete = async () => {
      if (!subjectToDelete.value) return
      try {
        await api.delete(`/api/subjects/${subjectToDelete.value.id}/`)
        fetchSubjects()
      } catch (err) {
        showErrorModal.value = true
        modalErrorMessage.value = 'Не удалось удалить предмет'
      } finally {
        showDeleteModal.value = false
        subjectToDelete.value = null
      }
    }

    const openEditModal = (subject: Subject) => {
      subjectToEdit.value = subject
      showEditModal.value = true
    }

    const closeEditModal = () => {
      subjectToEdit.value = null
      showEditModal.value = false
    }

    const getTeacherIds = (subject: Subject): number[] => {
      const teacherMap = new Map(subjects.value.flatMap(s =>
        s.teachers.map((t, i) => [t, i + 1])
      ))
      return subject.teachers.map(name => teacherMap.get(name)).filter(Boolean) as number[]
    }

    onMounted(fetchSubjects)

    return {
      subjects,
      filteredSubjects,
      loading,
      error,
      showAddModal,
      showEditModal,
      subjectToEdit,
      EditIcon,
      DeleteIcon,
      fetchSubjects,
      showDeleteModal,
      subjectToDelete,
      openDeleteModal,
      cancelDelete,
      confirmDelete,
      openEditModal,
      closeEditModal,
      showErrorModal,
      modalErrorMessage,
      getTeacherIds
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

th {
  background: #6995D0;
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: bold;
  position: relative;
}

td {
  padding: 12px 15px;
  text-align: left;
  vertical-align: top;
  border: 1px solid #e0e0e0;
}

tr {
  border: 1px solid #e0e0e0;
}

tr:hover {
  background-color: rgba(105, 149, 208, 0.1);
}

th.action-header,
td.action-buttons {
  width: 90px;
  text-align: center;
  white-space: nowrap;
  border: none;
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
  padding-left: 0;
  list-style-type: none;
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
  z-index: 1000;
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
  font-size: 22px;
}

.error-modal p {
  margin: 0 0 15px;
  font-size: 15px;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.modal-actions button,
.error-modal button {
  background-color: #6995d0;
  color: white;
  padding: 6px 14px;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.modal-actions button:hover,
.error-modal button:hover {
  background-color: #527cbf;
}
</style>
