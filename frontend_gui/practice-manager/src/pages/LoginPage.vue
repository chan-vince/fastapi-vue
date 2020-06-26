<template>
    <section>
        <NavBar/>
        <h1>Login</h1>
        <section class="login-form">
            <b-field label="Email" style="text-align:left">
                <b-input value=""></b-input>
            </b-field>
            <b-field label="Password" style="text-align:left" >
                <b-input type="password" maxlength="30" password-reveal="true"></b-input>
            </b-field>
        </section>
    </section>
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

<style scoped>
.login-form {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    max-width: 500px;
    margin: 0 auto;
    margin-top: 20px;
    padding: 20px 15px 20px 15px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
}
h1 {
    margin-top: 100px;
    font-size: 20pt;
}
</style>
