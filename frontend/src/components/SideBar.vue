<template>
  <aside class="sidebar">
    <button class="page-icon-bg" @click="handleBackClick" :disabled="pageStore.title === 'Главная'" @mouseover="hoverBack" @mouseleave="unhoverBack">
      <img class="page-icon" :src="currentPageIcon" alt="Home" />
    </button>
    <div class="page-text">{{ pageStore.title }}</div>
    <!--<div class="page-text">Основы алгоритмизации...</div>-->
    <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
  </aside>
</template>

<script lang="ts">
  import { defineComponent, computed, ref } from 'vue';
  import { usePageStore } from '../stores/page';
  import HomeIcon from '../assets/icons/home.png';
  import BackIcon from '../assets/icons/back_blue.png';
  import BackIcon2 from '../assets/icons/back_red.png';
  import FEFUIcon from '../assets/icons/fefu.png';

  export default defineComponent({
    name: 'SidebarMenu',
    setup() {
      const pageStore = usePageStore();
      const isHovering = ref(false);
    
      const currentPageIcon = computed(() => {
        if (pageStore.title === 'Главная') {
          return HomeIcon;
        }
        return isHovering.value ? BackIcon2 : BackIcon;
      });

     const handleBackClick = () => {
      if (pageStore.currentSubject) {
        pageStore.resetToHome();
      }
     };

     const hoverBack = () => {
      if (pageStore.title !== 'Главная') {
        isHovering.value = true;
      }
     };

     const unhoverBack = () => {
      isHovering.value = false;
     };

      return {
        pageStore,
        currentPageIcon,
        FEFUIcon,
        handleBackClick,
        hoverBack,
        unhoverBack
      };
    },
  });
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
    cursor: pointer;
    transition: all 0.3s ease;
  }

    .page-icon-bg:hover:not(:disabled) {
      transform: scale(1.05);
    }

    .page-icon-bg:disabled {
      cursor: default;
      opacity: 0.7;
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
