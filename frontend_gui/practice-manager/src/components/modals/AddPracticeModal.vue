<template>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{action}} GP Practice</p>
    </header>
    <section class="modal-card-body">
      <b-field label="Name" horizontal>
        <b-input :value="this.name" v-model="name" placeholder="Name" required></b-input>
      </b-field>

      <b-field label="National Code" horizontal>
        <b-input :value="this.national_code" v-model="national_code" placeholder="National Code" required></b-input>
      </b-field>

      <b-field label="EMIS CDB Practice Code" horizontal>
        <b-input
          :value="this.emis_cdb_practice_code"
          v-model="emis_cdb_practice_code"
          placeholder="EMIS CDB Practice Code"
          required
        ></b-input>
      </b-field>

      <b-field label="Go Live Date" horizontal>
        <b-datepicker
          v-model="go_live_date"
          :first-day-of-week="1"
          placeholder="Click to select..."
          position="is-top-right"
          :append-to-body="true"
        >
          <button class="button is-primary" @click="go_live_date = new Date()">
            <b-icon icon="calendar-today"></b-icon>
            <span>Today</span>
          </button>

          <button class="button is-danger" @click="go_live_date = null">
            <b-icon icon="close"></b-icon>
            <span>Clear</span>
          </button>
        </b-datepicker>
      </b-field>
      <hr />
      <b-checkbox v-model="closed" type="is-primary">Practice closed</b-checkbox>
    </section>
    <footer class="modal-card-foot">
      <button class="button" type="button" @click="$parent.close()">Cancel</button>
      <button class="button is-primary" @click="addNewPractice">Submit</button>
    </footer>
  </div>
</template>


<script>
import { client } from "../../api.js";

export default {
  name: "ModalPractice",
  props: ["jobTitles", "action"],
  components: {},
  data() {
    return {
      isComponentModalActive: false,
      name: this.name,
      national_code: null,
      emis_cdb_practice_code: null,
      go_live_date: null,
      closed: false
    };
  },
  created() {
    // console.log(this.$props.jobTitles)
    // console.log(this.$props.rowObject)
  },
  methods: {
    addNewPractice() {
      var current = this;

      var payload = {
        name: this.name,
        national_code: this.national_code,
        emis_cdb_practice_code: this.emis_cdb_practice_code,
        go_live_date: this.go_live_date.toISOString().split('T')[0],
        closed: this.closed
      };
      var body = {
        requestor_id: 5000,
        target_table: "practices",
        target_id: null,
        modify: false,
        payload: payload
      }

      console.log(payload)
      client
        .post(`api/v1/stagingbeta`, body)
        .then(response => {
          console.log(response.data);
          this.$parent.close()
          this.$buefy.toast.open({
            message: "Request submitted successfully",
            type: "is-success"
          });
        })
        .catch(function(error) {
          console.log(error);
          current.$buefy.toast.open({
            message: "Request error",
            type: "is-danger"
          });
        });
    }
  }
};
</script>

<style scoped>
.modal .animation-content .modal-card {
  overflow: visible !important;
}

.modal-card-body {
  overflow: visible !important;
}
</style>