def map_range( val, min1, max1, min2, max2 ):
    return (val-min1)/(max1-min1) * (max2-min2) + min2

def to_grayscale( rgb, steps = 3.0 ):

    r, g, b = rgb

    value = float( r + g + b ) / 3.0
    value = map_range( value, 0.0, 255.0, 0.0, steps )

    return int( round( value ) )
