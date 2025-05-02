<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container>
      <q-page class="flex flex-center">
        <q-card class="q-pa-md" style="width: 400px">
          <q-card-section>
            <div class="text-h6">Регистрация</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit="onSubmit" class="q-gutter-md">
              <q-input
                v-model="form.email"
                label="Email"
                type="email"
                :rules="[
                  val => !!val || 'Email обязателен',
                  val => /.+@.+\..+/.test(val) || 'Введите корректный email'
                ]"
              />

              <q-input
                v-model="form.firstName"
                label="Имя"
                :rules="[val => !!val || 'Имя обязательно']"
              />

              <q-input
                v-model="form.lastName"
                label="Фамилия"
                :rules="[val => !!val || 'Фамилия обязательна']"
              />

              <q-input
                v-model="form.middleName"
                label="Отчество"
              />

              <q-input
                v-model="form.password"
                label="Пароль"
                type="password"
                :rules="[val => val.length >= 8 || 'Пароль должен быть не менее 8 символов']"
              />

              <q-input
                v-model="form.confirmPassword"
                label="Подтверждение пароля"
                type="password"
                :rules="[
                  val => !!val || 'Подтвердите пароль',
                  val => val === form.password || 'Пароли не совпадают'
                ]"
              />

              <div>
                <q-btn label="Зарегистрироваться" type="submit" color="primary"/>
                <q-btn label="Войти" to="/login" flat class="q-ml-sm"/>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const $q = useQuasar()
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

        $q.notify({
          type: 'positive',
          message: 'Регистрация прошла успешно!'
        })

        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        router.push('/')
      } catch (error) {
        const errors = error.response?.data
        if (errors) {
          for (const field in errors) {
            $q.notify({
              type: 'negative',
              message: `${field}: ${Array.isArray(errors[field]) ? errors[field].join(', ') : errors[field]}`
            })
          }
        } else {
          $q.notify({
            type: 'negative',
            message: error.message || 'Ошибка регистрации'
          })
        }
      }
    }

    return {
      form,
      onSubmit
    }
  }
}
</script>