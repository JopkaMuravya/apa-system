<template>
  <div class="users-list">
    <table>
      <thead>
        <tr>
          <th>ФИО</th>
          <th>Корпоративная почта</th>
          <th>Роль</th>
          <th class="action-header">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
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
              <button class="delete-button" @click="deleteUser(user)">
                <img :src="DeleteIcon" alt="Удалить" />
              </button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>

    <div v-if="loading" class="loader">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
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
  setup() {
    const users = ref<User[]>([])
    const loading = ref(false)
    const error = ref('')
    const editingUserId = ref<number | null>(null)
    const editForm = ref({
      id: 0,
      full_name: '',
      email: '',
      role: ''
    })

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
        const e = err as AxiosError<{ detail?: string }>
        const detail = e.response?.data?.detail || 'Ошибка при сохранении'
        alert(detail)
      }
    }

    const deleteUser = async (user: User) => {
      const confirmed = confirm(`Удалить пользователя ${user.full_name}?`)
      if (!confirmed) return

      try {
        await api.delete(`/api/users/${user.id}/`)
        fetchUsers()
      } catch (err) {
        alert('Не удалось удалить пользователя')
      }
    }

    onMounted(fetchUsers)

    return {
      users,
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
      deleteUser
    }
  }
})
</script>

<style scoped>
.users-list {
  font-family: 'Arial', sans-serif;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
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
  padding: 5px;
  font-size: 14px;
}

.loader {
  margin-top: 10px;
  color: #6995d0;
}

.error {
  margin-top: 10px;
  color: red;
}
</style>
