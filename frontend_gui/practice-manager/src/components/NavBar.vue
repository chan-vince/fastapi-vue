<template>
    <div style="padding-left: 20px">
        <b-navbar spaced shadow>
            <template slot="brand">
                <b-navbar-item tag="router-link" :to="{ path: '/admin' }" style="padding-right: 40px">
                    <img
                        src="../../public/logo.png"
                        alt="GP Data Access System"
                    >
                </b-navbar-item>
            </template>
            <template slot="start">
                <b-navbar-dropdown v-show="isAdmin" label="Practices" hoverable>
                    <b-navbar-item href="#">
                        Add New Practice
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Edit Practice Details
                    </b-navbar-item>
                </b-navbar-dropdown>
                <b-navbar-dropdown v-show="isAdmin" label="Employees" hoverable>
                    <b-navbar-item href="#">
                        Add New Employee
                    </b-navbar-item>
                    <b-navbar-item href="#">
                        Edit Employee Details
                    </b-navbar-item>
                </b-navbar-dropdown>
                <b-navbar-item v-show="isAdmin" href="/approvals">
                    Pending Approvals
                </b-navbar-item>
            </template>

            <template slot="end">
                <b-navbar-dropdown label="Switch View" hoverable>
                    <router-link to='/login'><b-navbar-item>Login Page</b-navbar-item></router-link>
                    <router-link to='/admin'><b-navbar-item>Admin View</b-navbar-item></router-link>
                    <router-link to='/practice'><b-navbar-item>GP User View</b-navbar-item></router-link>
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
    </div>
</template>

<script>
export default {
    name: 'NavBar',
    computed: {
      isAdmin() {
        if( (this.$route.path == "/login" || this.$route.path == "/practice")) {
          return false
        } else {
          return true
        }
      }
    } 
//   props: {
//     msg: String
//   }
}
</script>