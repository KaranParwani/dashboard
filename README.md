**Setup Instructions for Patient CRUD API**

### Prerequisites

1. **Docker & Docker Compose**: Ensure Docker and Docker Compose are installed on your system.
2. **Environment Variables**: Place your `.env` file in a folder called `config` with database credentials.
3. **FastAPI Backend**: Backend code is written in FastAPI.
4. **Frontend**: React application, styled using Material-UI.

---

### Step 1: Clone Repositories

```bash
# Backend repository
git clone https://github.com/KaranParwani/dashboard.git

# Frontend repository
git clone https://github.com/KaranParwani/dashboard-FE.git
```

These both are public repository

---

### Step 2: Setup Backend

1. **Navigate to the backend directory**:

   ```bash
   cd dashboard
   ```

2. **Create a `.env` inside config folder**: Use the provided environment variables format.

   ```env
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

3. **Dockerize the backend**:
   Run the `Dockerfile`:

   ```dockerfile
   docker build -t fastapi-backend .
   ```

4. **Start Backend**:

   ```bash
   Click on run from docker desktop
   ```

---

### Step 3: Setup Frontend

1. **Navigate to the frontend directory**:

   ```bash
   cd dashboard-fe
   ```

2. **Dockerize the frontend**:
   Run the `Dockerfile`:

   ```dockerfile
    docker build -t react-frontend .
   ```

3. **Start Frontend**:

   ```bash
   Click on run from docker desktop
   ```

---

**API Documentation for Patient CRUD**

### 1. **Admin Login**

**Endpoint**: `/admin/login`
Credentials are created as soon as the backend app is started

**Method**: `POST`

**Request Body**:

```json
{
  "user_email": "test",
  "password": "test"
}
```

**Response**:

* `200 OK`: Success

  ```json
  {
    "access_token": "<token>",
    "token_type": "Bearer"
  }
  ```
* `401 Unauthorized`: Invalid credentials

---

### 2. **Create Patient**

**Endpoint**: `/patients`

**Method**: `POST`

**Headers**:
`Authorization: Bearer <token>`

**Request Body**:

```json
{
    "first_name": "Mercedes",
    "middle_name": "Reagan Pugh",
    "last_name": "Page",
    "date_of_birth": "2025-06-05",
    "blood_type": "Provident porro ius",
    "gender": "Male",
    "contacts": {
        "phone_number": "+14378372123",
        "email": "nuly@mailinator.com",
        "address_1": "863 West Cowley Avenue",
        "address_2": "Nihil quisquam exerc"
    },
    "dob": "2025-06-04"
}
```

**Response**:

* `200 Created`:

  ```json
    {
    "status_code": 200,
    "message": "Successfully added record",
    "data": {
        "patient_id": 23
      }
    }
  ```

---

### 3. **Read All Patients**

**Endpoint**: `/patients`

**Method**: `GET`

**Headers**:
`Authorization: Bearer <token>`

**Response**:

* `200 OK`:

  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "age": 45,
      "address": "123 Elm Street",
      "contact": "555-1234"
    }
  ]
  ```

---

### 4. **Update Patient**

**Endpoint**: `/patients/{id}`

**Method**: `PUT`

**Headers**:
`Authorization: Bearer <token>`

**Request Body**:

```json
{
  "name": "John Smith",
  "age": 46,
  "address": "124 Oak Street",
  "contact": "555-5678"
}
```

**Response**:

* `200 OK`:

  ```json
  {
    "id": 1,
    "name": "John Smith",
    "age": 46,
    "address": "124 Oak Street",
    "contact": "555-5678"
  }
  ```

---

### 5. **Delete Patient**

**Endpoint**: `/patients/{id}`

**Method**: `DELETE`

**Headers**:
`Authorization: Bearer <token>`

**Response**:

* `204 No Content`
