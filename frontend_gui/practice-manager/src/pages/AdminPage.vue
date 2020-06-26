<template>
  <div id="app">
    <NavBar/>
    <PracticesTable/>
  </div>
</template>

<script>
import PracticesTable from '../components/PracticesTable.vue'
import NavBar from '../components/NavBar.vue'

export default {
  name: 'AdminPage',
  components: {
    NavBar,
    PracticesTable
  }
}
</script>

<style>
@import 'https://cdn.materialdesignicons.com/5.3.45/css/materialdesignicons.min.css';
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}

</style>
