<template>
    <Plotly :data="data" :layout="layout" :display-mode-bar="false"></Plotly>
</template>

<script>

export default {
    data: () => ({
      data: [],
      layout: {
        title: "Média de salarios por ano",
        xaxis: {
            autorange: false
            , type: 'category'
             , categoryorder: 'array'
             , categoryarray: []
        }
        },
    }),
    async mounted() {
        //const response = await this.$axios.$get(`/getPrecipitacao?cod_uc=${this.cod_uc}&ano=${this.ano}`);
        const response = await this.$axios.$get(`/getSalariesAverageBySize?size=L`);
        this.data.push(response)
        this.categoryarray = response['x']
    },
  }
</script>