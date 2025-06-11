<template>
  <div class="group-detail">
      <table class="students-table">
        <thead>
          <tr>
            <th>№</th>
            <th>Название работы</th>
            <th>Оценка</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(assignment, index) in assignments" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ assignment }}</td>
            <td>{{ grades[0][assignment] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

interface StudentGrade {
  student: number;
  full_name: string;
  [assignment: string]: string | number;
}

export default defineComponent({
  name: 'GradesList',
  props: {
    assignments: {
      type: Array as () => string[],
      required: true
    },
    grades: {
      type: Array as () => StudentGrade[],
      required: true
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update-grade'],
  methods: {
    onGradeChange(studentId: number, assignment: string, event: Event) {
      const value = (event.target as HTMLElement).innerText.trim();
      this.$emit('update-grade', {
        studentId,
        assignment,
        value
      });
    }
  }
});

</script>

<style scoped>
.group-detail h3 {
  margin-bottom: 15px;
}

.error {
  color: red;
  margin-top: 10px;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  margin-bottom: 15px;
}

.students-table th {
  background: #6995D0;
  color: white;
  padding: 12px 15px;
  text-align: center;
  font-weight: bold;
  position: relative;
  border: none;
}

.students-table td {
  padding: 12px 15px;
  text-align: left;
  border: 1px solid #e0e0e0;
  text-align: center;
}

.students-table tr {
  border: 1px solid #e0e0e0;
}

.students-table tr:hover {
  background-color: rgba(105, 149, 208, 0.1);
}

th.action-header,
td.action-buttons {
  width: 90px;
  text-align: center;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.delete-button,
.edit-button,
.save-button,
.cancel-button {
  border: none;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  padding: 4px;
  cursor: pointer;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-button,
.save-button {
  background-color: #5cb85c;
}
.edit-button:hover,
.save-button:hover {
  background-color: #4cae4c;
}
.cancel-button,
.delete-button {
  background-color: #d9534f;
}
.cancel-button:hover,
.delete-button:hover {
  background-color: #c9302c;
}

img {
  width: 16px;
  height: 16px;
}

input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

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
}

.error-modal {
  background: white;
  padding: 25px 30px;
  border-radius: 10px;
  text-align: center;
  min-width: 280px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.error-modal h2 {
  margin: 0 0 10px;
  font-size: 24px;
}

.error-modal p {
  margin: 0 0 15px;
  font-size: 14px;
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

.add-student-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #6995d0;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  float: right;
}

.add-student-button:hover {
  background-color: #527cbf;
}

</style>
