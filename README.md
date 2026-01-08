# Client Sales Receipt API

This project is a **FastAPI-based Sales API** designed to provide
**receipt-wise sales data** to external clients in a **secure, scalable, and controlled manner**.

The API is optimized for **large datasets** by enforcing **day-by-day data fetching**, even when a date range is provided.

---

## Authentication

The API uses **token-based authentication**.

### Login
Clients will be provided with a **username and password** by the company.

**Authentication Flow**
1. Login using provided credentials
2. Receive an access token
3. Use the token in subsequent API requests
4. Logout when finished

---

## Sales Receipt Data

The API provides **receipt-wise sales data** including:
- Receipt ID
- Transaction date
- Store code
- Customer mobile number
- Payment amount
- Item-level details (price, quantity, discount)

---

## Date Range Parameters

The API accepts a **date range** using:

- `from_date` → Start date (YYYY-MM-DD)
- `to_date` → End date (YYYY-MM-DD)


## Data Fetching Strategy (IMPORTANT)

Although a date range is provided, the API is **designed to fetch data one day at a time**.

### Why this approach?
- Prevents server timeouts
- Avoids very large payloads
- Ensures stable performance
- Handles high-volume transactional data safely

### Client Responsibility
Clients are expected to:
1. Start from `from_date`
2. Fetch data for **one day**
3. Store/process the response
4. Move to the next date
5. Repeat until `to_date` is reached

This looping logic **must be handled by the client**.

---

## Response Characteristics

- Data is grouped by **Receipt ID**
- Each receipt contains its associated item list
- No aggregation or transformation is done at API level
- All values are sourced directly from the database

---

## Performance Notes

- Fetching multiple days in a single request is **not recommended**
- Large date ranges can generate very large responses
- Best practice is **one request per day**

---

## Technology Stack

- FastAPI
- SQL Server
- SQLAlchemy
- Token-based Authentication
- Azure App Service (Deployment Target)

---

## Support

For access credentials or integration assistance, please contact the **Company Technical Team**.
