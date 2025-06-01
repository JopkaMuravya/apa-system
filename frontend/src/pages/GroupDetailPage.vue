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
            :class="{ active: currentTab === 'students' }"
            @click="currentTab = 'students'"
          >
            Студенты
          </button>
          <button
            :class="{ active: currentTab === 'subjects' }"
            @click="currentTab = 'subjects'"
          >
            Предметы
          </button>
        </div>

        <div class="tab-content">
          <GroupStudents v-if="currentTab === 'students'" />
          <GroupSubjects v-else />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRoute } from 'vue-router'
import SideBar from '../components/SideBar.vue'
import TopBar from '../components/TopBar.vue'
import GroupStudents from '../components/GroupStudents.vue'
import GroupSubjects from '../components/GroupSubjects.vue'

export default defineComponent({
  name: 'GroupDetailPage',
  components: {
    SideBar,
    TopBar,
    GroupStudents,
    GroupSubjects
  },
  setup() {
    const currentTab = ref<'students' | 'subjects'>('students')
    useRoute()
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
