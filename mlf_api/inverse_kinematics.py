import numpy as np

def inverse_kinematics(X=150,Y=0,Z=60, eff_off_x=65, eff_off_z=0):

    link_lengths = [55, 39, 135, 147, 66.3]
    offset_z = 100
    zb = Z - offset_z + eff_off_z
    l1 = link_lengths[2]
    l2 = link_lengths[3]
    
    q0 = np.arctan2(Y,X)

    if np.abs(Y)<1e-2:
        xo = X-eff_off_x
    else:
        xo = np.sqrt((X-eff_off_x*np.cos(q0))**2 + (Y-eff_off_x*np.sin(q0))**2)

    q1 = np.pi - np.arctan2(zb,xo) - np.arccos((xo**2 + zb**2 + l1**2-l2**2)/(2*l1*np.sqrt(xo**2 + zb**2)))
    q2 = np.pi/2 - q1 + np.arccos((l1**2+l2**2-xo**2-zb**2)/(2*l1*l2))

    #to deg
    q0 = -2*np.round(np.rad2deg(q0),0)+90
    q1 = np.round(np.rad2deg(q1),0)
    q2 = np.round(np.rad2deg(q2),0)
    return np.array([q0,q1,q2])
