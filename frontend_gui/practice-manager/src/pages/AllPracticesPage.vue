<template>
  <div id="app">
    <NavBar />
    <section id="content">
      <div class="container">
        <TitleWithSearchBar
          pageTitle="All Practices"
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
              <a class="button is-primary" @click="addPracticeModal">Add New Practice</a>
            </p>
          </div>
        </nav>

        <b-table
          :data="data"
          :loading="loading"
          :total="total"
          backend-pagination
          paginated
          :per-page="perPage"
          @page-change="onPageChange"
          :current-page.sync="currentPage"
          :default-sort-direction="defaultSortDirection"
          :sort-icon="sortIcon"
          :sort-icon-size="sortIconSize"
          aria-next-label="Next page"
          aria-previous-label="Previous page"
          aria-page-label="Page"
          aria-current-label="Current page"
          :selected.sync="selected"
          @dblclick="onDoubleClick"
        >
          <template slot-scope="props">
            <template v-for="column in columns">
              <b-table-column :key="column.id" v-bind="column">
                <template
                  v-if="!('list_target' in column) && !column.date && !(column.parent)"
                >{{ props.row[column.field] }}</template>
                <template v-else-if="column.date">{{ displayDate(props.row[column.field]) }}</template>
                <template v-else-if="column.list_target && column.parent">
                  <template
                    v-if="props.row[column.parent].length"
                  >{{ props.row[column.parent][0][column.field].map(a => a[column.list_target]).join(", ") }}</template>
                </template>
                <template
                  v-else-if="!(column.list_target) && column.parent"
                >{{ props.row[column.parent].map(a => a[column.field]).join(", ") }}</template>
                <template v-else>
                  <template
                    v-if="props.row[column.field].length"
                  >{{ props.row[column.field].map(a => a[column.list_target]).join(", ") }}</template>
                </template>
              </b-table-column>
            </template>
          </template>
        </b-table>
      </div>
    </section>
  </div>
</template>

<script>
import { client } from "../api.js";
import NavBar from "../components/NavBar.vue";
import TitleWithSearchBar from "../components/TitleWithSearchBar";
import moment from "moment";
import ModalPractice from "../components/ModalPractice.vue";

export default {
  name: "AllPracticesPage",
  components: {
    NavBar,
    TitleWithSearchBar
  },
  data() {
    return {
      data: [],
      columns: [
        { field: "id", label: "ID", width: "100", numeric: true },
        { field: "created_date", label: "Date Created", date: true },
        { field: "name", label: "Practice Name" },
        { field: "national_code", label: "National Code" },
        { field: "emis_cdb_practice_code", label: "EMIS CDB Practice Code" },
        {
          field: "access_systems",
          label: "Access System(s)",
          list_target: "name"
        },
        {
          field: "ip_ranges",
          parent: "addresses",
          label: "IP Range(s)",
          list_target: "cidr"
        },
        { field: "phone_num", parent: "addresses", label: "Phone Number" }
      ],
      total: 0,
      practice_names: [],
      loading: false,
      isPaginated: true,
      isPaginationSimple: false,
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
    addPracticeModal() {
      this.$buefy.modal.open({
        parent: this,
        component: ModalPractice,
        hasModalCard: true,
        trapFocus: true,
        scroll: "keep",
        props: {
          jobTitles: [],
          action: "Add"
        }
      });
    },
    onDoubleClick(rowObject) {
      this.$router.push({ path: `/practice/${rowObject["name"]}` });
    },
    displayDate(datestring) {
      return moment(datestring).format("Do MMM YYYY");
    },
    getPractices(skip, limit) {
      client
        .get(`api/v1/practice`, { params: { skip: skip, limit: limit } })
        .then(response => {
          this.data = response.data;
          this.loading = false;
        });
    },
    onPageChange(page) {
      let skip = page * this.perPage - this.perPage;
      let limit = this.perPage;
      this.currentPage = page;
      if (this.searchInput.length == 0) {
        this.getPractices(skip, limit);
      }
    },
    perPageModified() {
      this.onPageChange(this.currentPage);
    },
    getPractice() {
      if (this.searchInput.length > 0) {
        this.loading = true;
        var names = this.practice_names.filter(name =>
          name.toLowerCase().includes(this.searchInput.toLowerCase())
        );
        var practice_details = [];
        var promises = [];
        for (const name of names) {
          promises.push(
            client
              .get(`api/v1/practice/name`, { params: { name: name } })
              .then(response => {
                practice_details.push(response.data);
              })
          );
        }
        Promise.all(promises).then(() => {
          // Need to check the length again once the promise returns as its likely that the search input is deleted before the return
          if (this.searchInput.length != 0) {
            this.total = practice_details.length;
          }
          this.data = practice_details;
          this.currentPage = 1;
          this.loading = false;
        });
      } else {
        this.getPractices(0, this.perPage);
        this.getTotalPractices();
      }
    },
    getTotalPractices() {
      client.get(`api/v1/practice/count`).then(response => {
        this.total = response.data.count;
      });
    },
    getAllPracticeNames() {
      client.get(`api/v1/practice/names`).then(response => {
        this.practice_names = response.data.names;
      });
    },
    updateTable(searchInput) {
      console.log(searchInput);
      this.searchInput = searchInput;
      this.getPractice();
    }
  },
  created() {
    this.loading = true;
    this.getTotalPractices();
    this.getAllPracticeNames();
    this.getPractices(0, 15);
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
}
#content {
  margin: 0px 5px 0px 5px;
}
</style>
