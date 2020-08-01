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

<style lang="scss">
@import 'https://cdn.materialdesignicons.com/5.3.45/css/materialdesignicons.min.css';
@font-face {
  font-family: Frutiger;
  src: url("./assets/fonts/Frutiger.ttf") format('truetype');
}
#app {
  // font-family: Avenir, Helvetica, Arial, sans-serif;
  font-family: Frutiger,serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
h1.subsection {
  font-weight: bold;
  font-size: 30pt;
  text-align: left;
  padding-top: 30px;
  padding-bottom: 10px;
  padding-left: 30px;
}
// Import Bulma's core
@import "~bulma/sass/utilities/_all";

// Set your colors
$primary: #005eb8;
$primary-invert: findColorInvert($primary);

// Setup $colors to use as bulma classes (e.g. 'is-twitter')
$colors: (
    "white": ($white, $black),
    "black": ($black, $white),
    "light": ($light, $light-invert),
    "dark": ($dark, $dark-invert),
    "primary": ($primary, $primary-invert),
    "info": ($info, $info-invert),
    "success": ($success, $success-invert),
    "warning": ($warning, $warning-invert),
    "danger": ($danger, $danger-invert)
);

$navbar-item-img-max-height: 40px;
$navbar-padding-vertical: 0.6rem;

// Links
$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

// Import Bulma and Buefy styles
@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
