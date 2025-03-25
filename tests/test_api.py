import pytest
from datetime import datetime



@pytest.mark.asyncio
@pytest.mark.parametrize("limit, expected_length, expected_status", [
    (1, 1, 200),
    (0, 0, 422),
    (-1, 0, 422),
    ("abc", 0, 422)
])
async def test_get_last_trading_dates(async_client, limit, expected_length, expected_status):
    response = await async_client.get(f"/get_last_trading_dates?limit={limit}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert len(response.json()) == expected_length
        

@pytest.mark.asyncio
@pytest.mark.parametrize("params, expected_status", [
    (
        {
            "oil_id": "A100",
            "delivery_type_id": "F",
            "delivery_basis_id": "NVY",
            "start_date": "04.03.2025",
            "end_date": "03.03.2025"
        },
        200,
    ),
    (
        {
            "oil_id": "A1000",
            "delivery_type_id": "F",
            "delivery_basis_id": "NVY",
            "start_date": "04.03.2025",
            "end_date": "03.03.2025"
        },
        422,
    ),
    (
        {
            "delivery_type_id": "F",
            "delivery_basis_id": "NVY",
            "start_date": "2025.03.04",
            "end_date": "03.03.2025"
        },
        422,
    ),
])
async def test_get_dynamics(
    async_client,
    params,
    expected_status, 
):
    response = await async_client.get("/get_dynamics", params=params)
    assert response.status_code == expected_status
    if expected_status == 200:
        results = response.json()
        for result in results:
            assert result["oil_id"] == params["oil_id"]
            assert result["delivery_type_id"] == params["delivery_type_id"]
            assert result["delivery_basis_id"] == params["delivery_basis_id"]
            assert (datetime.strptime(result["date"],"%d.%m.%Y").date() <= 
                    datetime.strptime(params["start_date"],"%d.%m.%Y").date())
            assert (datetime.strptime(result["date"],"%d.%m.%Y").date() >= 
                    datetime.strptime(params["end_date"],"%d.%m.%Y").date())
            


@pytest.mark.asyncio
@pytest.mark.parametrize("params, expected_status", [
    (
        {
            "oil_id": "A100",
            "delivery_type_id": "F",
            "delivery_basis_id": "NVY",
        },
        200,
    ),
    (
        {
            "oil_id": "A1000",
            "delivery_type_id": "F",
            "delivery_basis_id": "NVY",
        },
        422,
    ),
    (
        {
            "delivery_type_id": "F",
            "delivery_basis_id": "NVY",
        },
        422,
    ),
])
async def test_get_trading_results(
    async_client,
    params,
    expected_status, 
):
    response = await async_client.get("/get_trading_results", params=params)
    assert response.status_code == expected_status
    if expected_status == 200:
        results = response.json()
        for result in results:
            assert result["oil_id"] == params["oil_id"]
            assert result["delivery_type_id"] == params["delivery_type_id"]
            assert result["delivery_basis_id"] == params["delivery_basis_id"]
            






