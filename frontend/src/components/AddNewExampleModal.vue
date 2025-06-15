<template>
  <div class="modal-backdrop">
    <div class="add-modal">
      <h2>Добавить новое задание</h2>

      <input v-model="assignmentName"
             type="text"
             placeholder="Название задания"
             class="search-input">

      <div class="modal-buttons">
        <button class="cancel-btn" @click="$emit('close')">Отмена</button>
        <button class="submit-btn" @click="confirmAdd">Добавить</button>
      </div>
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
  const FEFUIcon = new URL('../assets/icons/fefu.png', import.meta.url).href

  export default defineComponent({
    name: 'AddNewExampleModal',
    emits: ['close', 'confirm'],
    setup(_, { emit }) {
      const assignmentName = ref('')
      const showErrorModal = ref(false)
      const errorMessage = ref('')

      const confirmAdd = () => {
        if (!assignmentName.value.trim()) {
          errorMessage.value = 'Название задания обязательно'
          showErrorModal.value = true
          return
        }

        emit('confirm', assignmentName.value.trim())
        emit('close')
      }

      return {
        assignmentName,
        confirmAdd,
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
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
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
    margin-bottom: 20px;
    padding: 10px 15px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 6px;
  }

  .modal-buttons {
    display: flex;
    justify-content: space-between;
    gap: 15px;
  }

  .cancel-btn,
  .submit-btn {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .cancel-btn {
    background-color: #f0f0f0;
    color: #333;
  }

    .cancel-btn:hover {
      background-color: #e0e0e0;
    }

  .submit-btn {
    background-color: #6995d0;
    color: white;
  }

    .submit-btn:hover {
      background-color: #527cbf;
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
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
  }

    .error-modal button:hover {
      background-color: #527cbf;
    }
</style>
