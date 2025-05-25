const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('pages/LoginPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('pages/RegisterPage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('layouts/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/login'
      },
      {
        path: 'student',
        name: 'student-home',
        component: () => import('pages/StudentHomePage.vue')
      },
      {
        path: 'teacher',
        name: 'teacher-home',
        component: () => import('pages/TeacherHomePage.vue')
      },
      {
        path: 'moderator',
        name: 'moderator-home',
        component: () => import('pages/ModeratorHomePage.vue')
      },
      {
        path: 'moderator/group/:id/:name?',
        name: 'group-detail',
        component: () => import('pages/GroupDetailPage.vue'),
        props: true
      },
      {
        path: 'no-role',
        name: 'no-role',
        component: () => import('pages/NoRolePage.vue')
      },
      {
        path: 'student/subject/:id',
        name: 'student-subject-detail',
        component: () => import('pages/StudentSubjectDetail.vue'),
        props: true
      }
    ]
  },
  {
    path: '/',
    component: () => import('layouts/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/login'
      },
      {
        path: 'student-grades',
        name: 'student-grades',
        component: () => import('pages/StudentGradesPage.vue')
      },
      {
        path: 'teacher-grades',
        name: 'teacher-grades',
        component: () => import('pages/TeacherGradesPage.vue')
      },
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
