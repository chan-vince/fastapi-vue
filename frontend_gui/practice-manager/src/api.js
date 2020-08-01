import axios from 'axios';

export const client = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_URL,
    json: true
})

const baseURL = process.env.VUE_APP_BACKEND_URL
const apiVersion = `api/v1`
const apiBase = `${baseURL}${apiVersion}`

export const getPracticeAll = (skip, limit) => {
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

export const getPracticeDetailsByName = (practice_name) => {
    return axios(`${apiBase}/practice/name`, {
        method: 'GET',
        params: {
            name: practice_name
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error));
}

export const getPracticeDetailsById = (practice_id) => {
    return axios(`${apiBase}/practice/id`, {
        method: 'GET',
        params: {
            practice_id: practice_id
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error));
}

export const getPracticeNamesAll = () => {
    return axios(`${apiBase}/practice/name/all`, {
        method: 'GET',
    })
        .then(response => response.data.names)
        .catch(error => console.log(error));
}

export const getPracticeCount = () => {
    return axios(`${apiBase}/practice/count`, {
        method: 'GET',
    })
        .then(response => response.data)
        .catch(error => console.log(error));
}

export const getAccessSystemsAll = () => {
    return axios(`${apiBase}/access_system/all`, {
        method: 'GET',
    })
        .then(response => response.data)
        .catch(error => console.log(error))
}

export const getEmployeeCount = () => {
    return axios(`${apiBase}/employee/count`, {
        method: 'GET',
    })
        .then(response => response.data)
        .catch(error => console.log(error));
}

export const getEmployeeAll = (skip, limit) => {
    return axios(`${apiBase}/employee/all`, {
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

export const getEmployeeNames = () => {
    return axios(`${apiBase}/employee/names`, {
        method: 'GET',
    })
        .then(response => response.data.names)
        .catch(error => console.log(error));
}

export const getEmployeeByName = (name) => {
    return axios(`${apiBase}/employee/name`, {
        method: 'GET',
        params: {
            name: name
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error));
}

export const getJobTitles = () => {
    return axios(`${apiBase}/employee/job-titles`, {
        method: 'GET'
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

export const getPendingChangesAll = (skip, limit) => {
    return axios(`${apiBase}/changes/pending/all`, {
        method: 'GET',
        params: {
            skip: skip,
            limit: limit
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error.response.data.detail));
}

export const getHistoricChangesAll = (skip, limit) => {
    return axios(`${apiBase}/changes/history/all`, {
        method: 'GET',
        params: {
            skip: skip,
            limit: limit
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error.response.data.detail));
}

export const getPendingChangeById = (id) => {
    return axios(`${apiBase}/changes/pending/id`, {
        method: 'GET',
        params: {
            id: id
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error.response.data.detail));
}

export const getDeltaPendingChangeById = (id) => {
    return axios(`${apiBase}/changes/pending/id/delta`, {
        method: 'GET',
        params: {
            id: id
        }
    })
        .then(response => response.data)
        .catch(error => console.log(error.response.data.detail));
}

export const postChangeRequest = (request) => {
    return axios(`${apiBase}/change/request`, {
        method: 'POST',
        data: request
    })
        .then(response => response)
        .catch(error => console.log(error.response.data.detail));
}

export const approveChangeRequest = (change_request_id, approver_id) => {
    return axios(`${apiBase}/change/request/approve`, {
        method: 'PUT',
        params: {
            change_request_id: change_request_id,
            approver_id: approver_id
        }
    })
        .then(response => response)
        .catch(error => console.log(error.response.data.detail));
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