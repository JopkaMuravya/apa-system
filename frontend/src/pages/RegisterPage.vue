<template>
  <form @submit.prevent="onSubmit">
    <input v-model="form.email" type="email" placeholder="Email" />
    <input v-model="form.firstName" placeholder="Имя" />
    <input v-model="form.lastName" placeholder="Фамилия" />
    <input v-model="form.middleName" placeholder="Отчество" />
    <input v-model="form.password" type="password" placeholder="Пароль" />
    <input v-model="form.confirmPassword" type="password" placeholder="Подтверждение пароля" />
    <button type="submit">Зарегистрироваться</button>
    <button type="button" @click="goToLogin">Уже есть аккаунт?</button>
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
      firstName: '',
      lastName: '',
      middleName: '',
      password: '',
      confirmPassword: ''
    })

    const onSubmit = async () => {
      try {
        const response = await api.post('/api/register/', {
          email: form.value.email,
          first_name: form.value.firstName,
          last_name: form.value.lastName,
          middle_name: form.value.middleName,
          password: form.value.password
        })

        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))

        router.push('/')
      } catch (error) {
        alert('Ошибка регистрации: ' + (error.response?.data?.detail || error.message))
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      form,
      onSubmit,
      goToLogin
    }
  }
}
</script>