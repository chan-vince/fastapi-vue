<template>
    <div class="card">
        <div class="level" style="margin: 30px 75px 0px 10px">
            <div class="level-left">
                <div class="card-header-title">
                    <p class="title is-3">
                        Branches
                    </p>
                </div>
            </div>
            <div class="level-right">
                <b-button type="is-primary" outlined icon-left="plus">
                    Add
                </b-button>
            </div>
        </div>
        <div class="card-content">
            <div class="card" v-for="(address, index) in addresses" :key="address.id">
                <div class="card-header-title">
                    <p class="title is-4">
                        Address {{ index + 1 }}
                    </p>
                </div>
                <div class="card-content" style="padding-right: 50px">
                    <b-field label="Line 1" horizontal>
                        <b-input v-model="address.line_1" size="is-default"
                            placeholder="Line 1 of Address"></b-input>
                    </b-field>
                    <b-field label="Line 2" horizontal>
                        <b-input v-model="address.line_2" size="is-default"
                            placeholder="Line 2 of Address"></b-input>
                    </b-field>
                    <b-field label="Town" horizontal>
                        <b-input v-model="address.town" size="is-default"
                            placeholder="Town"></b-input>
                    </b-field>
                    <b-field label="County" horizontal>
                        <b-input v-model="address.county" size="is-default"
                            placeholder="County"></b-input>
                    </b-field>
                    <b-field label="Postcode" horizontal>
                        <b-input v-model="address.postcode" size="is-default"
                            placeholder="Postcode"></b-input>
                    </b-field>
                    <b-field label="Contact email (DTS)" horizontal>
                        <b-input v-model="address.dts_email" size="is-default"
                            placeholder="Contact email"></b-input>
                    </b-field>
                    <b-field label="Contact phone number" horizontal>
                        <b-input v-model="address.phone_num" size="is-default"
                            placeholder="Contact phone number"></b-input>
                    </b-field>
                    <hr>
                    <div v-for="(cidr, index) in address.ip_ranges" :key="cidr.id">
                        <div style="margin-bottom: 10px">
                            <b-field :label="`CIDR ${index + 1}`" horizontal>
                                <b-input v-model="cidr.cidr" size="is-default"
                                    placeholder="CIDR Range"></b-input>
                            </b-field>
                        </div>
                    </div>

                    <div class="level-right" style="padding-top: 20px">
                        <b-button type="is-primary" outlined icon-left="content-save">Save</b-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'GPDetailsAddressesForm',
    props: ['practice_details'],
    data() {
        // const today = new Date()
        return {
            // go_live_date: new Date(),
            // minDate: new Date(today.getFullYear(), today.getMonth(), today.getDate()),
            addresses: []
        }
    },
    watch: { 
          practice_details: function(details) {
            this.addresses = details['addresses']
        }
    },
    created() {
    }
}
</script>

<style scoped>
.title {
    font-weight: lighter;
}
</style>