<template>
    <div id="button_holder">
        <div @click="event => this.show_playlists = false" class="toggle_button">
            Albums
        </div>
        <div @click="event => this.show_playlists = true" id="playlist_button" class="toggle_button" :class="{active:this.show_playlists}">
            Playlists
        </div>
    </div>
    <div v-if="show_playlists" id="playlists_holder" class="album_holder">
      <Album v-for="album in playlists" :key="album.id" :album="album" />
    </div>
    <div v-else id="albums_holder" class="album_holder">
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
        show_playlists: false,
      }
    }
  }
  </script>

<style scoped>
.album_holder {
    margin: auto;
    width: 60%;
    background-color: #F4AC45;
    padding: 2rem;
    border-radius: 1rem;
    border-top-left-radius: 0rem;
}

#playlists_holder {
    background-color: #DB514A;
}

#button_holder {
    display: flex;
    width: 60%;
    margin: auto;
    margin-top: 2em;
    flex-direction: row;
    align-items: flex-end;
    justify-content: flex-start;
}

.toggle_button {
    width: 7rem;
    background-color: #F4AC45;
    margin-left: -2rem;
    padding: 0.5rem;
    text-align: center;
    border-top-left-radius: 1em;
    border-top-right-radius: 1em;
    z-index: 5;
}

#playlist_button {
    background-color: #DB514A;
    margin-left: -1rem;
    z-index: 1;
}

.active {
    z-index: 10 !important;
}
</style>