<template>
  <div class="modal-backdrop">
    <div class="add-modal">
      <h2>Добавить в группу {{ currentGroupName }}</h2>

      <input
        v-model="search"
        type="text"
        placeholder="Поиск по ФИО..."
        class="search-input"
      />

      <div class="student-scroll-wrapper">
        <div
          v-for="student in filteredStudents"
          :key="student.id"
          :class="['student-item', { 'has-group': student.group_name && student.group_name !== currentGroupName }]"
          @click="handleStudentClick(student)"
        >
          <div class="name">{{ student.full_name }}</div>
          <div class="group-info">
            {{ student.group_name || 'Группы нет' }}
          </div>
        </div>
      </div>

      <button class="close-btn" @click="$emit('close')">Закрыть</button>
    </div>

    <div v-if="showConfirmModal" class="modal-backdrop inner">
      <div class="error-modal">
        <h2>Подтверждение</h2>
        <p>
          Переместить студента из группы
          "{{ selectedStudent?.group_name }}" в "{{ currentGroupName }}"?
        </p>
        <div class="confirm-actions">
          <button @click="confirmAssign">Да</button>
          <button @click="cancelAssign">Нет</button>
        </div>
      </div>
    </div>

    <div v-if="showError" class="modal-backdrop inner">
      <div class="error-modal">
        <h2>Ошибка</h2>
        <p>{{ errorMessage }}</p>
        <button @click="showError = false">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, PropType } from 'vue'
import { api } from 'boot/axios'

interface Student {
  id: number
  full_name: string
  group_name?: string
}

interface RawUser {
  id: number
  first_name: string
  last_name: string
  middle_name?: string
  role: string
  group_name?: string
}

export default defineComponent({
  name: 'AddStudentModal',
  props: {
    groupId: {
      type: [String, Number] as PropType<string | number>,
      required: true
    }
  },
  emits: ['close', 'student-added'],
  setup(props, { emit }) {
    const search = ref('')
    const students = ref<Student[]>([])
    const currentGroupName = ref('')
    const showConfirmModal = ref(false)
    const showError = ref(false)
    const errorMessage = ref('')
    const selectedStudent = ref<Student | null>(null)

    const filteredStudents = computed(() =>
      students.value.filter(s =>
        s.full_name.toLowerCase().includes(search.value.toLowerCase())
      )
    )

    const fetchAllStudents = async () => {
      try {
        const [usersRes, groupRes] = await Promise.all([
          api.get('/api/users/'),
          api.get(`/api/groups/${props.groupId}/`)
        ])

        currentGroupName.value = groupRes.data.name

        students.value = (usersRes.data as RawUser[])
          .filter(user => user.role === 'student')
          .map(user => ({
            id: user.id,
            full_name: `${user.last_name} ${user.first_name} ${user.middle_name || ''}`.trim(),
            group_name: user.group_name
          }))
      } catch {
        showError.value = true
        errorMessage.value = 'Не удалось загрузить студентов'
      }
    }

    const handleStudentClick = (student: Student) => {
      if (student.group_name === currentGroupName.value) {
        showError.value = true
        errorMessage.value = 'Студент уже в этой группе'
      } else if (student.group_name) {
        selectedStudent.value = student
        showConfirmModal.value = true
      } else {
        assignStudent(student)
      }
    }

    const assignStudent = async (student: Student) => {
      try {
        await api.post(`/api/groups/${props.groupId}/`, {
          student_id: student.id
        })
        emit('student-added')
        emit('close')
      } catch {
        showError.value = true
        errorMessage.value = 'Не удалось назначить студента'
      }
    }

    const confirmAssign = () => {
      if (selectedStudent.value) {
        assignStudent(selectedStudent.value)
        showConfirmModal.value = false
        selectedStudent.value = null
      }
    }

    const cancelAssign = () => {
      selectedStudent.value = null
      showConfirmModal.value = false
    }

    onMounted(fetchAllStudents)

    return {
      search,
      students,
      filteredStudents,
      handleStudentClick,
      currentGroupName,
      showConfirmModal,
      confirmAssign,
      cancelAssign,
      showError,
      errorMessage,
      selectedStudent
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

.student-scroll-wrapper {
  max-height: 350px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
  padding-right: 4px;
}

.student-item {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s ease;
  background-color: #f9f9f9;
}

.student-item:hover {
  background-color: #eef3ff;
}

.student-item.has-group {
  background-color: #fff3cd;
}

.name {
  font-weight: 500;
  color: #333;
}

.group-info {
  font-size: 13px;
  color: #777;
}

.close-btn {
  background-color: #6995d0;
  color: white;
  padding: 10px;
  font-size: 14px;
  width: 100%;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #527cbf;
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

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
