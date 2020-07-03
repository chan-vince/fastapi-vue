<template>
  <div id="app">
    <NavBar />
    <div class="container" id="content">
      <TitleWithSearchBar
        pageTitle="All Employees"
        minSearchLength="0"
        @newSearchInput="updateTable"
      />
      <b-field grouped group-multiline>
        <b-select v-model="perPage" v-on:input="perPageModified">
          <option value="5">5 per page</option>
          <option value="10">10 per page</option>
          <option value="15">15 per page</option>
          <option value="20">20 per page</option>
        </b-select>
        <!-- <button class="button field is-danger" @click="selected = null"
                    :disabled="!selected">
                    <b-icon icon="close"></b-icon>
                    <span>Clear selected</span>
        </button>-->
      </b-field>

      <b-table
        :data="employees"
        :selected.sync="selected"
        default-sort="name"
        :default-sort-direction="defaultSortDirection"
        :loading="loading"
        :total="total"
        backend-pagination
        paginated
        :per-page="perPage"
        @page-change="onPageChange"
        :current-page.sync="currentPage"
        :sort-icon="sortIcon"
        :sort-icon-size="sortIconSize"
        aria-next-label="Next page"
        aria-previous-label="Previous page"
        aria-page-label="Page"
        aria-current-label="Current page"
        @dblclick="onDoubleClick"
      >
        <template slot-scope="props">
          <b-table-column
            field="name"
            label="Name"
            sortable
          >{{ props.row.name }}</b-table-column>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import { client } from "../api.js";
import NavBar from "../components/NavBar.vue";
import TitleWithSearchBar from "../components/TitleWithSearchBar";
import moment from "moment";

export default {
  name: "AllEmployeesPage",
  components: {
    NavBar,
    TitleWithSearchBar
  },
  data() {
    return {
      employees: [],
      total: 0,
      employee_names: [],
      loading: false,
      isPaginated: true,
      isPaginationSimple: false,
      paginationPosition: "bottom",
      defaultSortDirection: "asc",
      sortIcon: "chevron-up",
      sortIconSize: "is-small",
      perPage: 15,
      currentPage: 1,
      searchInput: "",
      selected: null
    };
  },
  methods: {
    onDoubleClick(rowObject) {
      this.$router.push({ path: `/employee/${rowObject["name"]}` });
    },
    displayDate(datestring) {
      return moment(datestring).format("Do MMM YYYY");
    },
    getEmployees(skip, limit) {
      client
        .get(`api/v1/employees/`, { params: { skip: skip, limit: limit } })
        .then(response => {
          this.employees = response.data;
          this.loading = false;
        });
    },
    onPageChange(page) {
      let skip = page * this.perPage - this.perPage;
      let limit = this.perPage;
      this.currentPage = page;
      if (this.searchInput.length == 0) {
        this.getEmployees(skip, limit);
      }
    },
    perPageModified() {
      this.onPageChange(this.currentPage);
    },
    filterEmployees() {
      if (this.searchInput.length > 1) {
        this.loading = true;
        var names = this.employee_names.filter(name =>
          name.toLowerCase().includes(this.searchInput.toLowerCase())
        );
        var employee_details = [];
        var promises = [];
        console.log(names)
        for (const name of names) {
          promises.push(
            client
              .get(`api/v1/employee/name`, { params: { name: name } })
              .then(response => {
                employee_details.push(response.data);
              })
          );
        }
        Promise.all(promises).then(() => {
          // Need to check the length again once the promise returns as its likely that the search input is deleted before the return
          if (this.searchInput.length != 0) {
            this.total = employee_details.length;
          }
          this.employees = employee_details;
          this.currentPage = 1;
          this.loading = false;
        });
      } else {
        this.getEmployees(0, this.perPage);
        this.getTotalEmployees();
      }
    },
    getTotalEmployees() {
      client.get(`api/v1/employees/count`).then(response => {
        this.total = response.data.count;
      });
    },
    getAllEmployeeNames() {
      client.get(`api/v1/employees/names`).then(response => {
        this.employee_names = response.data.names;
      });
    },
    updateTable(searchInput) {
      console.log(searchInput);
      this.searchInput = searchInput;
      this.filterEmployees();
    }
  },
  created() {
    this.loading = true;
    this.getTotalEmployees();
    this.getAllEmployeeNames();
    this.getEmployees(0, 15);
  }
};
</script>

<style>
@import "https://cdn.materialdesignicons.com/5.3.45/css/materialdesignicons.min.css";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
#content {
  max-width: 1920px;
  padding: 0px 10px 0px 10px;
}
</style>
