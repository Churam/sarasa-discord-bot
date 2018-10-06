from PIL import Image, ImageFont, ImageDraw

canvas_size = (600,600)
canvas = Image.new("RGBA",canvas_size)

draw = ImageDraw.Draw(canvas, mode="RGBA")

draw.rectangle((0,0,canvas_size),fill='black')
draw.ellipse((0, 0, canvas_size), fill = 'white')
draw.ellipse(((canvas_size[0]-300)/2, (canvas_size[1]-300)/2, 500,500),fill='black')
canvas.thumbnail((150,150),Image.ANTIALIAS)
canvas.save('circle.png')