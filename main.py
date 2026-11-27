"""Task management API and arithmetic endpoints."""

import socket

from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Task Management API")

# Allow the frontend (e.g. a Next.js dev server on another origin) to call this
# API directly from the browser. Tighten allow_origins to your frontend's exact
# origin(s) before deploying to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Operands(BaseModel):
    """Operands used by arithmetic endpoints."""

    a: float
    b: float


class Item(BaseModel):
    """Item stored in the in-memory collection."""

    name: str
    description: Optional[str] = None


items: Dict[int, Item] = {
    1: Item(name="item1", description="first item"),
    2: Item(name="item2", description="second item"),
    3: Item(name="item3", description="third item"),
}

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/")
def root() -> dict:
    """Return the application health message."""
    return {"message": "it works !"}


@app.get("/addition")
def addition(a: int, b: int) -> dict:
    """Return the sum of two integers."""
    return {"result a+b=": a + b, "developer": "Dev1"}


@app.get("/soustraction")
def soustraction(a: int, b: int) -> dict:
    """Return the difference between two integers."""
    return {"result a-b=": a - b, "developer": "Dev1"}


def current_ip() -> str:
    """IP address of the network interface connected to the Internet."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


@app.get("/greeting")
def greeting(name: str) -> dict:
    """Return a greeting with host information."""
    return {
        "message": f"Hello, {name}",
        "developer": "Dev2",
        "hostname": socket.gethostname(),
        "IP": current_ip(),
    }


@app.post("/multiply")
def multiply(op: Operands) -> dict:
    """Return the product of two operands."""
    return {"result a*b=": op.a * op.b, "developer": "Dev1"}


@app.post("/divide")
def divide(op: Operands) -> dict:
    """Return the quotient of two operands."""
    if op.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result a/b=": op.a / op.b, "developer": "Dev2"}

@app.get("/items")
def list_items() -> List[dict]:
    """Return all stored items."""
    return [{"id": k, **v.model_dump()} for k, v in items.items()]


@app.delete("/remove/{item_id}")
def remove(item_id: int) -> dict:
    """Delete and return an item by identifier."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"deleted": item_id, "developer": "Dev1"}
