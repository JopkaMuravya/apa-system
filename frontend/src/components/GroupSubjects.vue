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
          <tr v-for="(entry, index) in subjects" :key="entry.id">
            <td>{{ index + 1 }}</td>
            <td>{{ entry.subject_name }}</td>
            <td>
              <template v-if="editingId === entry.id">
                <select v-model="editTeacherId">
                  <option
                    v-for="teacher in availableTeachers"
                    :key="teacher.id"
                    :value="teacher.id"
                  >
                    {{ teacher.full_name }}
                  </option>
                </select>
              </template>
              <template v-else>
                {{ entry.teacher_name }}
              </template>
            </td>
            <td class="action-buttons">
              <template v-if="editingId === entry.id">
                <button class="save-button" @click="saveEdit(entry)">
                  <img :src="AcceptIcon" alt="Сохранить" />
                </button>
                <button class="cancel-button" @click="cancelEdit">
                  <img :src="CancelIcon" alt="Отменить" />
                </button>
              </template>
              <template v-else>
                <button class="edit-button" @click="startEdit(entry)">
                  <img :src="EditIcon" alt="Редактировать" />
                </button>
                <button class="delete-button" @click="openDeleteModal(entry)">
                  <img :src="DeleteIcon" alt="Удалить" />
                </button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>

      <button class="add-student-button" @click="showAddModal = true">
        Добавить предмет
      </button>

      <AddGroupSubjectModal
        v-if="showAddModal"
        :group-id="groupId"
        @close="showAddModal = false"
        @subject-added="handleSubjectAdded"
      />

      <div v-if="showDeleteModal" class="modal-backdrop">
        <div class="error-modal">
          <h2>Подтверждение</h2>
          <p>Удалить {{ subjectToDelete?.subject_name }} из группы?</p>
          <div style="display: flex; justify-content: center; gap: 10px;">
            <button @click="confirmDeleteSubject">Да</button>
            <button @click="cancelDeleteSubject">Нет</button>
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
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'
import AddGroupSubjectModal from 'components/AddGroupSubjectModal.vue'

const DeleteIcon = new URL('../assets/icons/delete.png', import.meta.url).href
const EditIcon = new URL('../assets/icons/edit.png', import.meta.url).href
const AcceptIcon = new URL('../assets/icons/accept.png', import.meta.url).href
const CancelIcon = new URL('../assets/icons/cancel.png', import.meta.url).href

interface Entry {
  id: number
  subject_name: string
  teacher_name: string
  subject: number
  teacher: number
}

interface Teacher {
  id: number
  full_name: string
}

interface SubjectWithTeachers {
  id: number
  teachers: Teacher[]
}

export default defineComponent({
  name: 'GroupSubjects',
  components: {
    AddGroupSubjectModal
  },
  setup() {
    const route = useRoute()
    const groupId = ref(Number(route.params.id))

    const subjects = ref<Entry[]>([])
    const loading = ref(true)
    const error = ref('')
    const editingId = ref<number | null>(null)
    const editTeacherId = ref<number | null>(null)
    const availableTeachers = ref<Teacher[]>([])

    const showDeleteModal = ref(false)
    const showErrorModal = ref(false)
    const modalErrorMessage = ref('')
    const subjectToDelete = ref<Entry | null>(null)
    const showAddModal = ref(false)

    const fetchSubjects = async () => {
      try {
        const { data } = await api.get(`/api/groups/${groupId.value}/subject_teachers/`)
        subjects.value = data
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        error.value = e.response?.data?.detail || 'Ошибка при загрузке предметов'
      } finally {
        loading.value = false
      }
    }

    const fetchAvailableTeachers = async (subjectId: number) => {
      try {
        const res = await api.get<SubjectWithTeachers[]>('/api/subjects/')
        const subject = res.data.find((s) => s.id === subjectId)
        availableTeachers.value = subject?.teachers || []
      } catch {
        availableTeachers.value = []
      }
    }

    const startEdit = async (entry: Entry) => {
      editingId.value = entry.id
      editTeacherId.value = entry.teacher
      await fetchAvailableTeachers(entry.subject)
    }

    const cancelEdit = () => {
      editingId.value = null
      editTeacherId.value = null
      availableTeachers.value = []
    }

    const saveEdit = async (entry: Entry) => {
      try {
        await api.put(`/api/groups/${groupId.value}/subject_teachers/`, {
          subject_id: entry.subject,
          teacher_id: editTeacherId.value
        })
        await fetchSubjects()
        cancelEdit()
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        modalErrorMessage.value = e.response?.data?.detail || 'Ошибка при сохранении'
        showErrorModal.value = true
      }
    }

    const openDeleteModal = (entry: Entry) => {
      subjectToDelete.value = entry
      showDeleteModal.value = true
    }

    const cancelDeleteSubject = () => {
      subjectToDelete.value = null
      showDeleteModal.value = false
    }

    const confirmDeleteSubject = async () => {
      if (!subjectToDelete.value) return
      try {
        await api.delete(`/api/groups/${groupId.value}/subject_teachers/`, {
          params: { subject_id: subjectToDelete.value.subject }
        })
        await fetchSubjects()
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        modalErrorMessage.value = e.response?.data?.detail || 'Не удалось удалить предмет из группы'
        showErrorModal.value = true
      } finally {
        subjectToDelete.value = null
        showDeleteModal.value = false
      }
    }

    const handleSubjectAdded = () => {
      showAddModal.value = false
      fetchSubjects()
    }

    onMounted(fetchSubjects)

    return {
      groupId,
      subjects,
      loading,
      error,
      editingId,
      editTeacherId,
      availableTeachers,
      startEdit,
      cancelEdit,
      saveEdit,
      showDeleteModal,
      subjectToDelete,
      openDeleteModal,
      cancelDeleteSubject,
      confirmDeleteSubject,
      showErrorModal,
      modalErrorMessage,
      showAddModal,
      handleSubjectAdded,
      DeleteIcon,
      EditIcon,
      AcceptIcon,
      CancelIcon
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
