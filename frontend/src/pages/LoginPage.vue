<template>
  <div class="layer">
			<div class="form_wrapper">
            <div class="form_container">
              <div class="title_container">
                <h2>Вход</h2>
              </div>

              <div class="row clearfix">
                <div>
                  <form @submit.prevent="onSubmit">
                    <div class="input_field">
						            <span class="icon">
                          <i class="fa-solid fa-envelope"></i>
                        </span>
                      	<input v-model="form.email" type="email" placeholder="Email"/>
                    </div>

                    <div class="input_field">
						            <span class="icon">
                          <i class="fa fa-lock"></i>
                        </span>
                        <input v-model="form.password" type="password" placeholder="Пароль" id="password"/>
						            <span class="eye" @click="hidePassword">
                          <i class="fa-solid fa-eye"></i>
                        </span>
                    </div>

                    <input class="button" type="submit" value="Войти"/>
                  </form>
                </div>
              </div>

              <div class="login_container">
                <a href="#" class="forgot_password" @click="goToRegister">Еще нет аккаунта? <b>Зарегистрироваться</b></a>
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

    const hidePassword = () => {
      var x = document.getElementById('password');
      if (x.type === 'password') {
        x.type = 'text';
      } else {
        x.type = 'password';
      }
    }

    return {
      form,
      onSubmit,
      goToRegister,
      hidePassword
    }
  },
}
</script>

<style>
@import "../css/auth.scss";
</style>
