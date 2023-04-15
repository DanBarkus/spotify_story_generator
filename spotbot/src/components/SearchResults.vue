<template>
    <div class="album_holder">
      <Album v-for="album in playlists" :key="album.id" :album="album" />
    </div>
    <div class="album_holder">
      <Album v-for="album in albums" :key="album.id" :album="album" />
    </div>
  </template>
  
  <script>
  import Album from './Album.vue'
  
  export default {
    name: 'AlbumList',
    components: {
      Album
    },
    mounted() {
        this.emitter.on("search-albums", (msg) => {
            this.albums = msg;
        }),
        this.emitter.on("search-playlists", (msg) => {
            this.playlists = msg;
        })
    },
    data() {
      return {
        albums: [],
        playlists: [],
      }
    }
  }
  </script>

<style scoped>
.album_holder {
    margin: auto;
    margin-top: 2rem;
    width: 60%;
    background-color: lightgray;
    padding: 2rem;
    border-radius: 1rem;
}
</style>