<template>
  <aside class="group-panel">
    <div class="group-container">
      <button
        v-for="group in groups"
        :key="group.id"
        class="group-card"
        @click="openGroup(group)"
      >
        <img :src="SubjectIcon" alt="Group Icon" class="group-icon" />
        <p class="group-name">{{ group.name }}</p>
      </button>

      <button
        class="add-button"
        @click="createGroup"
        @mouseover="hoverAdd"
        @mouseleave="unhoverAdd"
      >
        <img :src="currentAddIcon" alt="Добавить группу" />
      </button>
    </div>
  </aside>
</template>

<script>
import SubjectIcon from '../assets/icons/programs.png';
import AddIcon from '../assets/icons/add_blue.png';
import AddIcon2 from '../assets/icons/add_red.png';
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

export default {
  name: 'GroupList',
  setup() {
    const groups = ref([])
    const currentAddIcon = ref(AddIcon)

    const fetchGroups = async () => {
      try {
        const response = await api.get('/api/groups/')
        groups.value = response.data
      } catch (error) {
        console.error('Ошибка при загрузке групп:', error)
      }
    }

    const createGroup = async () => {
      const name = prompt('Введите название новой группы:')
      if (!name) return
      try {
        await api.post('/api/groups/', { name })
        fetchGroups()
      } catch (err) {
        alert('Ошибка при создании группы')
      }
    }

    const openGroup = (group) => {
      alert(`Открыта группа: ${group.name}`)
    }

    const hoverAdd = () => {
      currentAddIcon.value = AddIcon2
    }

    const unhoverAdd = () => {
      currentAddIcon.value = AddIcon
    }

    onMounted(fetchGroups)

    return {
      groups,
      currentAddIcon,
      hoverAdd,
      unhoverAdd,
      createGroup,
      openGroup,
      SubjectIcon
    }
  }
}
</script>

<style scoped>
.group-panel {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  font-family: 'Arial', sans-serif;
  padding: 20px;
  height: 100vh;
  overflow-y: auto;
}

.group-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-start;
}

.group-card {
  width: 300px;
  height: 150px;
  background: rgba(0, 103, 177, 0.05);
  border-radius: 10px;
  border: 2px solid #6995D0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.group-card:hover {
  transform: scale(1.03);
  box-shadow: 0 15px 20px rgba(0, 0, 0, 0.15);
}

.group-icon {
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
}

.group-name {
  font-size: 18px;
  color: #6995D0;
  text-align: center;
  word-break: break-word;
}

.add-button {
  height: 40px;
  background: #ffffff;
  border-radius: 5px;
  padding: 5px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border: 2px solid #6995D0;
  transition: all 0.3s ease;
}

.add-button:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
}

.add-button img {
  width: 26px;
  height: 26px;
}
</style>
