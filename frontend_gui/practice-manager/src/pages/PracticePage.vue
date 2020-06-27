<template>
  <div id="login">
      <NavBar/>
    <PracticeForm v-bind:practice_name="practice_name" />
  </div>
</template>

<script>

import NavBar from '../components/NavBar'
import PracticeForm from '../components/PracticeForm'

export default {
  name: 'PracticePage',
  components: {
    NavBar,
    PracticeForm
  },
  data (){
    return {
      practice_name: this.$route.params.name
    }
  },
  created () {  
    }
}
</script>

<style>
#login {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
