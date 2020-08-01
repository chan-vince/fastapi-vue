<template>
  <section v-if="row">
    <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>

    <div class="title is-4" v-if="row.target_id != null">
      <router-link :to="`/practice/${row.current_state.name}`">{{ row.current_state.name }}</router-link>
      <hr>
    </div>
    <div v-for="(element, index) in elements" :key="index">
      <template v-if="detail_delta[element.key]">
        <div class="columns">
          <div class="column is-2">
            <strong>{{ element.label }}</strong>
          </div>
          <div class="column">
            <div class="level-left">
              <template v-if="detail_delta[element.key].before">
                <b-tag size="is-medium" type="is-danger">{{ detail_delta[element.key].before }}</b-tag>
                <b-icon icon="arrow-right"></b-icon>
              </template>
              <b-tag size="is-medium" type="is-success">{{ detail_delta[element.key].after }}</b-tag>
            </div>
          </div>
        </div>
      </template>
    </div>
  </section>
</template>

<script>
export default {
  name: "PendingPracticeDetail.vue",
  props: ["row", "detail_delta"],
  data() {
    return {
      loading: false,
      elements: [
        {"label": "Practice Name", "key": "name"},
        {"label": "National Code", "key": "national_code"},
        {"label": "EMIS CDB Practice Code", "key": "emis_cdb_practice_code"},
        {"label": "Go Live Date", "key": "go_live_date"},
        {"label": "Closed", "key": "closed"},
        {"label": "Access Systems", "key": "access_systems"}
      ],
    }
  }
}
</script>

<style scoped>

</style>