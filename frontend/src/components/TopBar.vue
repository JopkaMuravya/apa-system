<template>
  <div class="top-menu">
    <div class="search-wrapper">
      <img class="search-icon" :src="SearchIcon" alt="Поиск" />
      <input type="text"
              class="search-input"
              v-model="searchQuery"
              placeholder="Поиск..." />
    </div>
    <div class="user">Сущенко Андрей Андреевич</div>
    <button class="exit-button" @click="login" @mouseover="hoverExit" @mouseleave="unhoverExit">
      <img :src="currentExitIcon" alt="Выйти" />
    </button>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import AddIcon from '../assets/icons/add.png';
  import ExitIcon from '../assets/icons/exit_blue.png';
  import ExitIcon2 from '../assets/icons/exit_red.png';
  import SearchIcon from '../assets/icons/search.png';

  export default defineComponent({
    data() {
      return {
        searchQuery: '',
        AddIcon,
        ExitIcon,
        ExitIcon2,
        SearchIcon,
        currentExitIcon: ExitIcon
      };
    },
    methods: {
      login() {
        this.$router.push('/login');
      },
      hoverExit() {
        this.currentExitIcon = this.ExitIcon2;
      },
      unhoverExit() {
        this.currentExitIcon = this.ExitIcon;
      }
    },
  });
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
