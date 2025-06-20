<template>
  <div class="modal-backdrop">
    <div class="modal-window">
      <h2>Создание группы</h2>

      <input
        v-model="groupName"
        type="text"
        placeholder="Введите название группы"
        class="input-field"
      />

      <button class="submit-btn" @click="createGroup">Создать</button>
      <button class="close-btn" @click="$emit('close')">Отмена</button>
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
import { defineComponent, ref } from 'vue'
import { api } from 'boot/axios'
import type { AxiosError } from 'axios'
const FEFUIcon = new URL('../assets/icons/fefu.png', import.meta.url).href

export default defineComponent({
  name: 'CreateGroupModal',
  emits: ['close', 'group-created'],
  setup(_, { emit }) {
    const groupName = ref('')
    const showErrorModal = ref(false)
    const errorMessage = ref('')

    const createGroup = async () => {
      const name = groupName.value.trim()

      if (!name) {
        errorMessage.value = 'Название группы не может быть пустым'
        showErrorModal.value = true
        return
      }

      try {
        await api.post('/api/groups/', { name })
        emit('group-created')
        emit('close')
      } catch (err: unknown) {
        const e = err as AxiosError<Record<string, unknown>>
        const data = e.response?.data

        if (typeof data?.detail === 'string') {
          errorMessage.value = data.detail
        } else if (data && typeof data === 'object') {
          const messages: string[] = []
          for (const [, fieldErrors] of Object.entries(data)) {
            if (Array.isArray(fieldErrors)) {
              fieldErrors.forEach(error => {
                if (typeof error === 'string') messages.push(error)
              })
            } else if (typeof fieldErrors === 'string') {
              messages.push(fieldErrors)
            }
          }
          errorMessage.value = messages.join(' ')
        } else {
          errorMessage.value = 'Ошибка при создании группы'
        }

        showErrorModal.value = true
      }
    }

    return {
      groupName,
      showErrorModal,
      errorMessage,
      createGroup,
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

.modal-window {
  background: white;
  padding: 30px 40px;
  border-radius: 12px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 0 14px rgba(0, 0, 0, 0.25);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 22px;
  color: #333;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
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
