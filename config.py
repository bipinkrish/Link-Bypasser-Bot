Vars = [
	# Bot API Token
	"",
	# GdToT Crypt
	"",
	# Laravel Session
	"",
	# XSRF_TOKEN 
	""
]

if not Vars[0]:
	raise ValueError("Bot API Token cannot be empty!")
elif not Vars[1]:
	Vars.insert(1,'b0lDek5LSCt6ZjVRR2EwZnY4T1EvVndqeDRtbCtTWmMwcGNuKy8wYWpDaz0%3D')
else:
	pass
