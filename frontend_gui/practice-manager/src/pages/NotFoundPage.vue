<template>
  <section>
    <NavBar />
    <h1>Sorry, we couldn't find what you were looking for!</h1>
  </section>
</template>

<script>
import NavBar from "../components/general/NavBar";

export default {
  name: "NotFoundPage",
  components: {
    NavBar
  }
};
</script>

<style scoped>
h1 {
  margin-top: 100px;
  font-size: 20pt;
}
</style>
