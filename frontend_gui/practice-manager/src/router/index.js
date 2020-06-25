import Vue from 'vue'
import VueRouter from  'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import AdminPage from '../pages/AdminPage.vue'
import PracticePage from '../pages/PracticePage.vue'

Vue.use(VueRouter);

const routes = [
    {
      path: '/login',
      component: LoginPage,
      meta: {
        title: 'GP Access System Login',
        metaTags: [
          {
            name: 'description',
            content: 'Login Page.'
          },
          {
            property: 'og:description',
            content: 'Login Page.'
          }
        ]
      }
    },
    {
      path: '/admin',
      component: AdminPage,
      meta: {
        title: 'Admin Portal - GP Access System',
        metaTags: [
          {
            name: 'description',
            content: 'The about page of our example app.'
          },
          {
            property: 'og:description',
            content: 'The about page of our example app.'
          }
        ]
      }
    },
    {
      path: '/practice',
      component: PracticePage,
      meta: {
        title: 'GP Portal - GP Access System',
        metaTags: [
          {
            name: 'description',
            content: 'The about page of our example app.'
          },
          {
            property: 'og:description',
            content: 'The about page of our example app.'
          }
        ]
      }
    }
  ];

const router = new VueRouter({
  routes,
  mode: 'history'
});

export default router