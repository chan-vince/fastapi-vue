<template>
  <div id="app">
    <div>
        <vue-headful
            title="GP Data Access Manager"
        />
    </div>
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
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
