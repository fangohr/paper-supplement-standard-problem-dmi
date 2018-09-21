import subprocess

# discr = [(183, 150),
#          (182, 200),
#          (182.5, 250),
#          (184.25, 275),
#          (181, 100),
#          (180.5, 50),
#          ]
discr = [(186, 300)]

for L, dxy in discr:

    subprocess.call(('oommf '
                     ' boxsi -threads 6 '
                     '-parameters '
                     '"'
                     'L {0}e-9 '
                     'dxy {1}e-11 '
                     'BASENAME '
                     '3D_skyrmion_d{1}e-2nm'
                     '" '
                     'oommf_3D_bulkDMI_cylinder.mif').format(L, dxy),
                    shell=True)
