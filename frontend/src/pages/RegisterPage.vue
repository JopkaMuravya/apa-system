<template>
  <div class="background">
    <div class="layer">
      <div class="form_wrapper">
        <div class="centered_container">
          <h2>Регистрация</h2>
        </div>

        <form @submit.prevent="onSubmit">
          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-user"></i>
            </span>
            <input v-model="form.firstName" placeholder="Имя" type="text"/>
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-user"></i>
            </span>
            <input v-model="form.lastName" placeholder="Фамилия" type="text"/>
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-user"></i>
            </span>
            <input v-model="form.middleName" placeholder="Отчество (при наличии)" type="text"/>
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-envelope"></i>
            </span>
            <input v-model="form.email" type="email" placeholder="Email"/>
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa fa-lock"></i>
            </span>
            <input v-model="form.password" placeholder="Пароль" type="password" id="password1"/>
            <span class="eye" @click="hidePassword">
              <i aria-hidden="true" class="fa-solid fa-eye"></i>
            </span>
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa fa-lock"></i>
            </span>
            <input v-model="form.confirmPassword" placeholder="Подтверждение пароля" type="password" id="password2"/>
          </div>

          <input class="button" type="submit" value="Зарегистрироваться" />
        </form>

        <div class="centered_container">
          <a href="#" class="forgot_password" @click="goToLogin">Уже есть аккаунт? <b>Войти</b></a>
        </div>
      </div>
    </div>
  </div>
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

    const hidePassword = () => {
      var x1 = document.getElementById('password1');
      var x2 = document.getElementById('password2');

      if (x1.type === 'password') {
        x1.type = 'text';
      } else {
        x1.type = 'password';
      }

      if (x2.type === 'password') {
        x2.type = 'text';
      } else {
        x2.type = 'password';
      }
    }

    return {
      form,
      onSubmit,
      goToLogin,
      hidePassword
    }
  }
}
</script>

<style>
@import "../css/auth.scss";
</style>
