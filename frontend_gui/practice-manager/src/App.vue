<template>
  <div id="app">
    <NavBar/>
    <h1 class="subsection">GP Practices</h1>
    <Table/>
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  </div>
</template>

<script>
import Table from './components/Table.vue'
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld,
    NavBar,
    Table
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
h1.subsection {
  font-weight: bold;
  font-size: 30pt;
  text-align: left;
  padding-top: 30px;
  padding-bottom: 10px;
  padding-left: 30px;
}
</style>
