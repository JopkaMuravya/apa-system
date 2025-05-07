<template>
  <form @submit.prevent="onSubmit">
    <input v-model="form.email" type="email" placeholder="Email" />
    <input v-model="form.password" type="password" placeholder="Пароль" />
    <button type="submit">Войти</button>
    <button type="button" @click="goToRegister">Ещё нет аккаунта?</button>
  </form>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

export default {
  setup() {
    const router = useRouter()

    const form = ref({
      email: '',
      password: ''
    })

    const onSubmit = async () => {
      try {
        const response = await api.post('/api/login/', {
          email: form.value.email,
          password: form.value.password
        })

        const user = response.data.user

        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(user))

        if (user.is_superuser) {
          window.location.href = 'http://localhost:8000/admin'
        } else {
          switch (user.role) {
            case 'student':
              router.push('/student')
              break
            case 'teacher':
              router.push('/teacher')
              break
            case 'moderator':
              router.push('/moderator')
              break
            default:
              router.push('/no-role')
          }
        }
      } catch (error) {
        alert('Ошибка входа: ' + (error.response?.data?.detail || error.message))
      }
    }

    const goToRegister = () => {
      router.push('/register')
    }

    return {
      form,
      onSubmit,
      goToRegister
    }
  }
}
</script>