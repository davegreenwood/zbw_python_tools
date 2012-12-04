# Here's how it goes . . .
# choose a vert (for example)
# get the uv position of that vert
# create a soft mod there

# create a control at the position of the softmod
# connect the pos, rot, scale of the control to the softModHandle
# create an attr on the control for the falloff (and the envelope)
# connect that attr to the softmod falloff radius
# softmod NOT relative
# inherit transforms on softModHandle are "off"

# maybe . . .
# create secondary control under control
# this will drive falloff center attr of the softmod (connect attrs from translate)