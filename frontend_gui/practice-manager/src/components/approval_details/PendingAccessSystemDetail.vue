<template>
  <section v-if="row">
    <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>
    <div class="title is-4" v-if="row.target_id != null">
      <router-link :to="`/practice/${this.practice.name}`">{{ this.practice.name }}</router-link>
      <hr>
    </div>

    <template>
      <div class="columns">
        <div class="column is-2">
          <strong>Access Systems:</strong>
        </div>
        <div class="column">
          <div class="level">
            <div class="level-left">
              <b-tag size="is-medium" type="is-danger">{{ this.before_systems ? this.before_systems : "None" }}</b-tag>
              <b-icon icon="arrow-right"></b-icon>
              <b-tag size="is-medium" type="is-success">{{ this.after_systems ? this.after_systems : "None" }}</b-tag>
            </div>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<script>
import {getPracticeDetailsById} from "@/api";

export default {
  name: "PendingAccessSystemDetail.vue",
  props: ["row", "detail_delta"],

  data() {
    return {
      loading: true,
      access_systems: [
        {"name": "ICE", "id": 1},
        {"name": "SystemOne", "id": 2},
        {"name": "Vision 3", "id": 3}
      ],
      practice: {},
      before_systems: [],
      after_systems: [],
      prefix_word: ""
    }
  },
  watch: {
    detail_delta() {
      this.before_systems = this.$props.detail_delta.before.map(x => x.name).join(", ")
      this.after_systems = this.$props.detail_delta.after.map(x => x.name).join(", ")
    }
  },
  methods: {
    async getPracticeDetails() {
      this.practice = await getPracticeDetailsById(this.$props.row.target_id)
      this.loading = false
    }
  },
  created() {
    this.getPracticeDetails()
  }
}
</script>

<style scoped>

</style>