**Try 1**
1x Conv2D, 32 + MaxPooling2D layer
Dense 128
**Result 1**
1s loss: 0.7121, accuracy: 0.8150

**Try 2**
2x Conv2D, 32 + MaxPooling2D layer
Dense 128
**Result 2**
1s loss: 0.0687, accuracy: 0.9283
*Great improvement, a same time for training.*

**Try 3**
2x Conv2D, 32 + MaxPooling2D layer
Dense 256
**Result 3**
1s loss: 0.0587, accuracy: 0.9865
*Small improvement, a bit more time for training.*

**Try 4**
2x Conv2D, 64 + MaxPooling2D layer
Dense 256
**Result 4**
2s loss: 0.0540, accuracy: 0.9886
*Not so big improvement, but a lot of time for training.*

**Try 5**
3x Conv2D, 32 + MaxPooling2D layer
Dense 128
**Result 5**
2s loss: 0.1100, accuracy: 0.9699
*Good result, a little time on training.*

***FINAL***
**Try 6**
3x Conv2D, 32 + MaxPooling2D layer
Dense 256
**Result 6**
1s loss: 0.0730, accuracy: 0.9787
*A bit better result, a little time on training.*

