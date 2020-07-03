import Vue from 'vue'
import VueRouter from  'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import AllPracticesPage from '../pages/AllPracticesPage.vue'
import PracticePage from '../pages/PracticePage.vue'
import PendingApprovalsPage from '../pages/PendingApprovalsPage.vue'
import TestPage from '../pages/TestPage.vue'

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
      path: '/practices',
      component: AllPracticesPage,
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
      path: '/practice/:name',
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
    },
    {
      path: '/approvals',
      component: PendingApprovalsPage,
      meta: {
        title: 'Approvals',
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
      path: '/test',
      component: TestPage,
      meta: {
        title: 'TestPage',
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