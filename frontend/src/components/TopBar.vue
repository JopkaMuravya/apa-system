<template>
  <div class="top-menu">
    <!-- Десктопная версия -->
    <div class="desktop-top-bar" v-if="!isMobile">
      <div class="search-wrapper">
        <img class="search-icon" :src="SearchIcon" alt="Поиск" @click="search" />
        <input
          type="text"
          class="search-input"
          v-model="searchQuery"
          placeholder="Поиск..."
          @keyup.enter="search"
        />
      </div>
      <div class="user">
        {{ fullName }}
        <span v-if="group && role === 'student'" class="user-group">({{ group.name }})</span>
      </div>
      <button class="support-button" @click="openSupport">
        <img :src="SupportIcon" alt="Поддержка" />
      </button>
      <button class="exit-button"
              @click="login"
              @mouseover="hoverExit"
              @mouseleave="unhoverExit">
        <img :src="currentExitIcon" alt="Выйти" />
      </button>
    </div>

    <!-- Мобильная версия -->
    <div class="mobile-top-bar" v-if="isMobile">
      <div class="mobile-user-info" v-if="!isSearchExpanded">
        <div class="mobile-user-name">
          {{ fullName }}
          <span v-if="group && role === 'student'" class="mobile-user-group">({{ group.name }})</span>
        </div>
        <button class="mobile-search-button" @click="expandSearch">
          <img class="mobile-search-icon" :src="SearchIcon" alt="Поиск" />
        </button>
      </div>

      <div class="mobile-search-wrapper" v-else>
        <button class="mobile-search-button" @click="search">
          <img :src="SearchIcon" alt="Найти" width="16">
        </button>
        <input type="text"
               class="mobile-search-input"
               v-model="searchQuery"
               placeholder="Поиск..."
               ref="searchInput"
               @keyup.enter="search" />
        <button class="mobile-search-close" @click="collapseSearch">
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, nextTick } from 'vue'
const ExitIcon = new URL('../assets/icons/exit_blue.png', import.meta.url).href
const ExitIcon2 = new URL('../assets/icons/exit_red.png', import.meta.url).href
const SearchIcon = new URL('../assets/icons/search.png', import.meta.url).href
const SupportIcon = new URL('../assets/icons/help.png', import.meta.url).href;
import { api } from '../boot/axios'
import { useRoute, useRouter } from 'vue-router';

interface Group {
  id: number
  name: string
}

