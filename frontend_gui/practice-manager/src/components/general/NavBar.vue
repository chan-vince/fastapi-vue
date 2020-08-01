<template>
  <div id='navBar'>
    <b-navbar spaced shadow>
      <template slot="brand">
        <b-navbar-item style="padding-right: 40px">
          <!-- <img src="../../public/logo.png" alt="GP Data Access System" /> -->
          <a href="https://prel.im/"><img src="../../../public/nhs-logo.png" alt="GP Data Access System" /></a>
        </b-navbar-item>
      </template>
      <template slot="start">
        <b-navbar-item href="/practices" v-show="isAdmin">Practices</b-navbar-item>
        <b-navbar-item href="/employees" v-show="isAdmin">Employees</b-navbar-item>
        <b-navbar-item v-show="isAdmin" href="/approvals">
          Approvals
          <template v-if="(pending_count > 0)">({{pending_count}})</template>
        </b-navbar-item>
      </template>

      <template slot="end">
        <b-navbar-dropdown label="Switch View" hoverable>
          <router-link to="/login">
            <b-navbar-item>Login Page</b-navbar-item>
          </router-link>
          <router-link to="/practices">
            <b-navbar-item>Admin Practices View</b-navbar-item>
          </router-link>
          <router-link to="/employees">
            <b-navbar-item>Admin Employees View</b-navbar-item>
          </router-link>
          <!-- <router-link to="/practice">
            <b-navbar-item>GP User View</b-navbar-item>
          </router-link> -->
        </b-navbar-dropdown>
        <!-- <b-navbar-item tag="div">
                    <div class="buttons">
                        <a class="button is-light">
                            Report Issue
                        </a>
                    </div>
        </b-navbar-item>-->
      </template>
    </b-navbar>
  </div>
</template>

<script>
import { getPendingChangesCount } from "../../api.js";

export default {
  name: "NavBar",
  computed: {
    isAdmin() {
      if (this.$route.path == "/login" || this.$route.path == "/practice") {
        return false;
      } else {
        return true;
      }
    }
  },
  data() {
    return {
      pending_count: 0
    };
  },
  methods: {
    async getPendingApprovalsCount() {
      this.pending_count = await getPendingChangesCount();
    }
  },
  async created() {
    this.pending_count = await getPendingChangesCount();
    console.log("Pending changes count:", this.pending_count);
  },
};
</script>

<style scoped>
#navBar {
    padding-bottom: 25px;
}
</style>