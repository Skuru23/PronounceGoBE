# PronounceGoBE

// ...existing code...

## Setup Instructions

### Prerequisites

- Python 3.8+
- Poetry
- Alembic

### Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd PronounceGoBE
   ```

2. Create .env

3. Install dependencies using Poetry:

   ```sh
   poetry install
   ```

4. Apply database migrations using Alembic:

   ```sh
   alembic upgrade head
   ```

5. Run the `add_to_db.py` script to populate the database:
   ```sh
   python import_dictionary/add_to_db.py
   ```

### Running the Application

1. Start the application:
   ```sh
   python -m main.py
   ```

// ...existing code...
