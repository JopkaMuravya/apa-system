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
            <input v-model="form.firstName" placeholder="Имя" type="text" />
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-user"></i>
            </span>
            <input v-model="form.lastName" placeholder="Фамилия" type="text" />
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-user"></i>
            </span>
            <input v-model="form.middleName" placeholder="Отчество (при наличии)" type="text" />
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa-solid fa-envelope"></i>
            </span>
            <input v-model="form.email" type="email" placeholder="Email" />
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa fa-lock"></i>
            </span>
            <input
              v-model="form.password"
              placeholder="Пароль"
              type="password"
              id="password1"
            />
            <span class="eye" @click="togglePassword('password1')">
              <i aria-hidden="true" class="fa-solid fa-eye"></i>
            </span>
          </div>

          <div class="input_field">
            <span class="icon">
              <i aria-hidden="true" class="fa fa-lock"></i>
            </span>
            <input
              v-model="form.confirmPassword"
              placeholder="Подтверждение пароля"
              type="password"
              id="password2"
            />
            <span class="eye" @click="togglePassword('password2')">
              <i aria-hidden="true" class="fa-solid fa-eye"></i>
            </span>
          </div>

          <input class="button" type="submit" value="Зарегистрироваться" />
        </form>

        <div class="centered_container">
          <a href="#" class="forgot_password" @click="goToLogin">
            Уже есть аккаунт? <b>Войти</b>
          </a>
        </div>
      </div>
    </div>

    <ErrorModal
      :isOpen="showErrorModal"
      :message="errorMessage"
      @close="showErrorModal = false"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import ErrorModal from '../components/ErrorModal.vue'

const unauthApi = axios.create({ baseURL: 'http://localhost:8000' })

export default {
  components: {
    ErrorModal
  },

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

    const showErrorModal = ref(false)
    const errorMessage = ref('')

    const showError = (message) => {
      errorMessage.value = message
      showErrorModal.value = true
    }

    const onSubmit = async () => {
      const allowedDomain = 'dvfu.ru';
      const emailDomain = form.value.email.split('@')[1];

      if (emailDomain !== allowedDomain) {
        showError(`Разрешена регистрация только с email домена @${allowedDomain}`);
        return;
      }

      if (form.value.password !== form.value.confirmPassword) {
        showError('Пароли не совпадают!');
        return;
      }

      try {
        const response = await unauthApi.post('/api/register/', {
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
        showError('Ошибка регистрации: ' + (error.response?.data?.detail || error.message))
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    const togglePassword = (id) => {
      const el = document.getElementById(id)
      if (el) {
        el.type = el.type === 'password' ? 'text' : 'password'
      }
    }

    return {
      form,
      onSubmit,
      goToLogin,
      showErrorModal,
      errorMessage,
      togglePassword
    }
  }
}
</script>

<style>
@import "../css/auth.scss";
</style>
