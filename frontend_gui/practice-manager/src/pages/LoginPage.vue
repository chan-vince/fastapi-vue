<template>
  <div id="login">
      <NavBar/>
    <h1>Login Page</h1>
  </div>
</template>

<script>

import NavBar from '../components/NavBar'

export default {
  name: 'LoginPage',
  components: {
    NavBar
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
