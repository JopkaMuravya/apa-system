<template>
  <div class="group-detail">
    <div v-if="loading">Загрузка данных...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="students-table">
        <thead>
          <tr>
            <th>№</th>
            <th>ФИО</th>
            <th>Корпоративная почта</th>
            <th class="action-header">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(student, index) in sortedStudents" :key="student.id">
            <template v-if="editingStudentId === student.id">
              <td>{{ index + 1 }}</td>
              <td><input v-model="editForm.full_name" /></td>
              <td><input v-model="editForm.email" /></td>
              <td class="action-buttons">
                <button class="save-button" @click="saveStudent">
                  <img :src="AcceptIcon" alt="Сохранить" />
                </button>
                <button class="cancel-button" @click="cancelEdit">
                  <img :src="CancelIcon" alt="Отменить" />
                </button>
              </td>
            </template>
            <template v-else>
              <td>{{ index + 1 }}</td>
              <td>{{ student.full_name }}</td>
              <td>{{ student.email }}</td>
              <td class="action-buttons">
                <button class="edit-button" @click="startEdit(student)">
                  <img :src="EditIcon" alt="Редактировать" />
                </button>
                <button class="delete-button" @click="openDeleteModal(student)">
                  <img :src="DeleteIcon" alt="Удалить" />
                </button>
              </td>
            </template>
          </tr>
        </tbody>
      </table>

      <button class="add-student-button" @click="showAddModal = true">
        Добавить студента
      </button>

      <AddStudentModal
        v-if="showAddModal"
        :group-id="String(groupId)"
        @close="showAddModal = false"
        @student-added="fetchGroupData"
      />

      <div v-if="showErrorModal" class="modal-backdrop">
        <div class="error-modal">
          <div class="error-modal-blue">
            <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
            <h2>Ошибка</h2>
            <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
          </div>
          <div class="error-modal-text">
            <p>{{ modalErrorMessage }}</p>
            <button @click="showErrorModal = false">Закрыть</button>
          </div>
        </div>
      </div>

      <div v-if="showDeleteModal" class="modal-backdrop">
        <div class="error-modal">
          <div class="error-modal-blue">
            <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
            <h2>Подтверждение</h2>
            <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
          </div>
          <div class="error-modal-text">
            <p>Удалить {{ studentToDelete?.full_name }} из группы?</p>
            <div style="display: flex; justify-content: center; gap: 10px;">
              <button @click="confirmDeleteStudent">Да</button>
              <button @click="cancelDeleteStudent">Нет</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'

import AddStudentModal from './AddStudentModal.vue'
const DeleteIcon = new URL('../assets/icons/delete.png', import.meta.url).href
const EditIcon = new URL('../assets/icons/edit.png', import.meta.url).href
const AcceptIcon = new URL('../assets/icons/accept.png', import.meta.url).href
const CancelIcon = new URL('../assets/icons/cancel.png', import.meta.url).href

interface Student {
  id: number
  full_name: string
  email: string
}

export default defineComponent({
  name: 'GroupStudents',
  components: { AddStudentModal },
  setup() {
    const showAddModal = ref(false)
    const route = useRoute()
    const groupId = route.params.id
    const students = ref<Student[]>([])
    const loading = ref(true)
    const error = ref('')
    const editingStudentId = ref<number | null>(null)
    const editForm = ref({ id: 0, full_name: '', email: '' })
    const showErrorModal = ref(false)
    const modalErrorMessage = ref('')
    const showDeleteModal = ref(false)
    const studentToDelete = ref<Student | null>(null)

    const fetchGroupData = async () => {
      try {
        const { data } = await api.get(`/api/groups/${groupId}/`)
        students.value = data.students
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        error.value = e.response?.data?.detail || 'Ошибка при загрузке данных группы'
      } finally {
        loading.value = false
      }
    }

    const removeStudentFromGroup = async (studentId: number) => {
      try {
        await api.delete(`/api/groups/${groupId}/`, {
          params: { student_id: studentId }
        })
        students.value = students.value.filter((s) => s.id !== studentId)
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        error.value = e.response?.data?.detail || 'Ошибка при удалении студента из группы'
      }
    }

    const sortedStudents = computed(() =>
      [...students.value].sort((a, b) => a.full_name.localeCompare(b.full_name))
    )

    const startEdit = (student: Student) => {
      editingStudentId.value = student.id
      editForm.value = {
        id: student.id,
        full_name: student.full_name,
        email: student.email
      }
    }

    const cancelEdit = () => {
      editingStudentId.value = null
    }

    const saveStudent = async () => {
      const parts = editForm.value.full_name.trim().split(/\s+/)
      const last_name = parts[0] || ''
      const first_name = parts[1] || ''
      const middle_name = parts.slice(2).join(' ') || ''

      try {
        await api.put('/api/users/', {
          id: editForm.value.id,
          email: editForm.value.email,
          first_name,
          last_name,
          middle_name
        })

        editingStudentId.value = null
        fetchGroupData()
      } catch (err: unknown) {
        const e = err as AxiosError<Record<string, unknown>>
        const data = e.response?.data

        if (typeof data?.detail === 'string') {
          modalErrorMessage.value = data.detail
        } else if (data && typeof data === 'object') {
          const messages: string[] = []
          Object.values(data).forEach((fieldErrors) => {
            if (Array.isArray(fieldErrors)) {
              fieldErrors.forEach((msg) => {
                if (typeof msg === 'string') messages.push(msg)
              })
            } else if (typeof fieldErrors === 'string') {
              messages.push(fieldErrors)
            }
          })
          modalErrorMessage.value = messages.join(' ')
        } else {
          modalErrorMessage.value = 'Ошибка при сохранении'
        }

        showErrorModal.value = true
      }
    }

    const openDeleteModal = (student: Student) => {
      studentToDelete.value = student
      showDeleteModal.value = true
    }

    const cancelDeleteStudent = () => {
      studentToDelete.value = null
      showDeleteModal.value = false
    }

    const confirmDeleteStudent = async () => {
      if (!studentToDelete.value) return

      try {
        await removeStudentFromGroup(studentToDelete.value.id)
      } catch {
        modalErrorMessage.value = 'Не удалось удалить студента из группы'
        showErrorModal.value = true
      } finally {
        studentToDelete.value = null
        showDeleteModal.value = false
      }
    }

    onMounted(fetchGroupData)

    return {
      groupId,
      students,
      sortedStudents,
      loading,
      error,
      editingStudentId,
      editForm,
      startEdit,
      cancelEdit,
      saveStudent,
      openDeleteModal,
      cancelDeleteStudent,
      confirmDeleteStudent,
      studentToDelete,
      showDeleteModal,
      showErrorModal,
      modalErrorMessage,
      DeleteIcon,
      FEFUIcon,
      EditIcon,
      AcceptIcon,
      CancelIcon,
      showAddModal,
      fetchGroupData
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
    padding: 0;
    border-radius: 10px;
    text-align: center;
    min-width: 280px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }

  .error-modal-blue {
    background: #6995D0;
    border-radius: 10px 10px 0 0;
    min-width: 100px;
    min-height: 0;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 20px;
  }

  .error-modal-text {
    padding: 25px 30px;
    border-radius: 10px 10px 0 0;
    text-align: center;
    min-height: 80px;
  }

  .error-modal-blue img {
    width: auto;
    height: 35px;
    margin-bottom: 5px;
  }

  .error-modal h2 {
    margin: 0;
    font-size: 22px;
    color: white;
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
