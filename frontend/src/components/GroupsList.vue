<template>
  <aside class="group-panel">
    <div class="group-container">
      <button
        v-for="group in filteredGroups"
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
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { api } from 'boot/axios'

const SubjectIcon = new URL('../assets/icons/programs.png', import.meta.url).href
const AddIcon = new URL('../assets/icons/add_blue.png', import.meta.url).href
const AddIcon2 = new URL('../assets/icons/add_red.png', import.meta.url).href
import CreateGroupModal from './CreateGroupModal.vue'

interface Group {
  id: number
  name: string
}

export default defineComponent({
  name: 'GroupList',
  props: {
    searchQuery: {
      type: String,
      default: ''
    }
  },
  components: { CreateGroupModal },
  setup(props) {
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

    const filteredGroups = computed(() => {
      let filtered = groups.value

      if (props.searchQuery) {
        const query = props.searchQuery.toLowerCase()
        filtered = filtered.filter(group => group.name.toLowerCase().includes(query))
      }

      return filtered
    })

    onMounted(fetchGroups)

    return {
      groups,
      currentAddIcon,
      hoverAdd,
      unhoverAdd,
      openGroup,
      showCreateModal,
      handleGroupCreated,
      SubjectIcon,
      filteredGroups
    }
  }
})
</script>

<style scoped>
.group-panel {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: #ffffff;
  font-family: 'Arial', sans-serif;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}

.group-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-start;
  align-content: flex-start;
  margin-left: 80px;
  width: calc(100% - 80px);
  height: 100%;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
  scrollbar-width: auto;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.group-container::-webkit-scrollbar {
  width: 8px;
}

.group-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.group-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.group-card {
  background: rgba(0, 103, 177, 0.1);
  border-radius: 10px;
  width: 300px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px;
  text-align: center;
  border: 2px solid #6995D0;
  transition: all 0.3s ease;
  box-shadow: 0 20px 20px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  transform: scale(1);
  cursor: pointer;
}

.group-card:hover {
  transform: scale(1.03);
  box-shadow: 0 25px 25px rgba(0, 0, 0, 0.15);
}

.group-icon {
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
}

.group-name {
  color: #6995D0;
  font-size: 18px;
  margin: 5px 20px;
  text-decoration: underline;
  word-break: break-word;
}

.add-button {
  height: 40px;
  background: #ffffff;
  border-radius: 5px;
  padding: 5px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  justify-content: center;
  text-align: center;
  margin: 40px 5px;
  border: 2px solid #6995D0;
  transform: scale(1);
  transition: all 0.3s ease;
}

.add-button:hover {
  transform: scale(1.03);
  box-shadow: 0 25px 25px rgba(0, 0, 0, 0.15);
}

.add-button img {
  width: 26px;
  height: 26px;
}
</style>
