<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Djackets</strong></router-link>
        <a class="navbar-burger" role="button" aria-label="menu" aria-expanded="false" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div :class="['navbar-menu', {'is-active': showMobileMenu}]" id="navbar-menu">
        <div class="navbar-end">
          <router-link to="/summer" class="navbar-item">Summer</router-link>
          <router-link to="/winter" class="navbar-item">Winter</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <router-link to="/log-in" class="button is-light">Log in</router-link>
              <router-link to="/cart" class="button is-success">
                <span>Cart</span>
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view/>
    </section>
    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2024</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showMobileMenu: false,
    };
  },
};
</script>

<style lang="scss">
@import '../node_modules/bulma/css/bulma.css';
</style>
