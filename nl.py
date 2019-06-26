import pyNetLogo
import jpype

'''
netlogo = pyNetLogo.NetLogoLink( gui = True ) #Show NetLogo GUI
netlogo.load_model('test.nlogo')
# netlogo.command('setup')
'''

netlogo = pyNetLogo . NetLogoLink ( gui = True ) #Show NetLogo GUI
netlogo.load_model(r'test.nlogo')
netlogo.command('setup')