<template>
  <div class="no-role">
    <div class="error-modal">
      <div class="error-modal-blue">
        <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
        <h2>Добро пожаловать!</h2>
        <img class="fefu-icon" :src="FEFUIcon" alt="Fefu" />
      </div>
      <div class="error-modal-text">
        <p>Ваша роль ещё не назначена.</p>
        <p>Пожалуйста, обратитесь к модератору.</p>
        <div class="modal-actions">
          <button @click="login">Выйти</button>
        </div>
      </div>
    </div>
  </div>
  </template>
  
<script lang="ts">
  import { defineComponent } from 'vue'
  import FEFUIcon from '../assets/icons/fefu.png'

  export default defineComponent({
    name: 'NoRolePage',
    setup() {
      const login = () => {
        window.location.href = '/login'
      }

      return {
        FEFUIcon,
        login,
      }
    }
  })
</script>

  <style scoped>
    .no-role {
      background: url('../assets/images/auth_banner.jpeg');
      background-repeat: no-repeat;
      background-size: 100vw 100vh;
      background-attachment: fixed;
      margin: auto;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.2);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      font-family: 'Arial', sans-serif;
    }

    .no-role::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(85, 104, 118, 0.7);
      z-index: 1;
    }


    .error-modal {
      display: flex;
      flex-direction: column;
      position: relative;
      z-index: 2;
      background: white;
      padding: 0;
      border-radius: 10px;
      text-align: center;
      min-width: 500px;
      min-height: 310px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }

    .error-modal-blue {
      background: #6995D0;
      border-radius: 10px 10px 0 0;
      min-width: 100px;
      min-height: 20%;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 30px;
      padding: 8px 0px;
    }

    .error-modal-text {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 25px 30px;
      border-radius: 0 0 10px 10px;
      text-align: center;
    }

    .error-modal-blue img {
      width: auto;
      height: 45px;
      margin-bottom: 10px;
    }

    .error-modal h2 {
      margin: 0 0 10px;
      font-size: 26px;
      color: white;
    }

    .error-modal p {
      margin: 0 0 15px;
      font-size: 20px;
      color: #333;
    }

    .modal-actions {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-top: auto;
    }

      .modal-actions button {
        background-color: #6995d0;
        color: white;
        padding: 10px 18px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
      }

        .modal-actions button:hover {
          background-color: #527cbf;
        }
  </style>
