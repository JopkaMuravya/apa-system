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
              <span class="group-number">Группа: {{ groupName }}</span>
            </div>
          </div>

          <GradesTable 
            :assignments="assignments"
            :grades="grades"
            :is-editing="isEditing"
            @update-grade="handleGradeUpdate"
            @add-assignment="addAssignment"
          />

          <div class="add-column-container">
            <button class="add-column-button" @click="isAddingAssignment = true">
              <i class="fa-solid fa-plus"></i>
              Добавить колонку
            </button>
          </div>

          <div class="teacher-comment">
            <h3 class="section-title">Комментарии преподавателя:</h3>
            <textarea 
              v-model="teacherComment"
              class="comment-textarea" 
              placeholder="Введите комментарии для студентов..."
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
              <button 
                class="edit-button" 
                :disabled="isEditing"
                @click="startEditing"
              >
                <i class="fa-solid fa-pen"></i>
                Редактировать
              </button>
              <button 
                class="save-button"
                @click="saveGrades"
              >
                <i class="fa-solid fa-bookmark"></i>
                Сохранить ведомость
              </button>
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
    };
  },
  async created() {
    await this.fetchTeacherName();
    
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
    async loadGrades() {
      try {
        const response = await api.get(`/api/grades/${this.groupId}/${this.subjectId}/`);
        this.assignments = response.data.assignments;
        this.grades = response.data.grades;
        this.teacherComment = response.data.comment || '';
        this.communicationLink = response.data.link || '';
      } catch (error) {
        console.error('Ошибка загрузки оценок:', error);
      }
    },
    
    startEditing() {
      this.isEditing = true;
    },
    
    handleGradeUpdate({ studentId, assignment, value }: { studentId: number; assignment: string; value: string }) {
      if (!this.pendingUpdates[assignment]) {
        this.pendingUpdates[assignment] = {};
      }
      this.pendingUpdates[assignment][studentId] = value;
    },
    
    async saveGrades() {
      try {
        for (const [assignment, grades] of Object.entries(this.pendingUpdates)) {
          await api.post(`/api/grades/${this.groupId}/${this.subjectId}/`, {
            assignment_name: assignment,
            grades
          });
        }
        
        await api.put(`/api/grades/${this.groupId}/${this.subjectId}/`, {
          comment: this.teacherComment,
          link: this.communicationLink
        });
        
        this.isEditing = false;
        this.pendingUpdates = {};
        await this.loadGrades();
      } catch (error) {
        console.error('Ошибка сохранения:', error);
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