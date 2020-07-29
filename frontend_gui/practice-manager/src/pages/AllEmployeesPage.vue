<template>
  <div id="app">
    <NavBar />
    <section id="content">
      <div class="container">
        <TitleWithSearchBar
          pageTitle="All Employees"
          minSearchLength="0"
          @newSearchInput="updateTable"
        />

        <nav class="level">
          <!-- Left side -->
          <div class="level-left">
            <div class="level-item">
              <b-select v-model="perPage" v-on:input="perPageModified">
                <option value="5">5 per page</option>
                <option value="10">10 per page</option>
                <option value="15">15 per page</option>
                <option value="20">20 per page</option>
              </b-select>
            </div>
          </div>

          <!-- Right side -->
          <div class="level-right">
            <p class="level-item">
              <a class="button is-primary" @click="addEmployeeModal">Add New Employee</a>
            </p>
          </div>
        </nav>

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
            <b-table-column field="id" label="ID" sortable>{{ props.row.id }}</b-table-column>
            <b-table-column field="name" label="Name" sortable>{{ props.row.name }}</b-table-column>
            <b-table-column
              field="job_title"
              label="Job Title"
              sortable
            >{{ props.row.job_title.title }}</b-table-column>
            <b-table-column field="email" label="Email" sortable>{{ props.row.email }}</b-table-column>
            <b-table-column
              field="professional_num"
              label="Professional ID"
              sortable
            >{{ props.row.professional_num }}</b-table-column>
            <b-table-column
              field="it_portal_num"
              label="IT Portal ID"
              sortable
            >{{ props.row.it_portal_num }}</b-table-column>
            <b-table-column
              field="desktop_num"
              label="Desktop ID"
              sortable
            >{{ props.row.desktop_num }}</b-table-column>
            <b-table-column field="active" label="Active" sortable>
              <template v-if="props.row.active == true">
                <b-icon icon="check"></b-icon>
              </template>
              <template v-else>
                <b-icon icon="close"></b-icon>
              </template>
            </b-table-column>
          </template>
        </b-table>
      </div>
    </section>
  </div>
</template>

<script>
import {getEmployeeCount, getEmployeeAll, getEmployeeNames, getEmployeeByName} from "@/api";
import NavBar from "../components/general/NavBar.vue";
import TitleWithSearchBar from "../components/general/TitleWithSearchBar";
import moment from "moment";
import ModalEmployee from "../components/modals/AddEmployeeModal.vue";

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
      isPaginationSimple: true,
      paginationPosition: "bottom",
      defaultSortDirection: "asc",
      sortIcon: "chevron-up",
      sortIconSize: "is-small",
      perPage: 10,
      currentPage: 1,
      searchInput: "",
      selected: null
    };
  },
  methods: {
    addEmployeeModal() {
      var rowObject = null;
      var action = "Add";

      this.$buefy.modal.open({
        parent: this,
        component: ModalEmployee,
        hasModalCard: true,
        trapFocus: true,
        props: {
          rowObject: rowObject,
          jobTitles: this.job_titles,
          action: action
        }
      });
    },
    onDoubleClick(rowObject) {
      console.log(rowObject);
      this.$buefy.modal.open({
        parent: this,
        component: ModalEmployee,
        hasModalCard: true,
        trapFocus: true,
        props: {
          rowObject: rowObject,
          jobTitles: this.job_titles,
          action: "Edit"
        }
      });
    },
    displayDate(datestring) {
      return moment(datestring).format("Do MMM YYYY");
    },
    async onPageChange(page) {
      let skip = page * this.perPage - this.perPage;
      let limit = this.perPage;
      this.currentPage = page;
      if (this.searchInput.length === 0) {
        this.employees = await getEmployeeAll(skip, limit);
      }
    },
    perPageModified() {
      this.onPageChange(this.currentPage);
    },
    async filterEmployees() {
      if (this.searchInput.length > 1) {
        this.loading = true;
        let names = this.employee_names.filter(name =>
          name.toLowerCase().includes(this.searchInput.toLowerCase())
        );
        let employee_details = [];
        let promises = [];
        for (const name of names) {
          promises.push(
            getEmployeeByName(name)
              .then(response => {
                employee_details.push(response);
              })
          );
        }
        Promise.all(promises).then(() => {
          // Need to check the length again once the promise returns as its likely that the search input is deleted before the return
          if (this.searchInput.length !== 0) {
            this.total = employee_details.length;
          }
          this.employees = employee_details;
          this.currentPage = 1;
          this.loading = false;
        });
      } else {
        this.employees = await getEmployeeAll(0, this.perPage);
        this.total = await getEmployeeCount();
      }
    },
    updateTable(searchInput) {
      this.searchInput = searchInput;
      this.filterEmployees();
    }
  },
  async created() {
    this.loading = true;
    this.total = await getEmployeeCount();
    this.employees = await getEmployeeAll(0, 15);
    this.employee_names = await getEmployeeNames();
    this.loading = false;
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
  margin: 0px 5px 0px 5px;
}
</style>
