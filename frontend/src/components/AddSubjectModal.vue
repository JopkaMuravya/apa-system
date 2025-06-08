<template>
  <div class="modal-backdrop">
    <div class="add-modal">
      <h2>Добавить предмет</h2>

      <input
        v-model="subjectName"
        type="text"
        placeholder="Название предмета"
        class="search-input"
      />

      <input
        v-model="search"
        type="text"
        placeholder="Поиск преподавателя..."
        class="search-input"
      />

      <div class="teacher-scroll-wrapper">
        <div
          v-for="teacher in filteredTeachers"
          :key="teacher.id"
          class="teacher-item"
        >
          <label>
            <input
              type="checkbox"
              :value="teacher.id"
              v-model="selectedTeacherIds"
            />
            {{ teacher.full_name }}
          </label>
        </div>
      </div>

      <button class="submit-btn" @click="createSubject">Сохранить</button>
      <button class="close-btn" @click="$emit('close')">Закрыть</button>
    </div>

    <div v-if="showErrorModal" class="modal-backdrop inner">
      <div class="error-modal">
        <h2>Ошибка</h2>
        <p>{{ errorMessage }}</p>
        <button @click="showErrorModal = false">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'

interface Teacher {
  id: number
  full_name: string
}

interface RawUser {
  id: number
  first_name: string
  last_name: string
  middle_name?: string
  role: string
}

export default defineComponent({
  name: 'AddSubjectModal',
  emits: ['close', 'subject-added'],
  setup(_, { emit }) {
    const subjectName = ref('')
    const search = ref('')
    const teachers = ref<Teacher[]>([])
    const selectedTeacherIds = ref<number[]>([])

    const showErrorModal = ref(false)
    const errorMessage = ref('')

    const fetchTeachers = async () => {
      try {
        const res = await api.get('/api/users/')
        teachers.value = (res.data as RawUser[])
          .filter((u: RawUser) => u.role === 'teacher')
          .map((t: RawUser) => ({
            id: t.id,
            full_name: `${t.last_name} ${t.first_name} ${t.middle_name || ''}`.trim()
          }))
      } catch {
        errorMessage.value = 'Ошибка при загрузке преподавателей'
        showErrorModal.value = true
      }
    }

    const filteredTeachers = computed(() =>
      teachers.value.filter(t =>
        t.full_name.toLowerCase().includes(search.value.toLowerCase())
      )
    )

    const createSubject = async () => {
      if (!subjectName.value.trim()) {
        errorMessage.value = 'Название предмета обязательно'
        showErrorModal.value = true
        return
      }

      try {
        const res = await api.post('/api/subjects/create_with_teachers/', {
          name: subjectName.value.trim(),
          teacher_ids: selectedTeacherIds.value
        })

        emit('subject-added', res.data)
        emit('close')
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        errorMessage.value = e.response?.data?.detail || 'Не удалось создать предмет'
        showErrorModal.value = true
      }
    }

    onMounted(fetchTeachers)

    return {
      subjectName,
      search,
      teachers,
      selectedTeacherIds,
      filteredTeachers,
      createSubject,
      showErrorModal,
      errorMessage
    }
  }
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-backdrop.inner {
  background: rgba(0, 0, 0, 0.25);
  z-index: 101;
}

.add-modal {
  background: white;
  padding: 30px 40px;
  border-radius: 12px;
  width: 520px;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 0 0 14px rgba(0, 0, 0, 0.25);
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 22px;
  color: #333;
  text-align: center;
}

.search-input {
  width: 100%;
  margin-bottom: 15px;
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.teacher-scroll-wrapper {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.teacher-item {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: background 0.2s ease;
}

.teacher-item:hover {
  background-color: #eef3ff;
}

.submit-btn,
.close-btn {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.submit-btn {
  background-color: #6995d0;
  color: white;
}
.submit-btn:hover {
  background-color: #527cbf;
}

.close-btn {
  background-color: #ccc;
}
.close-btn:hover {
  background-color: #bbb;
}

.error-modal {
  background: white;
  padding: 25px 30px;
  border-radius: 10px;
  text-align: center;
  min-width: 280px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.error-modal h2 {
  margin-bottom: 10px;
  font-size: 20px;
}

.error-modal p {
  font-size: 14px;
  margin-bottom: 15px;
}
</style>
