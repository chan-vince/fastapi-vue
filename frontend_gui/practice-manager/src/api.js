import axios from 'axios';

export const client = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
  json: true
})

// export default {
//     async execute (method, resource, data) {
//       // inject the accessToken for each request
//       let accessToken = apiToken
//       return client({
//         method,
//         url: resource,
//         data,
//         headers: {
//           Authorization: `Bearer ${accessToken}`
//         }
//       }).then(req => {
//         return req.data
//       })
//     },
//     getPractices () {
//       return this.execute('get', '/api/v1/practice/')
//     }
//   }