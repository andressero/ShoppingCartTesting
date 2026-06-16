"""
Tengo una clase de Python que simula la funcionalidad de un carrito de compras. Y tengo estos requerimientos:

Requisitos:
    R1: Agregar producto al carrito; si ya existe, incrementar cantidad.
    R2: No se puede agregar más unidades de las disponibles en stock.
    R3: Descuento del 10% si el total supera $100.
    R4: Descuento del 20% si el usuario tiene membresía premium.
    R5: No se pueden aplicar ambos descuentos simultáneamente; prevalece el mayor.
    R6: Eliminar producto; si cantidad llega a 0, removerlo del carrito.
    R7: El carrito expira si pasan 30 minutos sin actividad.

Crea casos de prueba para el requisito R1, usando pytest. Te paso los archivos relevantes:
producto.py, item_carrito.py, excepciones.py, config.py, carrito.py

"""

import pytest
from carrito import Carrito
from producto import Producto
from excepciones import StockInsuficienteError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def producto_basico():
    """Producto con stock suficiente para la mayoría de los tests."""
    return Producto(id="P01", nombre="Laptop", precio=500.0, stock=10)


@pytest.fixture
def producto_secundario():
    return Producto(id="P02", nombre="Mouse", precio=25.0, stock=5)


@pytest.fixture
def carrito():
    return Carrito()


# ---------------------------------------------------------------------------
# R1-A: Agregar un producto nuevo al carrito
# ---------------------------------------------------------------------------

class TestAgregarProductoNuevo:

    def test_agregar_producto_aparece_en_items(self, carrito, producto_basico):
        """Un producto agregado debe estar presente en el carrito."""
        carrito.agregar_producto(producto_basico, cantidad=1)
        assert producto_basico.id in carrito.obtener_items()

    def test_agregar_producto_cantidad_correcta(self, carrito, producto_basico):
        """La cantidad registrada debe coincidir con la solicitada."""
        carrito.agregar_producto(producto_basico, cantidad=3)
        assert carrito.obtener_items()[producto_basico.id].cantidad == 3

    def test_agregar_producto_sin_especificar_cantidad_usa_1(self, carrito, producto_basico):
        """La cantidad por defecto debe ser 1."""
        carrito.agregar_producto(producto_basico)
        assert carrito.obtener_items()[producto_basico.id].cantidad == 1

    def test_agregar_producto_carrito_deja_de_estar_vacio(self, carrito, producto_basico):
        """El carrito debe reportar que no está vacío tras agregar un ítem."""
        assert carrito.esta_vacio()
        carrito.agregar_producto(producto_basico)
        assert not carrito.esta_vacio()

    def test_agregar_varios_productos_distintos(self, carrito, producto_basico, producto_secundario):
        """Se pueden agregar productos diferentes en el mismo carrito."""
        carrito.agregar_producto(producto_basico)
        carrito.agregar_producto(producto_secundario)
        items = carrito.obtener_items()
        assert producto_basico.id in items
        assert producto_secundario.id in items

    def test_agregar_producto_referencia_correcta(self, carrito, producto_basico):
        """El ítem en el carrito debe referenciar el producto correcto."""
        carrito.agregar_producto(producto_basico)
        item = carrito.obtener_items()[producto_basico.id]
        assert item.producto is producto_basico


# ---------------------------------------------------------------------------
# R1-B: Agregar un producto que ya existe incrementa la cantidad
# ---------------------------------------------------------------------------

class TestIncrementarCantidadProductoExistente:

    def test_segunda_adicion_acumula_cantidad(self, carrito, producto_basico):
        """Agregar el mismo producto dos veces debe sumar las cantidades."""
        carrito.agregar_producto(producto_basico, cantidad=2)
        carrito.agregar_producto(producto_basico, cantidad=3)
        assert carrito.obtener_items()[producto_basico.id].cantidad == 5

    def test_multiples_adiciones_acumulan_correctamente(self, carrito, producto_basico):
        """Varias adiciones sucesivas deben acumularse."""
        for _ in range(4):
            carrito.agregar_producto(producto_basico, cantidad=1)
        assert carrito.obtener_items()[producto_basico.id].cantidad == 4

    def test_no_se_duplica_el_id_en_items(self, carrito, producto_basico):
        """Agregar el mismo producto no debe crear entradas duplicadas."""
        carrito.agregar_producto(producto_basico, cantidad=1)
        carrito.agregar_producto(producto_basico, cantidad=2)
        assert len(carrito.obtener_items()) == 1

    def test_productos_distintos_no_se_mezclan(self, carrito, producto_basico, producto_secundario):
        """Agregar P02 no debe alterar la cantidad de P01."""
        carrito.agregar_producto(producto_basico, cantidad=2)
        carrito.agregar_producto(producto_secundario, cantidad=3)
        carrito.agregar_producto(producto_basico, cantidad=1)
        assert carrito.obtener_items()[producto_basico.id].cantidad == 3
        assert carrito.obtener_items()[producto_secundario.id].cantidad == 3


# ---------------------------------------------------------------------------
# R1-C: Validaciones de entrada
# ---------------------------------------------------------------------------

class TestValidacionesEntrada:

    def test_cantidad_cero_lanza_value_error(self, carrito, producto_basico):
        """Agregar con cantidad 0 debe lanzar ValueError."""
        with pytest.raises(ValueError):
            carrito.agregar_producto(producto_basico, cantidad=0)

    def test_cantidad_negativa_lanza_value_error(self, carrito, producto_basico):
        """Agregar con cantidad negativa debe lanzar ValueError."""
        with pytest.raises(ValueError):
            carrito.agregar_producto(producto_basico, cantidad=-5)

    def test_cantidad_cero_no_modifica_carrito(self, carrito, producto_basico):
        """Un intento fallido no debe alterar el estado del carrito."""
        with pytest.raises(ValueError):
            carrito.agregar_producto(producto_basico, cantidad=0)
        assert carrito.esta_vacio()


# ---------------------------------------------------------------------------
# R1-D: Límite de stock (frontera entre R1 y R2, incluido para completitud)
# ---------------------------------------------------------------------------

class TestLimiteStock:

    def test_agregar_exactamente_el_stock_disponible(self, carrito, producto_basico):
        """Agregar exactamente el stock disponible debe funcionar sin error."""
        carrito.agregar_producto(producto_basico, cantidad=producto_basico.stock)
        assert carrito.obtener_items()[producto_basico.id].cantidad == producto_basico.stock

    def test_agregar_mas_del_stock_lanza_stock_insuficiente(self, carrito, producto_basico):
        """Superar el stock debe lanzar StockInsuficienteError."""
        with pytest.raises(StockInsuficienteError):
            carrito.agregar_producto(producto_basico, cantidad=producto_basico.stock + 1)

    def test_acumulado_que_supera_stock_lanza_error(self, carrito, producto_basico):
        """La suma de adiciones no debe superar el stock disponible."""
        carrito.agregar_producto(producto_basico, cantidad=8)
        with pytest.raises(StockInsuficienteError):
            carrito.agregar_producto(producto_basico, cantidad=5)  # 8 + 5 = 13 > 10