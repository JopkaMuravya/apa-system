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
        component: () => import('pages/StudentHomePage.vue'),
        meta: { roles: ['student'] }
      },
      {
        path: 'teacher',
        name: 'teacher-home',
        component: () => import('pages/TeacherHomePage.vue'),
        meta: { roles: ['teacher'] }
      },
      {
        path: 'moderator',
        name: 'moderator-home',
        component: () => import('pages/ModeratorHomePage.vue'),
        meta: { roles: ['moderator'] }
      },
      {
        path: 'moderator/group/:id/:name?',
        name: 'group-detail',
        component: () => import('pages/GroupDetailPage.vue'),
        props: true,
        meta: { roles: ['moderator'] }
      },
      {
        path: 'no-role',
        name: 'no-role',
        component: () => import('pages/NoRolePage.vue'),
        meta: { roles: ['waiting'] }
      },
      {
        path: 'student/subject/:id',
        name: 'student-subject-detail',
        component: () => import('pages/StudentSubjectDetail.vue'),
        props: true,
        meta: { roles: ['student'] }
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
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
