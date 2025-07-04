<template>
  <div class="grades-table-container">
    <table class="grades-table">
      <thead>
        <tr>
          <th>№</th>
          <th>Студент</th>
          <th v-for="assignment in assignments" :key="assignment">
            {{ assignment }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(student, index) in filteredStudents" :key="student.student">
          <td>{{ index + 1 }}</td>
          <td>{{ student.full_name }}</td>
          <td
            v-for="assignment in assignments"
            :key="`${student.student}-${assignment}`"
            class="editable-grade"
            :contenteditable="isEditing"
            @blur="onGradeChange(student.student, assignment, $event)"
          >
            {{ student[assignment] || '' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ref, computed } from 'vue';

interface StudentGrade {
  student: number;
  full_name: string;
  [assignment: string]: string | number;
}

export default defineComponent({
  name: 'GradesTable',
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
    },
    searchQuery: {
      type: String,
      default: ''
    }
  },
  emits: ['update-grade'],

  setup(props) {
    const localGrades = ref<StudentGrade[]>([]);

    watch(() => props.grades, (newGrades) => {
      localGrades.value = JSON.parse(JSON.stringify(newGrades));
    }, { immediate: true });

    const filteredStudents = computed(() => {
      if (!props.searchQuery) return localGrades.value;

      const query = props.searchQuery.toLowerCase();

      return localGrades.value.filter(student =>
        student.full_name.toLowerCase().includes(query)
      );
    });

    return {
      localGrades,
      filteredStudents
    };
  },

  methods: {
    onGradeChange(studentId: number, assignment: string, event: Event) {
      if (!this.isEditing) return;
      const value = (event.target as HTMLElement).innerText.trim();

      const student = this.localGrades.find(s => s.student === studentId);
      if (student) {
        student[assignment] = value;
      }

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
.grades-table-container {
    overflow-x: auto;
    margin-bottom: 15px;
  }

  .grades-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 15px;
  }

  .grades-table th {
    background: #6995D0;
    color: white;
    padding: 12px 15px;
    text-align: center;
    font-weight: bold;
    position: relative;
  }

  .grades-table td {
    padding: 12px 15px;
    text-align: center;
    border-bottom: 1px solid #e0e0e0;
  }

  .grades-table tr:nth-child(even) {
    background-color: rgba(105, 149, 208, 0.05);
  }

  .grades-table tr:hover {
    background-color: rgba(105, 149, 208, 0.1);
  }

  .editable-grade {
    background-color: #fff8e1;
    border: 1px dashed #ffc107;
    border-radius: 4px;
  }

  .editable-grade:focus {
    outline: 2px solid #ffc107;
    background-color: #fff;
  }

  .editable-grade[contenteditable="false"] {
    background-color: transparent;
    color: #333333;
    border: 1px solid #dddddd;
    cursor: not-allowed;
  }
</style>
