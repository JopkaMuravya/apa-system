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

            </div>
          </div>

          <GradesTable 
            :assignments="assignments"
            :grades="grades"
            :is-editing="false"
          />

          <!-- Убрана кнопка добавления колонки -->
          <!-- <div class="add-column-container">
            <button class="add-column-button" @click="isAddingAssignment = true">
              <i class="fa-solid fa-plus"></i>
              Добавить колонку
            </button>
          </div> -->

          <div class="teacher-comment">
            <h3 class="section-title">Комментарии преподавателя:</h3>
            <textarea 
              v-model="teacherComment"
              class="comment-textarea" 
              placeholder="Введите комментарии для студентов..."
              readonly
            ></textarea>
          </div>

          <div class="link-section">
            <h3 class="section-title">Ссылка для связи:</h3>
            <div class="link-container">
              <i class="fa-solid fa-link link-icon"></i>
              <input 
                v-model="communicationLink"
                type="text" 
                class="link-input" 
                placeholder="Вставьте ссылку на чат"
                readonly
              >
              <button class="go-button" @click="openLink">Перейти</button>
            </div>
          </div>

          <div class="teacher-section">
            <div class="teacher">
              <span>Преподаватель: </span>
              <span class="teacher-name">{{ teacherName }}</span>
            </div>

          <div class="editing-buttons">
          </div>
        </div>
        </div>
      </div>
    </div>
    
    
    <div v-if="isAddingAssignment" class="modal-backdrop">
      <div class="modal">
        <h3>Добавить новое задание</h3>
        <input 
          v-model="newAssignmentName"
          type="text" 
          placeholder="Название задания"
          class="modal-input"
        >
        <div class="modal-buttons">
          <button @click="isAddingAssignment = false">Отмена</button>
          <button @click="confirmAddAssignment">Добавить</button>
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
import { api } from '../boot/axios';

interface StudentGrade {
  student: number;
  full_name: string;
  [assignment: string]: string | number;
}

export default defineComponent({
  name: 'GradesPage',
  components: {
    SideBar,
    TopBar,
    GradesTable,
  },
      data() {
        return {
          groupId: null as number | null,
          groupName: '',
          subjectId: null as number | null,
          subjectName: '',
          assignments: [] as string[],
          grades: [] as StudentGrade[],
          teacherName: '',
          teacherComment: '',
          communicationLink: '',
          isEditing: false,
          isAddingAssignment: false,
          newAssignmentName: '',
          pendingUpdates: {} as Record<string, Record<string, string>>,
          userRole: '',
        };
      },
    async created() {
      await this.fetchTeacherName();
      await this.fetchUserRole();

      this.groupId = parseInt(this.$route.query.groupId as string);
      this.groupName = this.$route.query.groupName as string;
      this.subjectId = parseInt(this.$route.query.subjectId as string);
      this.subjectName = this.$route.query.subjectName as string;
      
      await this.loadGrades();
    },
  methods: {
    async fetchTeacherName() {
      try {
        const response = await api.get('/api/current-user/');
        this.teacherName = response.data.full_name;
      } catch (error) {
        console.error('Ошибка загрузки данных преподавателя:', error);
        this.teacherName = 'Неизвестный преподаватель';
      }
    },
    async fetchUserRole() {
      try {
        const response = await api.get('/api/current-user/');
        this.userRole = response.data.role;
      } catch (error) {
        console.error('Ошибка загрузки роли пользователя:', error);
        this.userRole = '';
      }
    },
    async loadGrades() {
      try {
        const endpoint = this.userRole === 'student'
          ? `/api/student/grades/${this.groupId}/${this.subjectId}/`
          : `/api/grades/${this.groupId}/${this.subjectId}/`;
        const response = await api.get(endpoint);
        this.assignments = response.data.assignments;
        this.grades = response.data.grades;
        this.teacherComment = response.data.comment || '';
        this.communicationLink = response.data.link || '';
        if (this.userRole === 'student' && response.data.teacher_name) {
          this.teacherName = response.data.teacher_name;
        }
      } catch (error) {
        console.error('Ошибка загрузки оценок:', error);
      }
    },
    
    addAssignment() {
      this.isAddingAssignment = true;
    },
    
    confirmAddAssignment() {
      if (this.newAssignmentName.trim()) {
        this.assignments.push(this.newAssignmentName.trim());
        this.isAddingAssignment = false;
        this.newAssignmentName = '';
      }
    },
    
    openLink() {
      if (this.communicationLink) {
        window.open(this.communicationLink, '_blank');
      }
    }
  },
});
</script>

<style>
@import "../css/grades.scss";
</style>