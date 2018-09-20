import textwrap
import subprocess

discr = [(183, 150),
         (182, 200),
         (182.5, 250),
         (184.25, 275),
         (186, 300),
         (181, 100),
         (180.5, 50),
         ]

for L, dxy in discr:

    lx, ly, lz = L, L, 22
    dx, dy, dz = dxy * 0.01, dxy * 0.01, 1
    nx, ny, nz = int(lx // dx), int(ly // dy), int(lz // dz)

    sim = textwrap.dedent("""\
    lx := {}e-9
    ly := {}e-9
    lz := {}e-9

    dx := {}e-9
    dy := {}e-9
    dz := {}e-9

    nx := {}
    ny := {}
    nz := {}

    SetGridSize(nx, ny, nz)
    SetCellSize(dx, dy, dz)

    // Define the cylinder
    SetGeom(Circle(180e-9))

    Msat         = 0.384e6
    Aex          = 8.78e-12
    Dbulk        = 1.58e-3

    // External field in T
    Bz := 0.4
    B_ext = vector(0, 0, Bz)

    // No Demag
    NoDemagSpins = 1

    m = BlochSkyrmion(1, -1)

    OutputFormat = OVF2_TEXT

    // Relax with specific torque:
    // alpha       = 0.9
    // RunWhile(MaxTorque > 1e-3)

    // Relax with conjugate gradient:
    MinimizerStop = 1e-4
    minimize();
    SaveAs(m, "3D_skyrmion_d{}e-2nm")
    """.format(lx, ly, lz, dx, dy, dz, nx, ny, nz, dxy)
    )

    print(sim)
    with open('mumax_3D_sk_tmp.mx3', 'w') as F:
        F.write(sim)

    subprocess.call('mumax3 mumax_3D_sk_tmp.mx3', shell=True)
