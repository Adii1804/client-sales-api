from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import text
from .database import engine
from datetime import date
import uuid
import os

app = FastAPI(title="Client Sales API")

USERS = {
    os.getenv("API_USERNAME"): os.getenv("API_PASSWORD")
}

ACTIVE_TOKENS = set()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if USERS.get(form_data.username) != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid.uuid4())
    ACTIVE_TOKENS.add(token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def verify_token(token: str = Depends(oauth2_scheme)):
    if token not in ACTIVE_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/auth/logout")
def logout(token: str = Depends(oauth2_scheme)):
    ACTIVE_TOKENS.discard(token)
    return {"message": "Logged out successfully"}

@app.get("/health/db", dependencies=[Depends(verify_token)])
def check_database_connection():
    """
    Test database connectivity for debugging
    """
    import os
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test")).fetchone()
            return {
                "status": "connected",
                "test_query": "SUCCESS",
                "db_host": os.getenv("DB_HOST"),
                "db_port": os.getenv("DB_PORT"),
                "db_name": os.getenv("DB_NAME")
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "error_type": type(e).__name__,
            "db_host": os.getenv("DB_HOST"),
            "db_port": os.getenv("DB_PORT"),
            "db_name": os.getenv("DB_NAME")
        }

@app.get("/sales/receipt-wise", dependencies=[Depends(verify_token)])
def get_sales_receipt_wise(
    from_date: date = Query(..., description="YYYY-MM-DD"),
    to_date: date = Query(..., description="YYYY-MM-DD"),
):
    """
    Fetch receipt-wise sales BETWEEN from_date and to_date.
    """

    if to_date < from_date:
        raise HTTPException(
            status_code=400,
            detail="to_date must be greater than or equal to from_date"
        )

    sql = text("""
        SELECT
            b.RECEIPTID,
            b.CUSTMOBILENO,
            b.TRANSDATE,
            b.STORE,
            b.PAYMENTAMOUNT,

            (
                SELECT
                    s.Itemid,
                    s.price,
                    s.quantity,
                    s.discount
                FROM dbo.vw_LastYearSales s
                WHERE s.RECEIPTID = b.RECEIPTID
                  AND s.TRANSDATE >= :from_date
                  AND s.TRANSDATE < DATEADD(day, 1, :to_date)
                FOR JSON PATH
            ) AS ITEMS

        FROM dbo.vw_LastYearSales b
        WHERE b.TRANSDATE >= :from_date
          AND b.TRANSDATE < DATEADD(day, 1, :to_date)
        GROUP BY
            b.RECEIPTID,
            b.CUSTMOBILENO,
            b.TRANSDATE,
            b.STORE,
            b.PAYMENTAMOUNT
        ORDER BY b.TRANSDATE, b.RECEIPTID
    """)

    with engine.connect() as conn:
        rows = conn.execute(
            sql,
            {"from_date": from_date, "to_date": to_date}
        ).mappings().all()

    return {
        "from_date": from_date,
        "to_date": to_date,
        "records_returned": len(rows),
        "data": [
            {
                "receipt_id": r["RECEIPTID"],
                "customer_mobile": r["CUSTMOBILENO"],
                "trans_date": r["TRANSDATE"],
                "store": r["STORE"],
                "payment_amount": r["PAYMENTAMOUNT"],
                "items": r["ITEMS"]
            }
            for r in rows
        ]
    }
