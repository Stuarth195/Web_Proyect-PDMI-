root = tk.Toplevel()
recipe_manager = RecipeManager(
    parent=root,
    product_file="M_A.txt",
    pe_file="PE.txt",
    cosecha_file="COSECHA.txt",
    recipe_file="receta.txt",
    code="CHP-001",  # O None si es para editar
    description="Chips de papa (Paquete de 200g)"  # Solo si es para una nueva receta
)
root.mainloop()
