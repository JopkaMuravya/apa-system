<template>
  <div class="main-page">
    <SideBar />
    <div class="content">
      <TopBar />
      <div class="grades-panel-wrapper">
        <div class="grades-container">
          <div class="grades-header">
            <h2 class="grades-title">Оценки</h2>
            <div class="subject-info">
              <span class="subject-name">Комплексный анализ</span>
              <span class="group-number">Группа: Б9123-01.03.02сп</span>
            </div>
          </div>

          <GradesTable />

          <div class="add-column-container">
            <button class="add-column-button">
              <i class="fa-solid fa-plus"></i>
              Добавить колонку
            </button>
          </div>

          <div class="teacher-comment">
            <h3 class="section-title">Комментарии преподавателя:</h3>
            <textarea class="comment-textarea" placeholder="Введите комментарии для студентов..."></textarea>
          </div>

          <div class="link-section">
            <h3 class="section-title">Ссылка для связи:</h3>
            <div class="link-container">
              <i class="fa-solid fa-link link-icon"></i>
              <input type="text" class="link-input" placeholder="Вставьте ссылку на чат">
              <button class="go-button">Перейти</button>
            </div>
          </div>

          <div class="teacher-section">
            <div class="teacher">
              <span>Преподаватель: </span>
              <span class="teacher-name">Клевчихин Юрий Александрович</span>
            </div>

            <div class="editing-buttons">
              <button class="edit-button" disabled>
                <i class="fa-solid fa-pen"></i>
                Редактировать
              </button>
              <button class="save-button">
                <i class="fa-solid fa-bookmark"></i>
                Сохранить ведомость
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import SideBar from '../components/SideBar.vue';
  import TopBar from '../components/TopBar.vue';
  import GradesTable from '../components/GradesTable.vue';

  export default defineComponent({
    name: 'GradesPage',
    components: {
      SideBar,
      TopBar,
      GradesTable,
    },
    data() {
      return {
        searchQuery: '',
        currentPageTitle: 'Оценки'
      };
    },
    provide() {
      return {
        updatePageTitle: (title: string) => {
          this.currentPageTitle = title;
        },
        currentPageTitle: this.currentPageTitle
      };
    }
  });
</script>

<style>
@import "../css/grades.scss";
</style>
