<template>
  <div class="home">
    <section class="hero is-medium is-dark mb-6">
      <!-- #hero-body 这些东西都是现成的？ -->
      <div class="hero-body has-text-centered">
        <p class="title mb-6">Welcom to Djacket</p>
        <p class="subtitle">The best jacket store online</p>
      </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">Latest products</h2>
      </div>
      <!-- column is-3啥意思   还有这一部分是如何执行的 并没有见到它的结尾啊-->
      <!--  is-3 表示这个列占据了 12 格网格中的 3 格，即 1/4 的宽度 -->
      <div class="column is-3" v-for="product in latestProducts" v-bind="product.id">
        <!-- 为什么下面的内容都是循环里的 -->
        <div class="box">
          <figure class="image mb-4">
            <!-- v-bind:src="product.get_thumbnail"  啥意思 -->
            <img v-bind:src="product.get_thumbnail" />
          </figure>

          <h3 class="is-size-4">{{ product.name }}</h3>
          <p class="is-size-6 has-text-grey">${{ product.price }}</p>

          <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4">View details</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "HomeView",
  // 为啥这么写data()
  // data 方法返回组件的数据对象，包含 latestProducts 数组，用于存储从服务器获取的产品数据。
  data() {
    return {
      latestProducts: [],
    };
  },
  // components有什么作用
  components: {},
  // 生命周期钩子：什么概念，如何理解。。mounted 方法在组件挂载后立即调用 getLatestProducts 方法，发送请求获取最新产品数据。
  // data()这些是自己有的方法，methods里面的是自己写的方法？
  mounted() {
    this.getLatestProducts();
  },
  methods: {
    getLatestProducts() {
      axios
        .get("/api/v1/latest-products/")
        .then((response) => {
          this.latestProducts = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.image {
  margin-top: -1.25rem;
  margin-left: -1.25rem;
  margin-right: -1.25rem;
}
</style>
