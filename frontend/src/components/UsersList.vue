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
          <td>{{ user.full_name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ getRoleLabel(user.role) }}</td>
          <td class="action-buttons">
            <button class="edit-button" @click="editUser(user)">
              <img :src="EditIcon" alt="Редактировать" />
            </button>
            <button class="delete-button" @click="deleteUser(user)">
              <img :src="DeleteIcon" alt="Удалить" />
            </button>
          </td>
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
        case 'admin': return 'Админ'
        default: return 'Без роли'
      }
    }

    const deleteUser = (user: User) => {
      console.log('Удалить пользователя:', user)
    }

    const editUser = (user: User) => {
      console.log('Редактировать пользователя:', user)
    }

    onMounted(fetchUsers)

    return {
      users,
      loading,
      error,
      deleteUser,
      editUser,
      getRoleLabel,
      DeleteIcon,
      EditIcon
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
.edit-button {
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

.delete-button {
  background-color: #d9534f;
}

.delete-button:hover {
  transform: scale(1.1);
  background-color: #c9302c;
}

.edit-button {
  background-color: #5cb85c;
}

.edit-button:hover {
  transform: scale(1.1);
  background-color: #4cae4c;
}

.delete-button img,
.edit-button img {
  width: 16px;
  height: 16px;
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
