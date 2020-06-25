import axios from 'axios';
// import { apiToken } from '@/env';

export const client = axios.create({
  baseURL: 'http://localhost:5000/',
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