<template>
  <div>
    <!-- Десктопная версия -->
    <aside class="sidebar desktop" v-if="!isMobile">
      <div class="page-icon-bg"
           :class="{ disabled: isDisabled }"
           @click="handleBackClick"
           @mouseover="hoverBack"
           @mouseleave="unhoverBack">
        <img class="page-icon" :src="currentPageIcon" alt="icon" />
      </div>
      <div class="page-text">{{ currentTitle }}</div>
      <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
    </aside>

    <!-- Мобильная версия (только для студентов и преподавателей) -->
    <div class="mobile-sidebar" v-if="isMobile && (isStudent || isTeacher || isGradesPage)">
      <div class="mobile-sidebar-content">
        <div class="mobile-back-button"
             :class="{ disabled: isDisabled }"
             @click="handleBackClick">
          <img class="mobile-page-icon" :src="currentPageIcon" alt="back" />
        </div>
        <div class="mobile-page-title">{{ currentTitle }}</div>
        <button class="mobile-exit-button"
                @click="logout">
          <img :src="ExitIcon" alt="Выйти" />
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, computed, ref, onMounted, onUnmounted } from 'vue';
  import { usePageStore } from '../stores/page';
  import { useRoute, useRouter } from 'vue-router';
  const HomeIcon = new URL('../assets/icons/home.png', import.meta.url).href;
  const BackIcon = new URL('../assets/icons/back_blue.png', import.meta.url).href;
  const BackIcon2 = new URL('../assets/icons/back_red.png', import.meta.url).href;
  const FEFUIcon = new URL('../assets/icons/fefu.png', import.meta.url).href;
  const ExitIcon = new URL('../assets/icons/exit_blue.png', import.meta.url).href

export default defineComponent({
  name: 'SidebarMenu',
  setup() {
    const isHovering = ref(false);
    const pageStore = usePageStore();
    const route = useRoute();
    const router = useRouter();

    const isMobile = ref(false);

    const isStudent = computed(() => route.name === 'student-home');
    const isTeacher = computed(() => route.name === 'teacher-home');
    const isGradesPage = computed(() => {
      return route.name === 'teacher-grades' || route.name === 'student-grades';
    });

    // Проверка на мобильное устройство
    const checkMobile = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    onMounted(() => {
      checkMobile();
      window.addEventListener('resize', checkMobile);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile);
    });

    const isHome = computed(() =>
      ['moderator-home', 'student-home', 'teacher-home'].includes(route.name as string)
    );

    const isDisabled = computed(() => {
      return pageStore.isTeacher ? !pageStore.showBackButton : isHome.value;
    });

    const currentTitle = computed(() => {
      if (pageStore.isTeacher) {
        return pageStore.sidebarTitle;
      } else {
        if (isHome.value) return 'Главная';
        if (route.name === 'group-detail') {
          return decodeURIComponent(route.params.name as string || '');
        }
        if (route.name === 'student-grades') {
          return route.query.subjectName as string || 'Предмет';
        }
        if (route.name === 'teacher-grades') {
          return route.query.subjectName as string || 'Предмет';
        }
        return 'Страница';
      }
    });

    const currentPageIcon = computed(() => {
      if (pageStore.isTeacher) {
        return !pageStore.showBackButton
          ? HomeIcon
          : (isHovering.value ? BackIcon2 : BackIcon);
      } else {
        return isHome.value ? HomeIcon : (isHovering.value ? BackIcon2 : BackIcon);
      }
    });

    const handleBackClick = () => {
      if (pageStore.isTeacher) {
        if (pageStore.showBackButton) {
          if (route.name === 'teacher-grades') {
            router.back();
          } else {
            pageStore.clearSubject();
          }
        }
      } else {
        if (!isHome.value) {
          router.back();
        }
      }
    };

    const hoverBack = () => {
      if (pageStore.isTeacher ? pageStore.showBackButton : !isHome.value) {
        isHovering.value = true;
      }
    };

    const unhoverBack = () => {
      isHovering.value = false;
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };



    return {
      isMobile,
      isStudent,
      isTeacher,
      isGradesPage,
      isDisabled,
      currentTitle,
      currentPageIcon,
      ExitIcon,
      FEFUIcon,
      handleBackClick,
      hoverBack,
      unhoverBack,
      logout,
      pageStore

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


  .mobile-sidebar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #6995D0;
    padding: 10px 15px;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    z-index: 100;
  }

  .mobile-sidebar-content {
    display: flex;
    align-items: center;
    gap: 15px;
    width: 100%; 
  }

  .mobile-back-button {
    background: white;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    cursor: pointer;
    flex-shrink: 0;
  }

  .mobile-page-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-grow: 1; 
    text-align: center; 
    padding: 0 10px; 
  }

  .mobile-exit-button {
    background: white;
    border-radius: 10px;
    width: 40px;
    border: none;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    cursor: pointer;
    flex-shrink: 0; 
    margin-left: auto;
  }

  .mobile-back-button.disabled {
    opacity: 0.5;
    pointer-events: none;
  }

  .mobile-page-icon {
    width: 24px;
    height: 24px;
  }

  .mobile-exit-button img {
    width: 25px;
    height: 25px;
    transition: all 0.3s ease;
  }

  .main-page .content {
    padding-bottom: 70px;
  }

  @media (min-width: 769px) {
    .main-page .content {
      padding-bottom: 0;
    }
  }

</style>
