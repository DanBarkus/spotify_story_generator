<template>
  <div class="modal" v-if="show">
    <div class="modal-content" :style="{ backgroundColor: color }">
      <div class="modal-header">
        <img :src="album.cover" class="modal-cover" />
        <h3 class="modal-title">{{ album.title }}</h3>
        <p class="modal-artist">{{ album.artist }}</p>
      </div>
      <div class="modal-body">
        <ul class="modal-songs">
          <li v-for="(song, index) in album.songs" :key="index">{{ song }}</li>
        </ul>
      </div>
      <div class="modal-footer">
        <button class="modal-close" @click="close">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "AlbumModal",
    data() {
        return {
            album: {},
            show: false,
            color: ''
        }
    },
    methods: {
      close() {
        this.emitter.emit("show-modal", false);
        this.show = false;
      },
      getProminentColor(imageUrl, callback) {
        const img = new Image();
        img.crossOrigin = 'Anonymous';
        img.onload = function () {
            const canvas = document.createElement('canvas');
            canvas.width = this.width;
            canvas.height = this.height;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(this, 0, 0);

            const sampleSize = 4;
            let r = 0;
            let g = 0;
            let b = 0;

            for (let i = 0; i < sampleSize; i++) {
                const x = Math.floor(Math.random() * this.width);
                const y = Math.floor(Math.random() * this.height);
                const pixel = ctx.getImageData(x, y, 1, 1).data;
                r += pixel[0];
                g += pixel[1];
                b += pixel[2];
            }

            r = Math.floor(r / sampleSize);
            g = Math.floor(g / sampleSize);
            b = Math.floor(b / sampleSize);

            const color = `rgb(${r},${g},${b})`;
            callback(color);
        };
        img.src = imageUrl;
    }

    },
    mounted() {
        this.emitter.on("show-album", (msg) => {
            this.album = msg;
            this.getProminentColor(msg.cover, (nc) => {
                this.color = nc;
            });
            console.log(this.color);
        }),
        this.emitter.on("show-playlist", (msg) => {
            this.album = msg;
        }),
        this.emitter.on("show-modal", (msg) => {
            this.show = msg;
        })
    },
  };
</script>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-content {
  background-color: #fff;
  width: 500px;
  padding: 20px;
  border-radius: 10px;
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-top: 10px;
  margin-bottom: -6px;
}

.modal-artist {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.modal-cover {
  width: 200px;
  height: 200px;
  margin: 10px 0;
}

.modal-songs {
  list-style-type: none;
  padding: 10px;
  margin: 10px auto;
  max-height: 300px;
  overflow-y: auto;
  background-color: lightgrey;
  border-radius: 1em;
  width: 50%;
}

.modal-songs li {
  font-size: 16px;
  color: #333;
  padding: 0.25em 0;
  padding-left: 2em;
  margin-bottom: -3px;
  border: darkgrey 3px solid;
}

.modal-close {
  background-color: #f44336;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}
</style>
