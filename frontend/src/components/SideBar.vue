<template>
  <aside class="sidebar">
    <div
      class="page-icon-bg"
      :class="{ disabled: isHome }"
      @click="handleBackClick"
      @mouseover="hoverBack"
      @mouseleave="unhoverBack"
    >
      <img class="page-icon" :src="currentPageIcon" alt="icon" />
    </div>
    <div class="page-text">{{ currentTitle }}</div>
    <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
  </aside>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import HomeIcon from '../assets/icons/home.png'
import BackIcon from '../assets/icons/back_blue.png'
import BackIcon2 from '../assets/icons/back_red.png'
import FEFUIcon from '../assets/icons/fefu.png'

export default defineComponent({
  name: 'SidebarMenu',
  setup() {
    const isHovering = ref(false)
    const route = useRoute()
    const router = useRouter()

    const isHome = computed(() =>
      ['moderator-home', 'student-home', 'teacher-home'].includes(route.name as string)
    )

    const currentTitle = computed(() => {
      if (isHome.value) return 'Главная'
      if (route.name === 'group-detail') {
        return decodeURIComponent(route.params.name as string || '')
      }
      return 'Страница'
    })

    const currentPageIcon = computed(() => {
      return isHome.value ? HomeIcon : (isHovering.value ? BackIcon2 : BackIcon)
    })

    const handleBackClick = () => {
      if (!isHome.value) {
        router.back()
      }
    }

    const hoverBack = () => {
      if (!isHome.value) {
        isHovering.value = true
      }
    }

    const unhoverBack = () => {
      isHovering.value = false
    }

    return {
      isHome,
      currentTitle,
      currentPageIcon,
      FEFUIcon,
      handleBackClick,
      hoverBack,
      unhoverBack
    }
  }
})
</script>

<style scoped>
.sidebar {
  width: 70px;
  background: #6995D0;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 100vh;
  align-items: center;
}

.page-icon-bg {
  background: white;
  border: none;
  border-radius: 5px;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.page-icon-bg.disabled {
  pointer-events: none;
  opacity: 0.7;
  cursor: default;
}

.page-icon-bg:hover:not(.disabled) {
  transform: scale(1.05);
}

.page-icon {
  width: 100%;
  height: auto;
}

.page-text {
  transform: rotate(270deg);
  color: white;
  font-size: 30px;
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin: 20px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 70vh;
}

.fefu-icon {
  margin-top: auto;
  width: 100%;
  height: auto;
}
</style>
