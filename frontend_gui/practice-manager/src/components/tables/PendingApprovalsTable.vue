<template>
  <section>
    <b-table
        ref="table"
        paginated
        per-page="20"
        :loading="loading"
        :data="staging_records"
        :show-detail-icon="showDetailIcon"
        :opened-detailed="defaultOpenedDetails"
        :detailed="true"
        @details-open="getSupportInfo"
        detail-key="id"
        aria-next-label="Next page"
        aria-previous-label="Previous page"
        aria-page-label="Page"
        aria-current-label="Current page"
    >
      <template slot-scope="props">
        <b-table-column field="id" label="Request Type" sortable>
          <template v-if="props.row.target_id == null">Add New&nbsp;</template>
          <template v-else>Modify&nbsp;</template>
          <template>{{ target_names[props.row.target_name] }}</template>
        </b-table-column>

        <b-table-column field="last_modified" label="Request Date" sortable>
          <span class>{{ new Date(props.row.created_at).toLocaleString() }}</span>
        </b-table-column>

        <b-table-column field="requestor.name" label="Requested By" sortable>
          <template v-if="pendingOnly"></template>
          {{ props.row.requestor.name }}
        </b-table-column>

        <template v-if="!(pendingOnly)">
          <b-table-column field="approver.name" label="Approved At" sortable>
            <span class>{{ new Date(props.row.last_modified).toLocaleString() }}</span>
          </b-table-column>
        </template>

        <template v-if="!(pendingOnly)">
          <b-table-column field="approver.name" label="Approved By" sortable>
            {{ props.row.approver.name }}
          </b-table-column>
        </template>

        <b-table-column field="approved" label="Status" sortable>
          <template v-if="props.row.approval_status === true">
            <b-tag type="is-success" rounded>Approved</b-tag>
          </template>
          <template v-else-if="props.row.approval_status === false">
            <b-tag type="is-danger" rounded>Rejected</b-tag>
          </template>
          <template v-else>
            <b-tag rounded>Pending</b-tag>
          </template>
        </b-table-column>
      </template>

      <template slot="detail" slot-scope="props">
        <template v-if="props.row.target_name === 'practice'">
          <PendingPracticeDetail
              v-bind:row="props.row"
              v-bind:detail_delta="detail_delta"/>
        </template>
        <template v-if="props.row.target_name === 'practice.access_systems'">
          <PendingAccessSystemDetail
              v-bind:row="props.row"
              v-bind:detail_delta="detail_delta"/>
        </template>
        <template v-if="props.row.target_name === 'employee'">
          <PendingEmployeeDetail
              v-bind:row="props.row"
              v-bind:detail_delta="detail_delta"/>
        </template>

        <template v-if="props.row.target_name === 'ip_ranges'">
          <PendingIPRangeDetail
              v-bind:row="props.row"
              v-bind:aux_info="aux_info"
              v-bind:detail_delta="detail_delta"/>
        </template>


        <!-- <template v-if="props.row.target_id == null">
          {{ props.row.payload }}
          {{ aux_info }}
        </template>
        <template v-else>
          <div v-for="item in detail_delta" :key="item.key">{{item}}</div>
        </template>-->

        <!-- <template v-if="props.row.source_id == null">
          <div v-for="item in diff_data" :key="item.name">
            <div class="level-left">
              {{  }}
              <div class="level-item">
                <strong>{{ item.label }}:</strong>
              </div>
              <div class="level-item">{{props.row[item.field]}}</div>
            </div>
          </div>
        </template>-->

        <!-- <template v-else>
          <div class="title is-5">Changes:</div>
          <div v-for="item in staging_records" :key="item.name">
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
        </template>-->
        <template v-if="pendingOnly">
          <hr/>
          <div class="buttons">
            <b-button
                type="is-success"
                outlined
                icon-left="check"
                v-on:click="acceptChanges(props.row['id'])"
            >Accept
            </b-button>
            <b-button
                type="is-danger"
                outlined
                icon-left="close"
                v-on:click="rejectChanges(props.row['id'])"
            >Reject
            </b-button>
          </div>
        </template>
      </template>

      <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p>
              <b-icon
                  icon="emoticon-happy"
                  size="is-large">
              </b-icon>
            </p>
            <p>No pending approvals!</p>
          </div>
        </section>
      </template>
    </b-table>
  </section>
</template>


<script>
import {
  approveChangeRequest,
  getDeltaPendingChangeById,
  getPendingChangesAll,
  getHistoricChangesAll, rejectChangeRequest
} from "@/api";
import PendingIPRangeDetail from "../approval_details/PendingIPRangeDetail.vue";
import PendingPracticeDetail from "../approval_details/PendingPracticeDetail";
import PendingAccessSystemDetail from "../approval_details/PendingAccessSystemDetail";
import PendingEmployeeDetail from "../approval_details/PendingEmployeeDetail";

export default {
  name: "PendingApprovalsTable",
  props: ["pendingOnly"],
  components: {
    PendingEmployeeDetail,
    PendingIPRangeDetail,
    PendingPracticeDetail,
    PendingAccessSystemDetail
  },
  data() {
    return {
      staging_records: [],
      detail_delta: {},
      defaultOpenedDetails: [],
      showDetailIcon: true,
      loading: true,
      target_names: {
        ip_range: "CIDR IP Range",
        practice: "Practice",
        employee: "Employee",
        'practice.access_systems': "System Access"
      },
      aux_info: null,
      details_close: null
    };
  },
  methods: {
    async getSupportInfo(row) {
      this.detail_delta = await getDeltaPendingChangeById(row.id);
      this.defaultOpenedDetails = [row.id];
    },
    async refreshRows() {
      if (this.$props.pendingOnly === true) {
        this.staging_records = await getPendingChangesAll(0, 100)
        // this.staging_records = this.staging_records.filter(item => item.approval_status == null);
      } else {
        this.staging_records = await getHistoricChangesAll(0, 100)
        console.log(`pending: ${this.$props.pendingOnly}`)
        console.log(this.staging_records)
        // this.staging_records = this.staging_records.filter(item => item.approval_status != null);
      }
    },
    async acceptChanges(id) {
      console.log(`Accepting changes for row id ${id}`);
      try {
        // One day the approver_id will be the logged in admin user
        let approver_id = 1
        await approveChangeRequest(id, approver_id)
        this.$buefy.toast.open({
          message: "Accepted change successfully",
          type: "is-success"
        });
        this.$emit("refresh");
      } catch (error) {
        console.log(error);
        this.$buefy.toast.open({
          message: "Could not accept change",
          type: "is-danger"
        });
      }
    },
    async rejectChanges(id) {
      console.log(`Rejecting changes for row id ${id}`);
      try {
        // One day the approver_id will be the logged in admin user
        let approver_id = 1
        await rejectChangeRequest(id, approver_id)
        this.$buefy.toast.open({
          message: "No change made to original record",
          type: "is-success"
        });
        this.$emit("refresh");
      } catch (error) {
        console.log(error);
        this.$buefy.toast.open({
          message: "Could not reject change request",
          type: "is-danger"
        });
      }
    },
    goToPractice(rowObject) {
      this.$router.push({path: `/practice/${rowObject["name"]}`});
    }
  },
  async created() {
    this.loading = true;
    await this.refreshRows();
    this.loading = false;
  }
};
</script>


<style scoped>
</style>