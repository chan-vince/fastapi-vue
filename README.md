# prelim-francis
POC for luton NHS

# Usage

(todo: docker instructions)


# Architecture

(Proposed)

The core data is stored within a SQL (MariaDB) database.

The backend is essentially CRUD interface in front of a database. This is built on the [fastapi](https://fastapi.tiangolo.com/) framework to provide a quick option that can scale in the future. The database interactions will use SQLAlchemy as an ORM to abstract the database calls, allowing minimal rework to switch database backends (within reason).

The frontend will make the API calls to the backend to retrieve the data and present it in various views depending on the role of the user. This will be implemented in React or Vue.js.
