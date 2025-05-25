<template>
  <div class="grades-table-container">
    <table class="grades-table">
      <thead>
        <tr>
          <th>№</th>
          <th>Студент</th>
          <th>Колонка 1</th>
          <th>Колонка 2</th>
          <th>Колонка 3</th>
          <th>Колонка 4</th>
          <th>Колонка 5</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>Иванов А.А.</td>
          <td class="editable-grade" contenteditable="false">5</td> <!--Вот так должна выглядить ячнйка с оценкой у студента и у учителя когда он ее не редактирует-->
          <td class="editable-grade" contenteditable="true">5</td> <!--Вот так должна выглядить ячнйка с оценкой у учителя когда он ее редактирует-->
          <td class="editable-grade" contenteditable="false">4</td>
          <td class="editable-grade" contenteditable="false"></td>
          <td class="editable-grade" contenteditable="false"></td>
        </tr>
        <tr>
          <td>2</td>
          <td>Петров Б.В.</td>
          <td class="editable-grade" contenteditable="false">4</td>
          <td class="editable-grade" contenteditable="false">3</td>
          <td class="editable-grade" contenteditable="false">4</td>
          <td class="editable-grade" contenteditable="false"></td>
          <td class="editable-grade" contenteditable="false"></td>
        </tr>
        <tr>
          <td>3</td>
          <td>Сидорова Г.Д.</td>
          <td class="editable-grade" contenteditable="false">5</td>
          <td class="editable-grade" contenteditable="false">5</td>
          <td class="editable-grade" contenteditable="false">5</td>
          <td class="editable-grade" contenteditable="false"></td>
          <td class="editable-grade" contenteditable="false"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'GradesTable',
})
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
