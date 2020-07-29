import axios from 'axios';

export const client = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
  json: true
})

const baseURL = process.env.VUE_APP_BACKEND_URL
const apiVersion = `api/v1`
const apiBase = `${baseURL}${apiVersion}`

export const getPracticesAll = (skip, limit) => {
  return axios(`${apiBase}/practice/all`, {
    method: 'GET',
    headers: {},
    params: {
      skip: skip,
      limit: limit
    }
  })
      .then(response => response.data)
      .catch(error => console.log(error));
};

export const getPracticeNamesAll = () => {
  return axios(`${apiBase}/practice/name/all`, {
    method: 'GET',
  })
      .then(response => response.data.names)
      .catch(error => console.log(error));
}

export const getPracticesCount = () => {
  return axios(`${apiBase}/practice/count`, {
    method: 'GET',
  })
      .then(response => response.data)
      .catch(error => console.log(error));
}

export const getPendingChangesCount = () => {
  return axios(`${apiBase}/changes/pending/count`, {
    method: 'GET',
  })
      .then(response => response.data)
      .catch(error => console.log(error));
}


// export default {
//     async execute (method, resource, data) {
//       // inject the accessToken for each request
//       let accessToken = apiToken
//       return client({
//         method,
//         url: resource,
//         data,
//         headers: {
//           Authorization: `Bearer ${accessToken}`,
//           'content-type': 'application/json', // whatever you want
//         }
//       }).then(req => {
//         return req.data
//       })
//     },
//     getPractices () {
//       return this.execute('get', '/api/v1/practice/')
//     }
//   }