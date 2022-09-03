<template>
  <v-container>
    <v-row>
      <v-container>
        <h2>Conheça o {{ $route.params.nome }}</h2>
        <p>Visto pela última vez: Rio de Janeiro</p>
      </v-container>
    </v-row>
    <v-row>
      <v-carousel :show-arrows="true" height="350">
        <v-carousel-item
          v-for="(item, i) in items"
          :key="i"
          :src="item.src"
        ></v-carousel-item>
      </v-carousel>
    </v-row>
    
    <v-row>
      <plotly-map></plotly-map>
    </v-row>
  </v-container>

</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
        },
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
        },
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
        },
        {
          src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg",
        },
      ],
    };
  },
};
</script>

<style scoped>
</style>
