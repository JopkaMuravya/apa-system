<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="close">
    <div class="error-modal">
      <div class="error-modal-blue">
        <img class="fefu-icon" :src="FEFUIcon" alt="FEFU" />
        <h2>Ошибка</h2>
        <img class="fefu-icon" :src="FEFUIcon" alt="FEFU" />
      </div>
      <div class="error-modal-text">
        <p>{{ message }}</p>
        <button @click="close">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
    message: String
  },
  data() {
    return {
      FEFUIcon: new URL('../assets/icons/fefu.png', import.meta.url).href
    }
  },
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
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
  padding: 15px;
}

.error-modal-text {
  padding: 25px 30px;
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