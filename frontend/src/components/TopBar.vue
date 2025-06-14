<template>
  <div class="top-menu">
    <div class="search-wrapper">
      <img class="search-icon" :src="SearchIcon" alt="Поиск" />
      <input
        type="text"
        class="search-input"
        v-model="searchQuery"
        placeholder="Поиск..."
      />
    </div>
    <div class="user">
      {{ fullName }}
      <span v-if="group && role === 'student'" class="user-group">({{ group.name }})</span>
    </div>
    <button
      class="exit-button"
      @click="login"
      @mouseover="hoverExit"
      @mouseleave="unhoverExit"
    >
      <img :src="currentExitIcon" alt="Выйти" />
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import ExitIcon from '../assets/icons/exit_blue.png'
import ExitIcon2 from '../assets/icons/exit_red.png'
import SearchIcon from '../assets/icons/search.png'
import { api } from '../boot/axios'

interface Group {
  id: number
  name: string
}

export default defineComponent({
  name: 'TopBar',
  setup() {
    const searchQuery = ref('')
    const currentExitIcon = ref(ExitIcon)
    const fullName = ref('')
    const group = ref<Group | null>(null)
    const role = ref('')

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

    onMounted(() => {
      fetchCurrentUser()
    })

    const login = () => {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      window.location.href = '/login'
    }

    const hoverExit = () => {
      currentExitIcon.value = ExitIcon2
    }

    const unhoverExit = () => {
      currentExitIcon.value = ExitIcon
    }

    return {
      searchQuery,
      currentExitIcon,
      SearchIcon,
      fullName,
      group,
      role,
      login,
      hoverExit,
      unhoverExit
    }
  }
})
</script>

<style scoped>
  .top-menu {
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
    pointer-events: none; 
  }

  .user {
    color: white;
    font-size: 25px;
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 45%;
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
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    min-width: 2%;
  }

    .exit-button:hover {
      transform: scale(1.05);
    }

    .exit-button img {
      width: 24px;
      height: 24px;
    }
</style>
