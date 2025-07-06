# 🛒 Inventory CLI App

A sleek, no-nonsense inventory management system built in Python with a clean command-line interface. This tool is designed for local use, backed by PostgreSQL (or SQLite if you swap engines), and wrapped with eye candy using `rich`.

---

### 🔧 Features

* 🔐 User Registration & Login with secure `bcrypt` password hashing
* 📦 Add, View, Update, and Delete inventory items
* 📁 Category-wise organization
* 📉 Low-stock alerts
* 📊 Beautiful CLI tables via `tabulate`
* 📃 Persistent storage using **PostgreSQL** (configurable via `.env`)
* 🔍 Advanced Search (name/category/stock threshold)
* 📄 CSV Export of inventory
* 💬 Interactive CLI with `questionary` prompts
* 🎨 Polished UI using `rich` (panels, splash, centered banners)

---

### 📁 Project Structure

```bash
inventory-cli/
├── cli/                  # Command-line interface components
│   ├── InventoryCLI.py   # Main CLI loop
│   └── auth_menu.py      # Auth-related CLI prompts
├── db/                   # Database related files
│   ├── models.py         # SQLAlchemy models
│   └── init_db.py        # DB init logic
├── utils/                # Utility functions
│   └── helpers.py        # Common helper functions
├── .env                  # Database config (not pushed)
├── main.py               # App entry point
├── requirements.txt      # All dependencies
└── README.md             # This file
```

---

### 🚀 Run Locally

#### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/inventory-cli.git
cd inventory-cli
```

#### 2️⃣ Set up virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

#### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Set up `.env` file

Create a `.env` in the root with your DB connection string:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/inventory_db
```

> 💡 Use SQLite for dev by replacing the above with:

```env
DATABASE_URL=sqlite:///inventory.db
```

#### 5️⃣ Run the app

```bash
python main.py
```

---

### 👨‍💻 Credits

Built with ❤️ by **Vicky**
