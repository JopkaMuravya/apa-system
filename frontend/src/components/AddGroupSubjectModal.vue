<template>
  <div class="modal-backdrop">
    <div class="add-modal">
      <h2>Добавить предмет</h2>

      <input
        v-model="subjectSearch"
        type="text"
        placeholder="Поиск предмета..."
        class="search-input"
      />

      <div class="subject-scroll-wrapper">
        <div
          v-for="subject in filteredSubjects"
          :key="subject.id"
          class="subject-item"
          :class="{ selected: selectedSubjectId === subject.id }"
          @click="selectSubject(subject)"
        >
          {{ subject.name }}
        </div>
      </div>

      <div v-if="selectedSubject">
        <input
          v-model="teacherSearch"
          type="text"
          placeholder="Поиск преподавателя..."
          class="search-input"
        />

        <div class="teacher-scroll-wrapper">
          <div
            v-for="teacher in filteredTeachers"
            :key="teacher.id"
            class="teacher-item"
            :class="{ selected: selectedTeacherId === teacher.id }"
            @click="selectTeacher(teacher.id)"
          >
            {{ teacher.full_name }}
          </div>
        </div>
      </div>

      <button class="submit-btn" @click="assignSubject">Сохранить</button>
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

interface Subject {
  id: number
  name: string
  teachers: Teacher[]
}

export default defineComponent({
  name: 'AddGroupSubjectModal',
  props: {
    groupId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'subject-added'],
  setup(props, { emit }) {
    const subjectSearch = ref('')
    const teacherSearch = ref('')
    const subjects = ref<Subject[]>([])
    const selectedSubjectId = ref<number | null>(null)
    const selectedTeacherId = ref<number | null>(null)

    const showErrorModal = ref(false)
    const errorMessage = ref('')

    const fetchSubjects = async () => {
      try {
        const res = await api.get<Subject[]>('/api/subjects/')
        subjects.value = res.data
      } catch {
        errorMessage.value = 'Ошибка при загрузке предметов'
        showErrorModal.value = true
      }
    }

    const filteredSubjects = computed(() =>
      subjects.value.filter((s) =>
        s.name.toLowerCase().includes(subjectSearch.value.toLowerCase())
      )
    )

    const selectedSubject = computed(() =>
      subjects.value.find((s) => s.id === selectedSubjectId.value) || null
    )

    const filteredTeachers = computed(() =>
      selectedSubject.value
        ? selectedSubject.value.teachers.filter((t) =>
            t.full_name.toLowerCase().includes(teacherSearch.value.toLowerCase())
          )
        : []
    )

    const selectSubject = (subject: Subject) => {
      selectedSubjectId.value = subject.id
      selectedTeacherId.value = null
      teacherSearch.value = ''
    }

    const selectTeacher = (teacherId: number) => {
      selectedTeacherId.value = teacherId
    }

    const assignSubject = async () => {
      if (!selectedSubjectId.value || !selectedTeacherId.value) {
        errorMessage.value = 'Выберите предмет и преподавателя'
        showErrorModal.value = true
        return
      }

      try {
        await api.post(`/api/groups/${props.groupId}/subject_teachers/`, {
          subject_id: selectedSubjectId.value,
          teacher_id: selectedTeacherId.value
        })
        emit('subject-added')
        emit('close')
      } catch (err: unknown) {
        const e = err as AxiosError<{ detail?: string }>
        errorMessage.value = e.response?.data?.detail || 'Не удалось добавить предмет'
        showErrorModal.value = true
      }
    }

    onMounted(fetchSubjects)

    return {
      subjectSearch,
      teacherSearch,
      subjects,
      selectedSubjectId,
      selectedTeacherId,
      showErrorModal,
      errorMessage,
      filteredSubjects,
      filteredTeachers,
      selectedSubject,
      selectSubject,
      selectTeacher,
      assignSubject
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

.subject-scroll-wrapper,
.teacher-scroll-wrapper {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.subject-item,
.teacher-item {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: background 0.2s ease;
}

.subject-item:hover,
.teacher-item:hover {
  background-color: #eef3ff;
}

.selected {
  background-color: #c9e2ff;
  border-color: #6995d0;
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
