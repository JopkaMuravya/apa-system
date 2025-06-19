<template>
  <div class="main-page">
    <SideBar />
    <div class="content">
      <div class="topbar-wrapper">
        <TopBar />
      </div>

      <div class="inner-content">
        <div class="tab-switcher">
          <button
            :class="{ active: currentTab === 'users' }"
            @click="currentTab = 'users'"
          >
            Все пользователи
          </button>
          <button
            :class="{ active: currentTab === 'groups' }"
            @click="currentTab = 'groups'"
          >
            Учебные группы
          </button>
          <button
            :class="{ active: currentTab === 'subjects' }"
            @click="currentTab = 'subjects'"
          >
            Предметы и преподаватели
          </button>
        </div>

        <div class="tab-content">
          <UsersList v-if="currentTab === 'users'" />
          <GroupsList v-else-if="currentTab === 'groups'" />
          <SubjectsTeachers v-else />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import SideBar from '../components/SideBar.vue'
import TopBar from '../components/TopBar.vue'
import UsersList from '../components/UsersList.vue'
import GroupsList from '../components/GroupsList.vue'
import SubjectsTeachers from '../components/SubjectsTeachers.vue'
import { usePageStore } from '../stores/page';

export default defineComponent({
  name: 'ModeratorHomePage',
  components: {
    SideBar,
    TopBar,
    UsersList,
    GroupsList,
    SubjectsTeachers
  },
  setup() {
    const currentTab = ref<'users' | 'groups' | 'subjects'>('users')
    const pageStore = usePageStore();

    onMounted(() => {
      pageStore.setIsTeacher(false);
    });
    return { currentTab }
  }
})
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
  background: #ffffff;
  font-family: 'Arial', sans-serif;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1;
  height: 100vh;
  box-sizing: border-box;
}

.topbar-wrapper {
  flex-shrink: 0;
  padding: 0 20px;
  margin: 10px 0 10px;
}

.inner-content {
  padding: 0 20px 20px;
  flex: 1;
  overflow-y: auto;
}

.tab-switcher {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-switcher button {
  padding: 10px 20px;
  border: none;
  background-color: #e0eafc;
  color: #335d92;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.tab-switcher button.active {
  background-color: #6995d0;
  color: white;
}

.tab-content {
  margin-top: 10px;
}
</style>
