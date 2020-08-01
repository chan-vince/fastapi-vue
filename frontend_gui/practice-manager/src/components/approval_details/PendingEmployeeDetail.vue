<template>
  <section v-if="row">
    <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>

    <div class="title is-4" v-if="row.target_id != null">
      {{ row.current_state.name }}
    </div>

    <hr>
    <div v-for="(value, key) in detail_delta" :key="key">
      <div class="columns">
        <div class="column is-2">
          <strong>{{ labels.find(x => x.key === key).label }}:</strong>
        </div>
        <div class="column">
          <div class="level-left">
            <template v-if="key === 'active'">
              <template v-if="value.before">
                <b-tag size="is-medium" type="is-danger">
                  {{ value.before == true ? "Active" : "Inactive" }}
                </b-tag>
                <b-icon icon="arrow-right"></b-icon>
              </template>
              <b-tag size="is-medium" type="is-success">
                {{ value.after == true ? "Active" : "Inactive" }}
              </b-tag>
            </template>

            <template v-else-if="key === 'practice_ids'">
              <template v-if="value.before">
                <b-tag size="is-medium" type="is-danger">
                  {{ practices_before }}
                </b-tag>
                <b-icon icon="arrow-right"></b-icon>
              </template>
              <b-tag size="is-medium" type="is-success">
                {{ practices_after }}
              </b-tag>
            </template>

            <template v-else-if="key !== 'job_title_id'">
              <template v-if="value.before">
                <b-tag size="is-medium" type="is-danger">
                  {{ value.before }}
                </b-tag>
                <b-icon icon="arrow-right"></b-icon>
              </template>
              <b-tag size="is-medium" type="is-success">
                {{ value.after }}
              </b-tag>
            </template>

            <template v-else>
              <template v-if="value.before">
                <b-tag size="is-medium" type="is-danger">
                  {{ job_titles.find(x => x.id === value.before).title }}
                </b-tag>
                <b-icon icon="arrow-right"></b-icon>
              </template>
              <b-tag size="is-medium" type="is-success">
                {{ job_titles.find(x => x.id === value.after).title }}
              </b-tag>
            </template>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import {getJobTitles, getPracticeDetailsById} from "@/api";

export default {
  name: "PendingEmployeeDetail.vue",
  props: ["row", "detail_delta"],

  data() {
    return {
      loading: false,
      job_titles: [],
      practices_before: '',
      practices_after: '',
      labels: [
        {key: "name", label: "Name"},
        {key: "email", label: "Email"},
        {key: "professional_num", label: "Professional ID"},
        {key: "desktop_num", label: "Desktop ID"},
        {key: "it_portal_num", label: "IT Portal ID"},
        {key: "active", label: "Active"},
        {key: "job_title_id", label: "Job Title"},
        {key: "practice_ids", label: "Practice"},
      ],
    }
  },
  watch: {
    detail_delta(data) {
      this.getPracticeNames(data.practice_ids)
    }
  },
  created() {
    this.getJobTitles()
  },
  methods: {
    async getJobTitles() {
      this.job_titles = await getJobTitles()
    },
    async getPracticeNames(practice_ids) {

      let practice_names_before = []
      practice_ids.before.forEach( (item) => {
        practice_names_before.push(getPracticeDetailsById(item))
      })
      this.practices_before = (await Promise.all(practice_names_before)).map(x => x.name).join(", ")

      let practice_names_after = []
      practice_ids.after.forEach( (item) => {
        practice_names_after.push(getPracticeDetailsById(item))
      })
      this.practices_after = (await Promise.all(practice_names_after)).map(x => x.name).join(", ")

    }
  }
}
</script>

<style scoped>

</style>