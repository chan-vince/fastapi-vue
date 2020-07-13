import Vue from 'vue'
import VueRouter from  'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import AllPracticesPage from '../pages/AllPracticesPage.vue'
import AllEmployeesPage from '../pages/AllEmployeesPage.vue'
import PracticePage from '../pages/PracticePage.vue'
import ApprovalsPage from '../pages/ApprovalsPage.vue'
import TestPage from '../pages/TestPage.vue'
import NotFoundPage from '../pages/NotFoundPage.vue'

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
      path: '/employees',
      component: AllEmployeesPage,
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
      path: '/approvals',
      component: ApprovalsPage,
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
    },
    { path: '/', redirect: '/practices' },
    { path: "/404", component: NotFoundPage },
    { path: "*", component: NotFoundPage }
  ];

const router = new VueRouter({
  routes,
  mode: 'history'
});

export default router