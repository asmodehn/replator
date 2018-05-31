import ptyprocess


if '__main__'==__name__:
    p = ptyprocess.PtyProcessUnicode.spawn(['python'])
    out = p.read(200)
    inp = p.write('6+6\n')
    out = p.read(20)
    pass