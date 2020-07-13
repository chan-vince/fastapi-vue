<template>
  <section>
    <b-table
      :data="data"
      :loading="loading"
      ref="table"
      paginated
      per-page="15"
      :detailed="pendingOnly"
      detail-key="id"
      :show-detail-icon="showDetailIcon"
      aria-next-label="Next page"
      aria-previous-label="Previous page"
      aria-page-label="Page"
      aria-current-label="Current page"
    >
      <template slot-scope="props">
        <b-table-column field="id" label="Type">
          <template v-if="props.row.source_id == null">Add New Record</template>
          <template v-else>Modify Existing Record</template>
        </b-table-column>

        <b-table-column field="name" label="Name" sortable>
          <template>{{ props.row.name }}</template>
        </b-table-column>

        <b-table-column field="practice_name" label="Practice" sortable>
          <!-- <template><a @click="goToPractice(props.row.practice_name)">{{ props.row.practice_name }}</a></template> -->
          {{ props.row.practice_name }}
        </b-table-column>

        <b-table-column field="last_modified" label="Request Date" sortable centered>
          <span class>{{ new Date(props.row.last_modified).toLocaleString() }}</span>
        </b-table-column>

        <b-table-column field="requestor.name" label="Requestor" sortable>
          <template v-if="pendingOnly"></template>
          {{ props.row.requestor.name }}
        </b-table-column>

        <b-table-column field="approved" label="Status" sortable>
          <template v-if="props.row.approved == 1">
            <b-tag type="is-success" rounded>Approved</b-tag>
          </template>
          <template v-else-if="props.row.approved == 0">
            <b-tag type="is-danger" rounded>Rejected</b-tag>
          </template>
          <template v-else>
            <b-tag rounded>Pending</b-tag>
          </template>
        </b-table-column>
      </template>

      <template slot="detail" slot-scope="props">
        <template v-if="props.row.source_id == null">
          <div v-for="item in diff_data" :key="item.name">
            <div class="level-left">
              <div class="level-item">
                <strong>{{ item.label }}:</strong>
              </div>
              <div class="level-item">{{props.row[item.field]}}</div>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="title is-5">Changes:</div>
          <div v-for="item in diff_data" :key="item.name">
            <template v-if="props.row.source[item.field] != props.row[item.field]">
              <div class="columns">
                <div class="column is-2">
                  <strong>{{ item.label }}:</strong>
                </div>
                <div class="column">
                  <div class="level">
                    <div class="level-left">
                      <b-tag size="is-medium" type="is-danger">{{props.row.source[item.field]}}</b-tag>
                      <b-icon icon="arrow-right"></b-icon>
                      <b-tag size="is-medium" type="is-success">{{props.row[item.field]}}</b-tag>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </template>
        <template v-if="pendingOnly">
          <hr />
          <div class="buttons">
            <b-button
              type="is-success"
              outlined
              icon-left="check"
              v-on:click="acceptChanges(props.row['id'])"
            >Accept</b-button>
            <b-button
              type="is-danger"
              outlined
              icon-left="close"
              v-on:click="rejectChanges(props.row['id'])"
            >Reject</b-button>
          </div>
        </template>
      </template>
    </b-table>
  </section>
</template>


<script>
import { client } from "../../api.js";

export default {
  name: "PracticeApprovalsTable",
  props: ["pendingOnly"],
  data() {
    return {
      data: [],
      defaultOpenedDetails: [1],
      showDetailIcon: true,
      loading: true,
      job_titles: [],
      diff_data: [
        { field: "name", label: "Name" },
        { field: "email", label: "Email" },
        { field: "professional_num", label: "Professional ID" },
        { field: "desktop_num", label: "Desktop ID" },
        { field: "it_portal_num", label: "IT Portal ID" },
        { field: "job_title", label: "Job Title" }
      ]
    };
  },
  methods: {
    getStagingEmployees(skip, limit) {
      client
        .get(`api/v1/staging/employee`, {
          params: { skip: skip, limit: limit }
        })
        .then(response => {
          if (this.$props.pendingOnly) {
            this.data = response.data.filter(item => item.approved == null);
          } else {
            this.data = response.data.filter(item => item.approved != null);
          }
          this.data.forEach(item => {
            console.log(item["name"]);
            if (item.job_title_id !== null) {
              item["job_title"] = this.job_titles.find(
                element => element.id == item.job_title_id
              ).title;
            }
            if (item.source !== null) {
              if (item.source.job_title !== null) {
                item["source"]["job_title"] =
                  item["source"]["job_title"]["title"];
              }
            }
          });
          this.loading = false;
        });
    },
    acceptChanges(id) {
      var current = this;
      console.log(`Accepting changes for row id ${id}`);
      client
        .put(`api/v1/staging/employee/approved`, null, {
          params: { id: id, approved: true }
        })
        .then(response => {
          console.log(response.data);
          this.$buefy.toast.open({
            message: "Accepted change successfully",
            type: "is-success"
          });
          this.$emit("refresh");
        })
        .catch(function(error) {
          console.log(error);
          current.$buefy.toast.open({
            message: "Could not accept change",
            type: "is-danger"
          });
        });
    },
    rejectChanges(id) {
      var current = this;
      console.log(`Rejecting changes for row id ${id}`);
      client
        .put(`api/v1/staging/employee/approved`, null, {
          params: { id: id, approved: false }
        })
        .then(response => {
          console.log(response.data);
          this.$buefy.toast.open({
            message: "Rejected change successfully",
            type: "is-success"
          });
          this.$emit("refresh");
        })
        .catch(function(error) {
          console.log(error);
          current.$buefy.toast.open({
            message: "Could not reject change",
            type: "is-danger"
          });
        });
    },
    goToPractice(name) {
      this.$router.push({ path: `/practice/${name}` });
    },
    getJobTitles() {
      client.get(`api/v1/job_titles`).then(response => {
        this.job_titles = response.data;
      });
    }
  },
  created() {
    this.loading = true;
    this.getJobTitles();
    this.getStagingEmployees();
  }
};
</script>



<style scoped>
</style>