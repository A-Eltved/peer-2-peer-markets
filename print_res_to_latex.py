def write_schedule(p,filename='out_schedule.txt',caption='Schedule ...'):
    print('Writing table...')
    with open(filename,'w') as f:
        # Write header
        f.write('\\begin{table}[h]\n')
        f.write('\\caption{'+caption+'}\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{l|cccccccccccccc}\n')
        f.write('Agent &  1  &   2   &   3   &   4  &  5  &  6  &  7   &   8  &  9  &  10 &  11 &  12 &  13  & 14  \\\\ \\hline\n')
        f.write('$p_i$ [MW] &')
        for i in range(len(p.value)):
            f.write('{:.2f}'.format(p.value.item(i)))
            if not i == len(p.value)-1:
                f.write(' & ')
            else: 
                f.write(' \n')
        f.write('\\end{tabular}\n')
        f.write('\\label{tab:}\n')
        f.write('\\end{table}\n')
    print('Done.')
    
def write_pricing(p,price,filename='out_price.txt',caption='Payments and revenues ...'):
    print('Writing pricing table...')
    with open(filename,'w') as f:
        # Write header
        f.write('\\begin{table}[h]\n')
        f.write('\\caption{'+caption+'}\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{l|cccccccccccccc}\n')
        f.write('Agent &  1  &   2   &   3   &   4  &  5  &  6  &  7   &   8  &  9  &  10 &  11 &  12 &  13  & 14  \\\\ \\hline\n')
        f.write('Price [\\$] &')
        for i in range(len(p.value)):
            f.write('{:.2f}'.format(p.value.item(i)*price))
            if not i == len(p.value)-1:
                f.write(' & ')
            else: 
                f.write(' \n')
        f.write('\\end{tabular}\n')
        f.write('\\label{tab:}\n')
        f.write('\\end{table}\n')
    print('Done.')