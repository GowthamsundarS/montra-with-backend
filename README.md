<div align="center">

<img src="assets/logo.png" width="120">

# 💰 Montra

### Personal Finance Tracker Application

A full-stack finance management application built to help users track income, expenses, and manage their personal finances efficiently.

<br>

<img src="https://img.shields.io/badge/Flutter-Mobile%20App-blue?style=for-the-badge&logo=flutter">
<img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi">
<img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql">
<img src="https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge">

<br><br>

</div>


# 📌 About The Project

**Montra** is a personal finance tracking application that allows users to securely manage their financial activities.

Users can record income, expenses, view their financial overview, and manage their profile from a simple and intuitive mobile interface.

The project follows a modern full-stack architecture:

```
Flutter Mobile App
        |
        |
     REST API
        |
        |
     FastAPI Backend
        |
        |
 PostgreSQL Database
```

---

# ✨ Features

## 🔐 Authentication

- User registration
- Secure login
- JWT token authentication
- Password hashing using bcrypt
- Protected API routes


## 💵 Income Management

- Add income transactions
- Update income details
- Delete income records
- View income history
- Categorize income sources


## 💸 Expense Management

- Add expenses
- Edit expense records
- Delete expenses
- Track spending categories
- View expense history


## 📊 Financial Dashboard

- Total balance calculation
- Total income overview
- Total expense overview
- Transaction summaries


## 👤 Profile Management

- View user profile
- Update profile details
- Upload profile picture


---

# 🛠 Tech Stack


<table>

<tr>
<th>Technology</th>
<th>Purpose</th>
</tr>

<tr>
<td>Flutter</td>
<td>Mobile Application Development</td>
</tr>

<tr>
<td>Dart</td>
<td>Frontend Programming Language</td>
</tr>

<tr>
<td>FastAPI</td>
<td>Backend REST API</td>
</tr>

<tr>
<td>PostgreSQL</td>
<td>Database Management</td>
</tr>

<tr>
<td>SQLAlchemy</td>
<td>Database ORM</td>
</tr>

<tr>
<td>Pydantic</td>
<td>Data Validation</td>
</tr>

<tr>
<td>JWT</td>
<td>User Authentication</td>
</tr>

<tr>
<td>Bcrypt</td>
<td>Password Encryption</td>
</tr>

</table>


---

# 📂 Project Structure


```
montra-with-backend/

│
├── app/
│   │
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── authentication/
│   └── utils/
│
├── requirements.txt
├── .env
├── README.md
└── ...
```


---

# ⚙️ Installation & Setup


## 1. Clone Repository

```bash
git clone https://github.com/GowthamsundarS/montra-with-backend.git

cd montra-with-backend
```


---

## 2. Create Virtual Environment


### Windows

```bash
python -m venv venv

venv\Scripts\activate
```


### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```


---

## 3. Install Dependencies


```bash
pip install -r requirements.txt
```


---

# 🔑 Environment Configuration


Create a `.env` file:


```env
DATABASE_URL=postgresql://username:password@localhost/database_name


SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```


---

# ▶️ Running Backend


Start FastAPI server:


```bash
uvicorn app.main:app --reload
```


Server runs at:

```
http://127.0.0.1:8000
```


API Documentation:

```
http://127.0.0.1:8000/docs
```


---

# 🔌 API Endpoints


## Authentication

| Method | Endpoint | Description |
|-|-|-|
| POST | `/users` | Register user |
| POST | `/login` | Login user |


## Income

| Method | Endpoint | Description |
|-|-|-|
| GET | `/income` | Get income |
| POST | `/income` | Add income |
| PUT | `/income/{id}` | Update income |
| DELETE | `/income/{id}` | Delete income |


## Expense

| Method | Endpoint | Description |
|-|-|-|
| GET | `/expense` | Get expenses |
| POST | `/expense` | Add expense |
| PUT | `/expense/{id}` | Update expense |
| DELETE | `/expense/{id}` | Delete expense |


## Profile

| Method | Endpoint | Description |
|-|-|-|
| GET | `/profile` | View profile |
| PUT | `/profile` | Update profile |


---

# 📱 Application Screenshots


<div align="center">

<img src="screenshots/login.png" width="250">

<img src="screenshots/dashboard.png" width="250">

<img src="screenshots/income.png" width="250">

<img src="screenshots/expense.png" width="250">

</div>


---

# 🚀 Deployment


## Backend

Hosted using:

- Render


## Database

Hosted using:

- Neon PostgreSQL


Architecture:

```
Flutter App

      ↓

Render FastAPI Server

      ↓

Neon PostgreSQL Database
```


---

# 🔒 Security

Implemented security features:

✅ JWT Authentication  
✅ Password hashing  
✅ Protected routes  
✅ Environment variables  
✅ Database validation  


---

# 🔮 Future Improvements


- 📈 Advanced financial charts
- 🔔 Expense reminders
- 📧 Email verification
- 🔑 Forgot password
- 📄 Export financial reports
- 🌙 Dark mode
- 💰 Budget planning
- 🤖 AI-based spending insights


---

# 🤝 Contributing


Contributions are welcome!


1. Fork the repository

2. Create your feature branch


```bash
git checkout -b feature/new-feature
```


3. Commit changes


```bash
git commit -m "Added new feature"
```


4. Push changes


```bash
git push origin feature/new-feature
```


5. Create Pull Request


---

# 👨‍💻 Developer


<div align="center">

## Gowtham Sundar S

BCA Artificial Intelligence & Data Science Student

<br>

GitHub:

<a href="https://github.com/GowthamsundarS">
github.com/GowthamsundarS
</a>

</div>


---

<div align="center">

⭐ If you like this project, consider giving it a star!

</div>
