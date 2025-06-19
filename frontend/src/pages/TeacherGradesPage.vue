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

          <GradesTable :assignments="assignments"
                       :grades="grades"
                       :is-editing="isEditing"
                       @update-grade="handleGradeUpdate"
                       @add-assignment="addAssignment" />

          <div class="add-column-container">
            <button
              class="add-column-button"
              @click="isAddingAssignment = true"
              :disabled="!isEditing"
            >
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
              :disabled="!isEditing"
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
                :disabled="!isEditing"
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
                :class="{ 'cancel-button': isEditing }"
                @click="toggleEditing"
              >
                <i class="fa-solid" :class="isEditing ? 'fa-xmark' : 'fa-pen'"></i>
                {{ isEditing ? 'Отменить' : 'Редактировать' }}
              </button>
              <button 
                class="save-button"
                :disabled="!hasChanges || !isEditing"
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
    <AddNewExampleModal v-if="isAddingAssignment"
                        @close="isAddingAssignment = false"
                        @confirm="handleAssignmentConfirm" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import SideBar from '../components/SideBar.vue';
import TopBar from '../components/TopBar.vue';
import GradesTable from '../components/GradesTable.vue';
import AddNewExampleModal from '../components/AddNewExampleModal.vue';
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
    AddNewExampleModal
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
      backupGrades: [] as StudentGrade[],
      backupAssignments: [] as string[],
      backupComment: '',
      backupLink: ''
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
      this.backupGrades = JSON.parse(JSON.stringify(this.grades));
      this.backupAssignments = [...this.assignments];
      this.backupComment = this.teacherComment;
      this.backupLink = this.communicationLink;
      this.isEditing = true;
    },

    cancelEditing() {
      this.grades = JSON.parse(JSON.stringify(this.backupGrades));
      this.assignments = [...this.backupAssignments];
      this.teacherComment = this.backupComment;
      this.communicationLink = this.backupLink;
      this.isEditing = false;
      this.pendingUpdates = {};
    },

    toggleEditing() {
      if (this.isEditing) {
        this.cancelEditing();
      } else {
        this.startEditing();
      }
    },
    
    handleAssignmentConfirm(name: string) {
      this.assignments.push(name);
    },
    
    handleGradeUpdate({ studentId, assignment, value }: { studentId: number; assignment: string; value: string }) {
      if (!this.pendingUpdates[assignment]) {
        this.pendingUpdates[assignment] = {};
      }
      this.pendingUpdates[assignment][studentId] = value;
    },
    
    async saveGrades() {
      if (!this.hasChanges) return;

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
      if (!this.isEditing) return;
      
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

  computed: {
    hasChanges() {
      const gradesChanged = JSON.stringify(this.grades) !== JSON.stringify(this.backupGrades);
      const assignmentsChanged = JSON.stringify(this.assignments) !== JSON.stringify(this.backupAssignments);
      const commentChanged = this.teacherComment !== this.backupComment;
      const linkChanged = this.communicationLink !== this.backupLink;
      const hasPendingUpdates = Object.keys(this.pendingUpdates).length > 0;
      return gradesChanged || assignmentsChanged || commentChanged || linkChanged || hasPendingUpdates;
    }
  }
});
</script>

<style>
@import "../css/grades.scss";
</style>
