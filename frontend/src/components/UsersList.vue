<template>
  <div class="users-list">
    <table>
      <thead>
        <tr>
          <th>Имя</th>
          <th>Email</th>
          <th>Роль</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.full_name }}</td>
          <td>{{ user.email }}</td>
          <td>
            <select v-model="user.role" @change="changeRole(user)">
              <option value="">Без роли</option>
              <option value="student">Студент</option>
              <option value="teacher">Преподаватель</option>
              <option value="moderator">Модератор</option>
            </select>
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
        if (err instanceof Error) {
          error.value = err.message
        } else {
          error.value = 'Не удалось загрузить пользователей'
        }
      } finally {
        loading.value = false
      }
    }

    const changeRole = async (user: User) => {
      try {
        await api.put('/api/users/', {
          id: user.id,
          role: user.role
        })
      } catch (err) {
        alert('Ошибка при изменении роли')
      }
    }

    onMounted(fetchUsers)

    return {
      users,
      loading,
      error,
      changeRole
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

select {
  padding: 6px;
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
</style>