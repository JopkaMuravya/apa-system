<template>
  <div class="main-page">
    <SideBar />
    <div class="content">
      <div class="topbar-wrapper">
        <TopBar />
      </div>

      <div class="inner-content group-detail">
        <div v-if="loading">Загрузка данных...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else>
          <h3>Студенты</h3>
          <table class="students-table">
            <thead>
              <tr>
                <th>№</th>
                <th>ФИО</th>
                <th>Корпоративная почта</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, index) in sortedStudents" :key="student.id">
                <td>{{ index + 1 }}</td>
                <td>{{ student.full_name }}</td>
                <td>{{ student.email }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'

import SideBar from '../components/SideBar.vue'
import TopBar from '../components/TopBar.vue'

interface Student {
  id: number
  full_name: string
  email: string
}

export default defineComponent({
  name: 'GroupDetailPage',
  components: {
    SideBar,
    TopBar
  },
  setup() {
    const route = useRoute()
    const students = ref<Student[]>([])
    const loading = ref(true)
    const error = ref('')

    const fetchGroupData = async () => {
      try {
        const { data } = await api.get(`/api/groups/${route.params.id}/`)
        students.value = data.students
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        error.value = e.response?.data?.detail || 'Ошибка при загрузке данных группы'
      } finally {
        loading.value = false
      }
    }

    const sortedStudents = computed(() =>
      [...students.value].sort((a, b) => a.full_name.localeCompare(b.full_name))
    )

    onMounted(fetchGroupData)

    return {
      students,
      sortedStudents,
      loading,
      error
    }
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

.group-detail h3 {
  margin-bottom: 15px;
}

.error {
  color: red;
  margin-top: 10px;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.students-table th,
.students-table td {
  padding: 8px 12px;
  border: 1px solid #ccc;
  text-align: left;
}
</style>
