import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

image = plt.imread("crayons_mosaic.bmp").astype(np.float32)

#
# show the original color image
#

color_image = np.zeros(image.shape + (3,))
color_image[ ::2, ::2, 0] = image[::2,::2] # red pixels
color_image[ ::2,1::2, 1] = image[::2,1::2] # green pixels
color_image[1::2, ::2, 1] = image[1::2,::2] # green pixels
color_image[1::2,1::2, 2] = image[1::2,1::2] # blue pixels

def average(image, positions):
	assert len(positions) > 0
	return sum(image[p[0], p[1]] for p in positions) / len(positions)

def interp2(image, row, col):
	'''Does a 2-interpolation'''
	height, width = image.shape
	neighbors = None
	hor_nbrs = list(filter(lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < height and p[1] < width, [(row, col+1), (row, col-1)]))
	ver_nbrs = list(filter(lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < height and p[1] < width, [(row+1, col), (row-1, col)]))
	return average(image, hor_nbrs), average(image, ver_nbrs)

def interp4(image, row, col, diag):
	'''Does a 4-interpolation, either diagonally or horizontally/vertically'''
	height, width = image.shape
	neighbors = None
	if diag:
		neighbors = [(row + dr, col + dc) for dr in [-1,1] for dc in [-1,1]]
	else:
		neighbors = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]
	neighbors = list(filter(lambda p: p[0] >= 0 and p[1] >= 0 and p[0] < height and p[1] < width, neighbors))
	return average(image, neighbors)

def demosaic(image):
	height, width = image.shape
	output = np.zeros(image.shape + (3,))
	# Fill in green and red values at the blue spots
	for row in range(1, height, 2):
		for col in range(1, width, 2):
			output[row, col, 0] = interp4(image, row, col, True)
			output[row, col, 1] = interp4(image, row, col, False)
	# Fill in green and blue values at the red spots
	for row in range(0, height, 2):
		for col in range(0, width, 2):
			output[row, col, 1] = interp4(image, row, col, False)
			output[row, col, 2] = interp4(image, row, col, True)
	# Fill in red and blue values at the green spots
	for row in range(0, height, 2):
		for col in range(1, width, 2):
			output[row, col, 0], output[row, col, 2] = interp2(image, row, col)
	for row in range(1, height, 2):
		for col in range(0, width, 2):
			output[row, col, 2], output[row, col, 0] = interp2(image, row, col)
	return output

def compute_error_map(reference, demosaiced):
	'''Sum of squared error across three channels'''
	height, width, _ = reference.shape
	output = np.zeros(reference.shape)
	for row in range(height):
		for col in range(width):
			a = reference[row, col]
			b = demosaiced[row, col]
			output[row, col] = sum((a - b) ** 2)
	return output

demosaiced = demosaic(image)
reference = plt.imread("crayons.jpg").astype(np.uint8)
error_map = compute_error_map(reference, demosaiced)

error_map = np.log(error_map)
# print(error_map)

fig, ax = plt.subplots()
ax.set_title("Demosaiced image")
ax.imshow(demosaiced.astype(np.uint8), interpolation="nearest")
plt.savefig('demosaiced.jpg')

fig, ax = plt.subplots()
ax.set_title("Error map")
cax = ax.imshow(error_map, interpolation="nearest", cmap=cm.afmhot)
# plt.colorbar(cax, orientation='horizontal')
# fig.colorbar(cax)
# cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])

max_err = np.max(np.max(error_map))

total_err = np.sum(np.sum(error_map))
avg_err = total_err / (len(error_map) * len(error_map[0]))

print(max_err, avg_err)

plt.show()
