"""End-to-end smoke tests for all portals.

This script assumes the Flask backend is already running on
http://127.0.0.1:5001 (see backend/app.py).

It will:
- Ensure one user exists for each role: farmer, buyer, vendor, labor, admin
- Test registration (or fallback to login if already registered)
- Test key flows:
  * Farmer: create crop listing and labor posting
  * Buyer: browse marketplace and place crop order
  * Vendor: add a product
  * Labor: view job postings and apply to one
  * Admin: list users and fetch analytics

Run with the virtualenv active, from backend/:
    source ../venv/bin/activate
    python test_portals_e2e.py
"""
import os
import sys
from typing import Dict, Tuple

import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:5001")


def _request(method: str, path: str, token: str | None = None, **kwargs) -> requests.Response:
    url = f"{BASE_URL}{path}"
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if "json" in kwargs:
        headers.setdefault("Content-Type", "application/json")
    resp = requests.request(method, url, headers=headers, timeout=15, **kwargs)
    return resp


def register_or_login(email: str, password: str, full_name: str, role: str, extra: Dict | None = None) -> Tuple[str, Dict]:
    """Register a user; if email already exists, just login.

    Returns (token, user_dict).
    """
    payload: Dict = {
        "email": email,
        "password": password,
        "full_name": full_name,
        "role": role,
    }
    if extra:
        payload.update(extra)

    # Try register
    r = _request("POST", "/api/auth/register", json=payload)
    if r.status_code == 201:
        data = r.json()
        print(f"[OK] Registered {role} {email}")
        return data["token"], data["user"]

    data = r.json()
    if r.status_code == 400 and data.get("error") == "Email already registered":
        # Fallback to login
        r2 = _request("POST", "/api/auth/login", json={"email": email, "password": password})
        r2.raise_for_status()
        d2 = r2.json()
        print(f"[OK] Logged in existing {role} {email}")
        return d2["token"], d2["user"]

    print(f"[FAIL] Register {role} {email}: {r.status_code} {data}")
    r.raise_for_status()
    raise SystemExit(1)


def admin_login() -> str:
    r = _request(
        "POST",
        "/api/auth/login",
        json={"email": "admin@smartfarming.com", "password": "admin123"},
    )
    r.raise_for_status()
    data = r.json()
    print("[OK] Admin login")
    return data["token"]


def test_farmer_flow(token: str) -> int:
    """Farmer: create crop listing and labor posting.

    Returns created crop listing id.
    """
    # Profile check
    r = _request("GET", "/api/auth/profile", token=token)
    r.raise_for_status()
    print("[OK] Farmer profile")

    # Create crop listing
    listing_payload = {
        "crop_name": "Test Rice",
        "category": "grains",
        "quantity": 1000,
        "unit": "kg",
        "price_per_unit": 25,
        "description": "High quality test rice",
        "harvest_date": "2026-02-01",
    }
    r = _request("POST", "/api/farmer/crop-listings", token=token, json=listing_payload)
    r.raise_for_status()
    listing = r.json()["listing"]
    listing_id = listing["id"]
    print(f"[OK] Farmer created crop listing id={listing_id}")

    # Create labor posting
    labor_payload = {
        "job_title": "Harvest workers",
        "description": "Need help with harvest",
        "work_type": "harvesting",
        "start_date": "2026-02-10",
        "end_date": "2026-02-12",
        "wage_per_day": 500,
        "total_wage": 3000,
        "location": "Test Farm Location",
        "laborers_needed": 2,
    }
    r = _request("POST", "/api/farmer/labor-postings", token=token, json=labor_payload)
    r.raise_for_status()
    posting_id = r.json()["posting_id"]
    print(f"[OK] Farmer created labor posting id={posting_id}")

    return listing_id


def test_buyer_flow(token: str, listing_id: int) -> None:
    # Marketplace browse
    r = _request("GET", "/api/buyer/marketplace", token=token)
    r.raise_for_status()
    data = r.json()
    print(f"[OK] Buyer marketplace: {len(data.get('crops', []))} crops, {len(data.get('products', []))} products")

    # Place crop order
    order_payload = {
        "order_type": "crop",
        "crop_listing_id": listing_id,
        "quantity": 100,
        "unit_price": 25,
        "is_contract_farming": False,
        "delivery_date": "2026-02-15",
        "delivery_address": "123 Main St, Test City",
        "notes": "Test order via script",
    }
    r = _request("POST", "/api/buyer/orders", token=token, json=order_payload)
    r.raise_for_status()
    order_id = r.json()["order_id"]
    print(f"[OK] Buyer placed order id={order_id}")


def test_vendor_flow(token: str) -> None:
    product_payload = {
        "product_name": "Organic Fertilizer - Test",
        "category": "fertilizers",
        "brand": "GreenGrow",
        "quantity_available": 500,
        "unit": "kg",
        "price_per_unit": 50,
        "description": "Test fertilizer product",
        "specifications": "NPK 10:20:10",
    }
    r = _request("POST", "/api/vendor/products", token=token, json=product_payload)
    r.raise_for_status()
    product_id = r.json()["product"]["id"]
    print(f"[OK] Vendor added product id={product_id}")


def test_labor_flow(token: str) -> None:
    # View postings
    r = _request("GET", "/api/labor/job-postings", token=token)
    r.raise_for_status()
    postings = r.json().get("postings", [])
    print(f"[OK] Labor sees {len(postings)} job postings")
    if not postings:
        print("[WARN] No postings available to apply to")
        return

    posting_id = postings[0]["id"]
    r = _request("POST", f"/api/labor/apply/{posting_id}", token=token)
    r.raise_for_status()
    print(f"[OK] Labor applied to posting id={posting_id}")


def test_admin_flow(token: str) -> None:
    r = _request("GET", "/api/admin/users", token=token)
    r.raise_for_status()
    users = r.json().get("users", [])
    print(f"[OK] Admin fetched {len(users)} users")

    r = _request("GET", "/api/admin/analytics", token=token)
    r.raise_for_status()
    print("[OK] Admin analytics fetched")


def main() -> None:
    print(f"Using BASE_URL={BASE_URL}")

    # Create/login users for each role
    farmer_token, _ = register_or_login(
        email="farmer.portal@test.local",
        password="pass1234",
        full_name="Farmer Portal User",
        role="farmer",
        extra={
            "phone": "1111111111",
            "farm_name": "Test Farm",
        },
    )

    buyer_token, _ = register_or_login(
        email="buyer.portal@test.local",
        password="pass1234",
        full_name="Buyer Portal User",
        role="buyer",
        extra={"phone": "2222222222"},
    )

    vendor_token, _ = register_or_login(
        email="vendor.portal@test.local",
        password="pass1234",
        full_name="Vendor Portal User",
        role="vendor",
        extra={
            "phone": "3333333333",
            "business_name": "Test Vendor Biz",
        },
    )

    labor_token, _ = register_or_login(
        email="labor.portal@test.local",
        password="pass1234",
        full_name="Labor Portal User",
        role="labor",
        extra={
            "phone": "4444444444",
            "skills": "Planting, Harvesting",
            "daily_wage": 500,
        },
    )

    admin_token = admin_login()

    # Portal-specific flows
    listing_id = test_farmer_flow(farmer_token)
    test_buyer_flow(buyer_token, listing_id)
    test_vendor_flow(vendor_token)
    test_labor_flow(labor_token)
    test_admin_flow(admin_token)

    print("\nAll portal smoke tests completed.")


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as exc:
        print(f"[ERROR] HTTP error: {exc}")
        sys.exit(1)
