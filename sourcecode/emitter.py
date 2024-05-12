import physics

def generate():
    #obj_quantity = random.randint(1, 5)
    for i in range(physics.obj_quantity):
        position_choice = [0.0, 30, 0.0]  
        physics.obj.append(physics.Create_Sphere(position_choice, [0.0, 0.0, 0.0]))
