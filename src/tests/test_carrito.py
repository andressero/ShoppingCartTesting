import pytest

from carrito import Carrito
from producto import Producto

@pytest.fixture
def carrito():
    return Carrito()

@pytest.fixture
def laptop():
    return Producto('001', 'Laptop', 300000, 120)

@pytest.fixture
def teclado():
    return Producto('002', 'Teclado', 5000, 0)

# R1

def test_producto_nuevo_agregado(carrito, laptop):
    carrito.agregar_producto(laptop)
    assert laptop.id in carrito.obtener_items()

def test_producto_agregado_incrementa_cantidad(carrito, laptop):
    carrito.agregar_producto(laptop)
    carrito.agregar_producto(laptop)
    items = carrito.obtener_items()
    assert items[laptop.id].cantidad == 2

def test_carrito_vacio(carrito):
    assert carrito.esta_vacio()

def test_carrito_deja_de_estar_vacio(carrito, laptop):
    carrito.agregar_producto(laptop)
    assert not carrito.esta_vacio()

def test_error_cantidad_cero(carrito, laptop):
    with pytest.raises(ValueError):
        carrito.agregar_producto(laptop, 0)
