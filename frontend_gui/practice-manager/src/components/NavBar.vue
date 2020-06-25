<template>
    <b-navbar>
        <template slot="brand">
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                <img
                    src="../../public/logo.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
        <template slot="start">
            <b-navbar-item v-show="isAdmin" href="#">
                Access Systems
            </b-navbar-item>
            <b-navbar-item v-show="isAdmin" href="#">
                Pending Approvals
            </b-navbar-item>
            <b-navbar-dropdown v-show="isAdmin" label="Practices">
                <b-navbar-item href="#">
                    Add New Practice
                </b-navbar-item>
                <b-navbar-item href="#">
                    Edit Practice Details
                </b-navbar-item>
            </b-navbar-dropdown>
            <b-navbar-dropdown v-show="isAdmin" label="Employees">
                <b-navbar-item href="#">
                    Add New Employee
                </b-navbar-item>
                <b-navbar-item href="#">
                    Edit Employee Details
                </b-navbar-item>
            </b-navbar-dropdown>
        </template>

        <template slot="end">
            <b-navbar-dropdown label="Switch View">
                <router-link to='/login'><b-navbar-item>Login</b-navbar-item></router-link>
                <router-link to='/admin'><b-navbar-item>Admin</b-navbar-item></router-link>
                <router-link to='/practice'><b-navbar-item>GP Practice</b-navbar-item></router-link>
            </b-navbar-dropdown>
            <!-- <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-light">
                        Report Issue
                    </a>
                </div>
            </b-navbar-item> -->
        </template>
    </b-navbar>
</template>

<script>
export default {
    name: 'NavBar',
    computed: {
      isAdmin() {
        if(this.$route.path == "/admin") {
          return true
        } else {
          return false
        }
      }
    } 
//   props: {
//     msg: String
//   }
}
</script>