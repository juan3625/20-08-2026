import pytest

from app.calculators import (calculate_subtotal, calculate_discount, calculate_total)
from pytest import raises

def test_calculate_subtotal_multiplies_price_by_quantity():

    # Arrange
    unit_price = 25000
    quantity = 3

    # Act
    subtotal = calculate_subtotal(unit_price, quantity)

    # Assert
    assert subtotal == 75000

def test_calculate_discount_returns_ten_percent():

    # Arrange
    subtotal = 100000
    discount_percentage = 10

    # Act
    discount = calculate_discount(subtotal, discount_percentage)

    # Assert
    assert discount == 10000

def test_calculate_total_with_discount():

    total  = calculate_total(unit_price=30000, quantity=2)

    assert total == 60000

def  test_calculate_total_with_twenty_percent_discount():

    total = calculate_total(unit_price=50000, quantity=2, discount_percentage=20)

    assert total == 80000

def test_calculate_subtotal_rejects_negative_unit_price():
    with pytest.raises(ValueError, match="Unit price cannot be negative."):
        calculate_subtotal(unit_price=-100, quantity=1)

def test_calculate_subtotal_returns_message_for_negative_unit_price():
    with pytest.raises(ValueError, match="Unit price cannot be negative."):
        calculate_subtotal(unit_price=-10000, quantity=0)

def test_calculate_subtotal_rejects_zero_quantity():
    with pytest.raises(ValueError) as exc_info:
        calculate_subtotal(unit_price=100, quantity=0)

    assert str(exc_info.value) == "Quantity cannot be zero or negative."

    print(exc_info.value)  



def test_calculate_discount_accepts_zero_percent():
    discount = calculate_discount(subtotal=100000, discount_percentage=0)

    assert discount == 0
   

def test_calculate_discount_accepts_one_hundred_percent ():
    discount = calculate_discount(subtotal=100000, discount_percentage=100)

    assert discount == 100000

def test_calculate_discount_rejects_percentage_below_zero ():
    with pytest.raises(ValueError):
        calculate_discount(subtotal=100000, discount_percentage=-10)




