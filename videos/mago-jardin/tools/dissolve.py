"""Block-dissolve frames: k4.jpg revealed tile by tile (16-bit style screen transition)."""
import sys, numpy as np
from PIL import Image
A = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
k4 = Image.open(f'{A}/k4.jpg').convert('RGBA'); W, H = k4.size; T = 60
cols, rows = W // T, -(-H // T)
rng = np.random.default_rng(11)
# ordered dither-like reveal: random rank biased from the centre outwards
cy, cx = np.mgrid[0:rows, 0:cols]
rank = rng.random((rows, cols)) * 0.7 + 0.3 * (np.hypot(cx - cols/2, (cy - rows/2) * 0.6) / np.hypot(cols/2, rows*0.3))
order = rank.argsort(axis=None).argsort().reshape(rows, cols) / (rows*cols)
for i in range(1, N):
    a = np.zeros((H, W), np.uint8)
    on = order < i / N
    a[:] = np.kron(on, np.ones((T, T), bool))[:H, :W] * 255
    im = k4.copy(); im.putalpha(Image.fromarray(a)); im.save(f'{A}/dis{i}.png', optimize=True)
print('ok')
