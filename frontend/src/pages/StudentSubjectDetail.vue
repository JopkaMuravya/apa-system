<template>
  <div class="main-page">
    <SideBar />
    <div class="content">
      <TopBar />
      <div class="subject-content">
        <h1>{{ subjectName }}</h1>
        <p>тут будет подробная информация о предмете</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import SideBar from '../components/SideBar.vue';
import TopBar from '../components/TopBar.vue';

export default defineComponent({
  name: 'StudentSubjectDetail',
  components: { SideBar, TopBar },
  setup() {
    const route = useRoute();
    const subjectName = ref('Загрузка...');

    onMounted(() => {
      if (route.query.name) {
        subjectName.value = route.query.name as string;
      } else if (route.params.id) {
        subjectName.value = `Предмет ID: ${route.params.id}`;
      } else {
        subjectName.value = 'Предмет не найден';
      }
    });

    return {
      subjectName,
    };
  },
});
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
  background: #ffffff;
  font-family: Arial, sans-serif;
  position: relative;
}

.content {
  flex: 1;
  padding: 8px 15px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1;
}

.subject-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
  scrollbar-width: thin;
}

.subject-content::-webkit-scrollbar {
  width: 8px;
}

.subject-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 4px;
}

.subject-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.8);
}
</style>
