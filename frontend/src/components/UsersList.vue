<template>
  <div class="users-list">
    <table>
      <thead>
        <tr>
          <th>ФИО</th>
          <th>Корпоративная почта</th>
          <th>
            <div class="role-header">
              <span>Роль</span>
              <select v-model="selectedRole" class="role-filter">
                <option value="">Все</option>
                <option value="waiting">Без роли</option>
                <option value="student">Студент</option>
                <option value="teacher">Преподаватель</option>
                <option value="moderator">Модератор</option>
              </select>
            </div>
          </th>
          <th class="action-header">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filteredUsers" :key="user.id">
          <template v-if="editingUserId === user.id">
            <td><input v-model="editForm.full_name" /></td>
            <td><input v-model="editForm.email" /></td>
            <td>
              <select v-model="editForm.role">
                <option value="waiting">Без роли</option>
                <option value="student">Студент</option>
                <option value="teacher">Преподаватель</option>
                <option value="moderator">Модератор</option>
              </select>
            </td>
            <td class="action-buttons">
              <button class="save-button" @click="saveUser">
                <img :src="AcceptIcon" alt="Сохранить" />
              </button>
              <button class="cancel-button" @click="cancelEdit">
                <img :src="CancelIcon" alt="Отменить" />
              </button>
            </td>
          </template>
          <template v-else>
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ getRoleLabel(user.role) }}</td>
            <td class="action-buttons">
              <button class="edit-button" @click="startEdit(user)">
                <img :src="EditIcon" alt="Редактировать" />
              </button>
              <button class="delete-button" @click="openDeleteModal(user)">
                <img :src="DeleteIcon" alt="Удалить" />
              </button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>

    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="showErrorModal" class="modal-backdrop">
      <div class="error-modal">
        <h2>Ошибка</h2>
        <p>{{ modalErrorMessage }}</p>
        <button @click="showErrorModal = false">Закрыть</button>
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-backdrop">
      <div class="error-modal">
        <h2>Подтверждение</h2>
        <p>Удалить пользователя {{ userToDelete?.full_name }}?</p>
        <div style="display: flex; justify-content: center; gap: 10px;">
          <button @click="confirmDeleteUser">Да</button>
          <button @click="cancelDeleteUser">Нет</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import DeleteIcon from '../assets/icons/delete.png'
import EditIcon from '../assets/icons/edit.png'
import AcceptIcon from '../assets/icons/accept.png'
import CancelIcon from '../assets/icons/cancel.png'
import type { AxiosError } from 'axios'

interface User {
  id: number
  full_name: string
  email: string
  role: string | null
}

export default defineComponent({
  name: 'UsersList',
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const users = ref<User[]>([])
    const selectedRole = ref('')
    const loading = ref(false)
    const error = ref('')
    const editingUserId = ref<number | null>(null)
    const editForm = ref({
      id: 0,
      full_name: '',
      email: '',
      role: ''
    })

    const showErrorModal = ref(false)
    const modalErrorMessage = ref('')
    const showDeleteModal = ref(false)
    const userToDelete = ref<User | null>(null)

    const fetchUsers = async () => {
      loading.value = true
      error.value = ''
      try {
        const response = await api.get('/api/users/')
        users.value = response.data.map((user: User) => ({
          ...user,
          role: user.role || '',
        }))
      } catch (err: unknown) {
        error.value = err instanceof Error ? err.message : 'Не удалось загрузить пользователей'
      } finally {
        loading.value = false
      }
    }

    const filteredUsers = computed(() => {
      let filtered = users.value

      if (selectedRole.value) {
        filtered = filtered.filter(user => user.role === selectedRole.value)
      }

      if (props.searchQuery) {
        const query = props.searchQuery.toLowerCase()
        filtered = filtered.filter(user =>
          user.full_name.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        )
      }

      return filtered
    })

    const getRoleLabel = (role: string | null) => {
      switch (role) {
        case 'student': return 'Студент'
        case 'teacher': return 'Преподаватель'
        case 'moderator': return 'Модератор'
        default: return 'Без роли'
      }
    }

    const startEdit = (user: User) => {
      editingUserId.value = user.id
      editForm.value = {
        id: user.id,
        full_name: user.full_name,
        email: user.email,
        role: user.role ?? ''
      }
    }

    const cancelEdit = () => {
      editingUserId.value = null
    }

    const saveUser = async () => {
      try {
        const parts = editForm.value.full_name.trim().split(/\s+/)
        const last_name = parts[0] || ''
        const first_name = parts[1] || ''
        const middle_name = parts.slice(2).join(' ') || ''

        await api.put('/api/users/', {
          id: editForm.value.id,
          email: editForm.value.email,
          role: editForm.value.role,
          first_name,
          last_name,
          middle_name
        })

        editingUserId.value = null
        fetchUsers()
      } catch (err: unknown) {
        const e = err as AxiosError<Record<string, unknown>>
        const data = e.response?.data

        if (typeof data?.detail === 'string') {
          modalErrorMessage.value = data.detail
        } else if (data && typeof data === 'object') {
          const messages: string[] = []
          Object.values(data).forEach(fieldErrors => {
            if (Array.isArray(fieldErrors)) {
              fieldErrors.forEach(error => {
                if (typeof error === 'string') messages.push(error)
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

    const openDeleteModal = (user: User) => {
      userToDelete.value = user
      showDeleteModal.value = true
    }

    const cancelDeleteUser = () => {
      userToDelete.value = null
      showDeleteModal.value = false
    }

    const confirmDeleteUser = async () => {
      if (!userToDelete.value) return

      try {
        await api.delete(`/api/users/${userToDelete.value.id}/`)
        fetchUsers()
      } catch (err) {
        showErrorModal.value = true
        modalErrorMessage.value = 'Не удалось удалить пользователя'
      } finally {
        userToDelete.value = null
        showDeleteModal.value = false
      }
    }

    onMounted(fetchUsers)

    return {
      users,
      selectedRole,
      filteredUsers,
      loading,
      error,
      DeleteIcon,
      EditIcon,
      AcceptIcon,
      CancelIcon,
      editingUserId,
      editForm,
      getRoleLabel,
      startEdit,
      cancelEdit,
      saveUser,
      openDeleteModal,
      showErrorModal,
      modalErrorMessage,
      showDeleteModal,
      userToDelete,
      confirmDeleteUser,
      cancelDeleteUser
    }
  }
})
</script>

<style scoped>
.users-list {
  font-family: 'Arial', sans-serif;
}

.role-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.role-filter {
  font-size: 14px;
  padding: 4px 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

table {
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
  border-bottom: 1px solid #e0e0e0;
}

tr:hover {
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

.save-button {
  background-color: #5cb85c;
}

.save-button:hover {
  background-color: #4cae4c;
}

.cancel-button {
  background-color: #d9534f;
}

.cancel-button:hover {
  background-color: #c9302c;
}

img {
  width: 16px;
  height: 16px;
}

input, select {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.loader {
  margin-top: 10px;
  color: #6995d0;
}

.error {
  margin-top: 10px;
  color: red;
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
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
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
</style>
