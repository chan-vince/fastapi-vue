<template>
  <div class="card">
    <div class="card-header-title" style="margin: 30px 75px 0px 10px">
      <p class="title is-3">
        General
      </p>
    </div>
    <div class="card-content">
      <section style="padding-right: 50px">
        <b-field label="Name" horizontal>
          <b-input v-model="name" size="is-default" required
                   placeholder="Enter a GP Practice Name"></b-input>
        </b-field>
        <b-field label="National Code" horizontal>
          <b-input v-model="national_code" size="is-default" required
                   placeholder="Enter a National Code"></b-input>
        </b-field>
        <b-field label="EMIS CDB Practice Code" horizontal>
          <b-input v-model="emis_cdb_practice_code" size="is-default" required
                   placeholder="Enter a National Code"></b-input>
        </b-field>
        <b-field label="Go Live Date" horizontal>
          <b-datepicker v-model="go_live_date"
                        :first-day-of-week="1"
                        placeholder="Click to select...">
            <button class="button is-primary"
                    @click="go_live_date = new Date()">
              <b-icon icon="calendar-today"></b-icon>
              <span>Today</span>
            </button>

            <button class="button is-danger"
                    @click="go_live_date = null">
              <b-icon icon="close"></b-icon>
              <span>Clear</span>
            </button>
          </b-datepicker>
        </b-field>
        <br>
        <div class="field level-left" horizontal>
          <b-checkbox v-model="closed"
                      type="is-primary">
            Practice closed
          </b-checkbox>
        </div>
        <div class="level" style="padding-top: 20px">
          <b-field class="level-left">
            <b-checkbox-button v-model="checkboxGroup" v-for="system in access_systems" :key="system.id"
                               :native-value="system.name"
                               type="is-success"
                               v-on:input="printSelected">
              <span>{{ system.name }}</span>
            </b-checkbox-button>
          </b-field>

          <div class="level-right">
            <b-button v-on:click="saveDetails" type="is-primary" outlined icon-left="content-save">Save
            </b-button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import {getAccessSystemsAll, postChangeRequest} from '../api.js'
import isEqual from 'lodash.isequal';


export default {
  name: 'GPDetailsGeneralForm',
  props: ['practice_details'],
  data() {
    const today = new Date()
    return {
      go_live_date: today,
      minDate: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
      name: '',
      national_code: '',
      emis_cdb_practice_code: '',
      closed: false,
      access_systems: [],
      checkboxGroup: [],
      checkboxGroupInit: [],
      originalPracticeDetails: null
    }
  },
  watch: {
    practice_details: function (details) {
      this.id = details['id']
      this.name = details['name']
      this.national_code = details['national_code']
      this.emis_cdb_practice_code = details['emis_cdb_practice_code']
      this.go_live_date = new Date(details['go_live_date'])
      this.closed = details['closed']
      this.checkboxGroup = details['access_systems'].map((item) => item["name"])
      this.checkboxGroupInit = details['access_systems'].map((item) => item["name"])
      this.originalPracticeDetails = {
        name: this.name,
        national_code: this.national_code,
        emis_cdb_practice_code: this.emis_cdb_practice_code,
        go_live_date: this.go_live_date.toISOString().split('T')[0],
        closed: this.closed
      }
    }
  },
  methods: {
    printSelected() {
      console.log(this.checkboxGroup)
    },


    async saveDetails() {

      // Build the objects for the new state of the data fields
      let new_state_general = {
        "name": this.name,
        "national_code": this.national_code,
        "emis_cdb_practice_code": this.emis_cdb_practice_code,
        "go_live_date": this.go_live_date.toISOString().split('T')[0],
        "closed": this.closed,
      }
      let new_state_access_system = {
        link: "access_system",
        action: "replace",
        data: this.access_systems
            .filter(i => this.checkboxGroup.includes(i.name))
            // .map(i => ({"id": this.id, "name": i.name})),
      }

      // Check for the case where the save button is pressed when no changes have been made
      if ((isEqual(this.originalPracticeDetails, new_state_general)) && (isEqual(this.checkboxGroup, this.checkboxGroupInit))) {
        this.$buefy.toast.open({
          message: "No changes made",
          type: "is-default"
        });
        return
      }

      // Create the wrapper info in preparation for the API requests
      let body = {
        requestor_id: 1,
        target_name: "practice",
        target_id: this.id,
      }

      try {
        // Send API request for the general section
        if (!(isEqual(this.originalPracticeDetails, new_state_general))) {
          let response = await postChangeRequest({...body, new_state: new_state_general});
          console.log(response.data);
        }

        console.log({...body, new_state: new_state_access_system})
        // Send API request for the Access system box thing
        if (!(isEqual(this.checkboxGroup, this.checkboxGroupInit))) {
          let response = await postChangeRequest({...body, new_state: new_state_access_system});
          console.log(response.data);
        }

        // Should we not encounter any errors after both requests, we can celebrate
        this.$buefy.toast.open({
          message: "Request submitted successfully",
          type: "is-success"
        });
        this.$emit("newRequestGenerated");

        // Crude uh-oh..the second can fail and the first succeed and the user won't know
      } catch
          (error) {
        this.$buefy.toast.open({
          message: "Request error",
          type: "is-danger"
        });
      }

    }
  },
  async created() {
    this.access_systems = await getAccessSystemsAll()
  }
}
</script>

<style scoped>
.title {
  font-weight: lighter;
}
</style>