export default defineComponent({
  name: 'TopBar',
  emits: ['search'],
  setup(props, { emit }) {
    const router = useRouter()
    const route = useRoute();
    const searchQuery = ref('')
    const currentExitIcon = ref(ExitIcon)
    const fullName = ref('')
    const group = ref<Group | null>(null)
    const role = ref('')
    const isMobile = ref(false)
    const isSearchExpanded = ref(false)
    const searchInput = ref<HTMLInputElement | null>(null)

    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 768
    }

    const fetchCurrentUser = async () => {
      try {
        const response = await api.get('/api/current-user/')
        const user = response.data
        const parts = [
          user.last_name,
          user.first_name,
          user.middle_name || ''
        ].filter(Boolean)
        fullName.value = parts.join(' ')
        group.value = user.group || null
        role.value = user.role || ''
      } catch (error) {
        console.error('Ошибка при получении данных пользователя:', error)
        fullName.value = 'Пользователь'
        group.value = null
        role.value = ''
      }
    }

    const expandSearch = async () => {
      isSearchExpanded.value = true
      await nextTick()
      searchInput.value?.focus()
    }

    const collapseSearch = () => {
      isSearchExpanded.value = false
      searchQuery.value = ''
    }

    const search = () => {
      const currentPath = route.path;
      const isGradesPage = currentPath.includes('-grades');

      if (isGradesPage) {
        emit('search', searchQuery.value);
      } else {
        let homePath = ''
        switch (role.value) {
          case 'student':
            homePath = '/student'
            break
          case 'teacher':
            homePath = '/teacher'
            break
          case 'moderator':
            homePath = '/moderator'
            break
        }
        if (route.path !== homePath) {
          router.push({
            path: homePath,
            query: { search: searchQuery.value }
          })
        } else {
          emit('search', searchQuery.value)
        }
      }
    }

    onMounted(() => {
      if (route.query.search) {
        searchQuery.value = route.query.search.toString();
      }
      checkMobile()
      window.addEventListener('resize', checkMobile)
      fetchCurrentUser()
    })

    const login = () => {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      router.push('/login')
    }

    const hoverExit = () => {
      currentExitIcon.value = ExitIcon2
    }

    const unhoverExit = () => {
      currentExitIcon.value = ExitIcon
    }

    const openSupport = () => {
      const email = 'NEgovnoedka@yandex.ru';
      const subject = encodeURIComponent('Поддержка ДВФУ');
      const body = encodeURIComponent(
        'Здравствуйте!\n\nМне нужна помощь по следующему вопросу:\n\n' +
        '----------------------------------\n' +
        'Дополнительная информация:\n' +
        '• Страница: ' + window.location.href + '\n' +
        '• Время: ' + new Date().toLocaleString() + '\n' +
        '• Браузер: ' + navigator.userAgent + '\n' +
        '• ОС: ' + navigator.platform
      );

      window.open('https://mail.yandex.ru/?uid=1130000065432#compose?to=' + email + '&subject=' + subject + '&body=' + body, '_blank');
    };

    return {
      SupportIcon,
      openSupport,
      searchQuery,
      currentExitIcon,
      SearchIcon,
      fullName,
      group,
      role,
      isMobile,
      isSearchExpanded,
      searchInput,
      login,
      hoverExit,
      unhoverExit,
      expandSearch,
      collapseSearch,
      search
    }
  }
})
</script>

<style scoped>

.top-menu {
  width: 100%;
}

.desktop-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background: #6995D0;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.search-wrapper {
  flex: 1;
  position: relative;
  margin: 0 10px;
  min-width: 45%;
}

.search-input {
  width: 100%;
  height: 40px;
  padding: 10px 15px 10px 40px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  color: #1b263b;
  font-weight: bold;
  background: #ffffff;
}

.search-icon {
  position: absolute;
  left: 10px;
  right: auto;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.user {
  color: white;
  font-size: 25px;
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 45%;
  user-select: none;
}

.user-group {
  font-size: 16px;
  margin-left: 8px;
  opacity: 0.8;
}

.exit-button {
  height: 40px;
  background: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  margin-left: 10px;
}

.exit-button:hover {
  transform: scale(1.05);
}

.exit-button img {
  width: 24px;
  height: 24px;
}

.support-button {
  height: 40px;
  background: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  min-width: 2%;
}

.support-button img {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease;
}

.support-button:hover img {
  transform: scale(1.1);
}

.mobile-top-bar {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background: #6995D0;
  margin-left: -15px;
  margin-right: -15px;
  margin-top: -10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  height: 80px;
}

.mobile-user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.mobile-user-name {
  color: white;
  font-size: 25px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 85%;
  user-select: none;
}

.mobile-user-group {
  font-size: 14px;
  opacity: 0.9;
}

.mobile-search-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 10px;
  border: none;
  padding: 8px;
  cursor: pointer;
}

.mobile-search-icon {
  width: 20px;
  height: 20px;
}

.mobile-search-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
}

.mobile-search-input {
  width: 100%;
  height: 36px;
  padding: 8px 35px 8px 15px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  color: #1b263b;
  font-size: 14px;
  background: #ffffff;
  margin-left: 10px;
}

.mobile-search-close {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  padding: 0 5px;
}

@media (min-width: 769px) {
  .mobile-top-bar {
    display: none;
  }
}
</style>
