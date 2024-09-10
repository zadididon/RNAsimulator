import torch
import matplotlib.pyplot as plt

def generate_fake_cell_image(img_size=64, num_spots=30, min_cells=1, max_cells=4, cell_radius_range=(5, 20), spot_brightness=1.0, spot_size=2, noise_probability = 0.5):
   
    image = torch.zeros((1, img_size, img_size)) 

    num_cells = torch.randint(min_cells, max_cells + 1, (1,))  

    cells = [] #add ?dictionary? to have different cell types

    is_noise_image = torch.rand(1) < noise_probability

    for cell in range(num_cells):
        
        placement_x = torch.randint(cell_radius_range[1], (1,))  
        placement_y = torch.randint(cell_radius_range[1], (1,))
        cell_radius = torch.randint (cell_radius_range[0], cell_radius_range[1], (1,))
        

        cells.append((placement_x, placement_y, cell_radius))
        
        
        for x in range(img_size):
            for y in range(img_size):
                distance = ((x - placement_x) ** 2 + (y - placement_y) ** 2) ** 0.5
                if distance < cell_radius:
                    image[0, x, y] = 0.2 + 0.3 * (1 - distance / cell_radius)  

                    
    for RNAspot in range(num_spots):
        place_inside_cell = torch.rand(1) < 0.5  
        
        if place_inside_cell:
        
            cell_idx = torch.randint(0, len(cells), (1,))
            placement_y, placement_y, cell_radius = cells[cell_idx]
       
            spot_x = torch.normal(mean=float(placement_x), std=float(cell_radius / 3), size=())
            spot_y = torch.normal(mean=float(placement_y), std=float(cell_radius / 3), size=())

        
            spot_x = int(min(max(spot_x, 0), img_size - 1))
            spot_y = int(min(max(spot_y, 0), img_size - 1))

        else:
            spot_x = torch.randint(0, img_size, (1,))
            spot_y = torch.randint(0, img_size, (1,))
        
        
        for i in range(-spot_size, spot_size + 1):
            for j in range(-spot_size, spot_size + 1):
                if 0 <= spot_x + i < img_size and 0 <= spot_y + j < img_size:
                    distance = (i ** 2 + j ** 2) ** 0.5
                    if distance <= spot_size:
                        image[0, spot_x + i, spot_y + j] += spot_brightness * (1 - distance / spot_size)



    return image


simulated_image = generate_fake_cell_image(img_size=64, num_spots=50, spot_brightness=1.0, spot_size=3, noise_probability=0.5)

plt.imshow(simulated_image.squeeze())
plt.title("Cell with RNA Clusters")
plt.show()



