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
        @click="showCreateModal = true"
        @mouseover="hoverAdd"
        @mouseleave="unhoverAdd"
      >
        <img :src="currentAddIcon" alt="Добавить группу" />
      </button>
    </div>

    <CreateGroupModal
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @group-created="handleGroupCreated"
    />
  </aside>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

import SubjectIcon from '../assets/icons/programs.png'
import AddIcon from '../assets/icons/add_blue.png'
import AddIcon2 from '../assets/icons/add_red.png'
import CreateGroupModal from './CreateGroupModal.vue'

interface Group {
  id: number
  name: string
}

export default defineComponent({
  name: 'GroupList',
  components: { CreateGroupModal },
  setup() {
    const router = useRouter()
    const groups = ref<Group[]>([])
    const currentAddIcon = ref(AddIcon)
    const showCreateModal = ref(false)

    const fetchGroups = async () => {
      try {
        const response = await api.get('/api/groups/')
        groups.value = response.data
      } catch (error) {
        console.error('Ошибка при загрузке групп:', error)
      }
    }

    const openGroup = (group: Group) => {
      router.push({
        name: 'group-detail',
        params: {
          id: group.id,
          name: encodeURIComponent(group.name)
        }
      })
    }

    const handleGroupCreated = () => {
      fetchGroups()
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
      openGroup,
      showCreateModal,
      handleGroupCreated,
      SubjectIcon
    }
  }
})
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
