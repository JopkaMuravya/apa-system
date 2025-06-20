<template>
  <div class="modal-backdrop">
    <div class="add-modal">
      <h2>Редактировать предмет</h2>

      <input
        v-model="name"
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

      <button class="submit-btn" @click="updateSubject">Сохранить</button>
      <button class="close-btn" @click="$emit('close')">Закрыть</button>
    </div>

    <div v-if="showErrorModal" class="modal-backdrop inner">
      <div class="error-modal">
        <div class="error-modal-blue">
          <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
          <h2>Ошибка</h2>
          <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
        </div>
        <div class="error-modal-text">
          <p>{{ errorMessage }}</p>
          <button @click="showErrorModal = false">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, PropType } from 'vue'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'
const FEFUIcon = new URL('../assets/icons/fefu.png', import.meta.url).href

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
  name: 'EditSubjectModal',
  props: {
    subjectId: {
      type: Number,
      required: true
    },
    initialName: {
      type: String,
      required: true
    },
    initialTeachers: {
      type: Array as PropType<number[]>,
      required: true
    }
  },
  emits: ['close', 'subject-updated'],
  setup(props, { emit }) {
    const name = ref(props.initialName)
    const search = ref('')
    const teachers = ref<Teacher[]>([])
    const selectedTeacherIds = ref<number[]>([...props.initialTeachers])
    const showErrorModal = ref(false)
    const errorMessage = ref('')

    const fetchTeachers = async () => {
      try {
        const res = await api.get('/api/users/')
        teachers.value = (res.data as RawUser[])
          .filter(user => user.role === 'teacher')
          .map(user => ({
            id: user.id,
            full_name: `${user.last_name} ${user.first_name} ${user.middle_name || ''}`.trim()
          }))
      } catch {
        showErrorModal.value = true
        errorMessage.value = 'Ошибка при загрузке преподавателей'
      }
    }

    const filteredTeachers = computed(() =>
      teachers.value.filter(t =>
        t.full_name.toLowerCase().includes(search.value.toLowerCase())
      )
    )

    const updateSubject = async () => {
      if (!name.value.trim()) {
        errorMessage.value = 'Введите название предмета'
        showErrorModal.value = true
        return
      }

      try {
        await api.put(`/api/subjects/${props.subjectId}/`, {
          name: name.value.trim(),
          teacher_ids: selectedTeacherIds.value
        })
        emit('subject-updated')
        emit('close')
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        errorMessage.value = e.response?.data?.detail || 'Не удалось обновить предмет'
        showErrorModal.value = true
      }
    }

    onMounted(fetchTeachers)

    return {
      name,
      search,
      teachers,
      selectedTeacherIds,
      filteredTeachers,
      updateSubject,
      showErrorModal,
      errorMessage,
      FEFUIcon
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
    padding: 0;
    border-radius: 10px;
    text-align: center;
    min-width: 280px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }

  .error-modal-blue {
    background: #6995D0;
    border-radius: 10px 10px 0 0;
    min-width: 100px;
    min-height: 0;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 20px;
  }

  .error-modal-text {
    padding: 25px 30px;
    border-radius: 10px 10px 0 0;
    text-align: center;
    min-height: 80px;
  }

  .error-modal-blue img {
    width: auto;
    height: 35px;
    margin-bottom: 5px;
  }

  .error-modal h2 {
    margin: 0;
    font-size: 22px;
    color: white;
  }

  .error-modal p {
    margin: 0 0 15px;
    font-size: 15px;
    color: #333;
  }

  .error-modal button {
    background-color: #6995d0;
    color: white;
    padding: 6px 14px;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
  }

    .error-modal button:hover {
      background-color: #527cbf;
    }
</style>
