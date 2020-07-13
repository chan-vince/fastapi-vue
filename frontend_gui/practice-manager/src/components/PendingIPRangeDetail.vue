<template>
    <section v-if="aux_info">
        <b-loading :is-full-page="false" :active.sync="loading" :can-cancel="false"></b-loading>
        <div class="columns">
            <div class="column is-1">
                <strong>
                    Practice:
                </strong>
            </div>
            <div class="column">
                {{ aux_info.name }}
            </div>
        </div>

        <div class="columns">
            <div class="column is-1">
                <strong>
                    Location:
                </strong>
            </div>
            <div class="column">
                {{ address.line_1 }}, {{ address.town }}
            </div>
        </div>

        <div class="columns">
            <div class="column is-1">
                <strong>
                    CIDR:
                </strong>
            </div>
            <div class="column">
                <section class="level-left">
                    <template v-if="row.modify">
                        <b-tag size="is-medium" type="is-danger">{{ address.ip_ranges.map(item => item.cidr).join(", ") }}</b-tag>
                        <b-icon icon="arrow-right"></b-icon>
                    </template>
                    <b-tag size="is-medium" type="is-success">{{ row.payload.cidr }}</b-tag>
                </section>
            </div>
        </div>
    </section>
</template>

<script>
    export default {
        name: "PendingIPRangeDetail",
        props: ["row", "aux_info", "modify"],

        data() {
            return {
                loading: true,
                address: {ip_ranges: [{}]}
            }
        },
        watch: {
            aux_info() {
                if(this.aux_info !== null){
                    this.getAddressForIpRange();
                    this.loading = false
                }
            }
        },
        methods: {
            getAddressForIpRange() {
                const address_id = this.$props.row.payload.address_id
                const addresses = this.$props.aux_info.addresses

                for (let i = 0; i < addresses.length; i++) {
                    if (addresses[i].id === address_id) {
                        this.address = addresses[i];
                    }
                }
            }
        }
    };
</script>