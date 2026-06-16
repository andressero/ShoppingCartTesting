from dataclasses import dataclass
from producto import Producto

@dataclass
class ItemCarrito:
    producto: Producto
    cantidad: int

    @property
    def subtotal(self) -> float:
        return self.producto.precio * self.cantidad