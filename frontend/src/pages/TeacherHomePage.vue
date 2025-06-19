<template>
  <div class="main-page">
    <SideBar />
    <div class="content">
      <TopBar @search="search" />
      <div class="task-list-wrapper">
        <SubjectsList :searchQuery="searchQuery" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import SideBar from '../components/SideBar.vue';
  import TopBar from '../components/TopBar.vue';
  import SubjectsList from '../components/SubjectsList.vue';
  import { useRoute } from 'vue-router';

  export default defineComponent({
    name: 'MainPage',
    components: {
      SideBar,
      TopBar,
      SubjectsList,
    },
    data() {
      return {
        currentPageTitle: 'Главная',
        searchQuery: ''
      };
    },
    created() {
      const route = useRoute();
      if (route.query.search) {
        this.searchQuery = route.query.search as string;
        this.search(this.searchQuery);
      }
    },
    provide() {
      return {
        updatePageTitle: (title: string) => {
          this.currentPageTitle = title;
        },
        currentPageTitle: this.currentPageTitle
      };
    },
    methods: {
      search(query: string) {
        this.searchQuery = query;
      }
    },
  });
</script>

<style scoped>
  .main-page {
    display: flex;
    height: 100vh;
    background: #ffffff;
    font-family: 'Arial', sans-serif;
    position: relative;
  }

  .content {
    flex: 1;
    padding: 8px 15px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 1;
    padding-bottom: 70px;
  }

  @media (min-width: 769px) {
    .content {
      padding-bottom: 0;
    }
  }

  .task-list-wrapper {
    flex: 1;
    overflow-y: auto;
    padding-right: 10px;
    scrollbar-width: thin;
  }

    .task-list-wrapper::-webkit-scrollbar {
      width: 8px;
    }

    .task-list-wrapper::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.5);
      border-radius: 4px;
    }

      .task-list-wrapper::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.8);
      }
</style>  
