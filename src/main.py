# main.py
from producto import Producto
from carrito import Carrito

carrito = Carrito()
laptop = Producto('001', 'Laptop', 300000, 120)

carrito.agregar_producto(laptop)
print(carrito.obtener_items())
carrito.agregar_producto(laptop)
print(carrito.obtener_items())