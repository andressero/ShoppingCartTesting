from typing import Dict

from producto import Producto
from item_carrito import ItemCarrito
from excepciones import StockInsuficienteError, ProductoNoEncontradoError
from config import UMBRAL_DESCUENTO_TOTAL, DESCUENTO_POR_TOTAL, DESCUENTO_PREMIUM

class Carrito:
    def __init__(self, es_premium: bool = False):
        self.es_premium: bool = es_premium
        self._items: Dict[str, ItemCarrito] = {}

    # ------------------------------------------------------------------
    # Agregar y eliminar productos
    # ------------------------------------------------------------------

    def agregar_producto(self, producto: Producto, cantidad: int = 1) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        cantidad_actual = self._items[producto.id].cantidad if producto.id in self._items else 0
        cantidad_total = cantidad_actual + cantidad

        if cantidad_total > producto.stock:  
            raise StockInsuficienteError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, solicitado: {cantidad_total}."
            )

        if producto.id in self._items:
            self._items[producto.id].cantidad += cantidad
        else:
            self._items[producto.id] = ItemCarrito(producto=producto, cantidad=cantidad)

    def eliminar_producto(self, producto_id: str, cantidad: int = 1) -> None:
        if producto_id not in self._items:
            raise ProductoNoEncontradoError(
                f"El producto '{producto_id}' no está en el carrito."
            )

        if cantidad <= 0:
            raise ValueError("La cantidad a eliminar debe ser mayor a cero.")

        item = self._items[producto_id]

        if cantidad >= item.cantidad:
            del self._items[producto_id]
        else:
            item.cantidad -= cantidad

    # ------------------------------------------------------------------
    # Totales y descuentos
    # ------------------------------------------------------------------

    def descuento_aplicable(self) -> float:
        bruto = self.total_bruto()
        descuento_total = DESCUENTO_POR_TOTAL if bruto > UMBRAL_DESCUENTO_TOTAL else 0.0 
        descuento_membresia = DESCUENTO_PREMIUM if self.es_premium else 0.0               
        return max(descuento_total, descuento_membresia)                                  

    """Total con el descuento aplicado."""
    def total_final(self) -> float:
        bruto = self.total_bruto()
        return bruto * (1 - self.descuento_aplicable())
    
    def total_bruto(self) -> float:
        return sum(item.subtotal for item in self._items.values())

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def obtener_items(self) -> Dict[str, ItemCarrito]:
        return dict(self._items)

    def esta_vacio(self) -> bool:
        return len(self._items) == 0
