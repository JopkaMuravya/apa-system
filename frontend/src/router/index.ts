import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  // Проверяем, есть ли токен аутентификации в localStorage
  const isAuthenticated = !!localStorage.getItem('token')

  // Получаем роль пользователя из localStorage
  let userRole = null
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      userRole = user.role
    } catch (e) {
      userRole = null
    }
  }

  // Если маршрут требует аутентификации, но пользователь не аутентифицирован, перенаправляем на /login
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } 
  // Если маршрут имеет ограничения по ролям
  else if (to.meta.roles && Array.isArray(to.meta.roles) && to.meta.roles.length > 0) {
    // Если роль пользователя разрешена для маршрута, разрешаем переход
    if ((userRole === null && to.meta.roles.includes('waiting')) || to.meta.roles.includes(userRole)) {
      next()
    } 
    // Иначе перенаправляем пользователя на домашнюю страницу, соответствующую его роли
    else {
      switch (userRole) {
        case 'student':
          next('/student')
          break
        case 'teacher':
          next('/teacher')
          break
        case 'moderator':
          next('/moderator')
          break
        case 'waiting':
        default:
          next('/no-role')
      }
    }
  } 
  // Если нет ограничений, разрешаем переход
  else {
    next()
  }
})

export default router