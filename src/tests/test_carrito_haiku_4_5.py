"""
Creame un archivo de pruebas para carrito.py usando pytest. Crea pruebas que cubran el requisito R1
"""

import pytest

from carrito import Carrito
from producto import Producto
from excepciones import StockInsuficienteError


def test_agregar_producto_nuevo_crea_item_en_carrito():
    carrito = Carrito()
    producto = Producto(id="p1", nombre="Camisa", precio=20.0, stock=10)

    carrito.agregar_producto(producto, cantidad=2)

    items = carrito.obtener_items()
    assert "p1" in items
    assert items["p1"].cantidad == 2
    assert items["p1"].producto is producto


def test_agregar_producto_existente_incrementa_cantidad():
    carrito = Carrito()
    producto = Producto(id="p1", nombre="Camisa", precio=20.0, stock=10)

    carrito.agregar_producto(producto, cantidad=2)
    carrito.agregar_producto(producto, cantidad=3)

    items = carrito.obtener_items()
    assert items["p1"].cantidad == 5
    assert carrito.total_bruto() == pytest.approx(100.0)


def test_agregar_producto_multiple_productos_mantiene_cantidades_separadas():
    carrito = Carrito()
    camisa = Producto(id="p1", nombre="Camisa", precio=20.0, stock=10)
    pantalon = Producto(id="p2", nombre="Pantalón", precio=40.0, stock=5)

    carrito.agregar_producto(camisa, cantidad=1)
    carrito.agregar_producto(pantalon, cantidad=2)
    carrito.agregar_producto(camisa, cantidad=1)

    items = carrito.obtener_items()
    assert items["p1"].cantidad == 2
    assert items["p2"].cantidad == 2
    assert carrito.total_bruto() == pytest.approx(120.0)


def test_agregar_producto_incremento_no_supera_stock_disponible():
    carrito = Carrito()
    producto = Producto(id="p1", nombre="Camisa", precio=20.0, stock=4)

    carrito.agregar_producto(producto, cantidad=2)
    carrito.agregar_producto(producto, cantidad=2)

    assert carrito.obtener_items()["p1"].cantidad == 4


def test_agregar_producto_incremento_supera_stock_lanza_error():
    carrito = Carrito()
    producto = Producto(id="p1", nombre="Camisa", precio=20.0, stock=4)

    carrito.agregar_producto(producto, cantidad=3)

    with pytest.raises(StockInsuficienteError):
        carrito.agregar_producto(producto, cantidad=2)
