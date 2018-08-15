def write_schedule(p,filename='out_schedule.txt',caption='Schedule ...',label = ''):
    print('Writing table...')
    with open(filename,'w') as f:
        # Write header
        f.write('\\begin{table}[h]\n')
        f.write('\\caption{'+caption+'}\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{l|cccccccccccccc}\n')
        f.write('Agent &  1  &   2   &   3   &   4  &  5  &  6  &  7   \\\\ \\hline\n')
        f.write('$p^\star_i$ [MW] &')
        for i in range(7):
            f.write('{:.2f}'.format(p.value.item(i)))
            if not i == 6:
                f.write(' & ')
            else: 
                f.write(' \\\\ \\hline\\hline\n')
        f.write('Agent &   8  &  9  &  10 &  11 &  12 &  13  & 14  \\\\ \\hline\n')
        f.write('$p^\star_i$ [MW] &')
        for i in range(7,len(p.value)):
            f.write('{:.2f}'.format(p.value.item(i)))
            if not i == len(p.value)-1:
                f.write(' & ')
            else: 
                f.write(' \n')
        f.write('\\end{tabular}\n')
        f.write('\\label{tab:'+label+'}\n')
        f.write('\\end{table}\n')
    print('Done.')
    
def write_pricing(p,price,filename='out_price.txt',caption='Payments and revenues ...',label = ''):
    print('Writing pricing table...')
    with open(filename,'w') as f:
        # Write header
        f.write('\\begin{table}[h]\n')
        f.write('\\caption{'+caption+'}\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{l|cccccccccccccc}\n')
        f.write('Agent &  1  &   2   &   3   &   4  &  5  &  6  &  7  \\\\ \\hline\n')
        f.write('Payment/revenue [\\$] &')
        for i in range(7):
            f.write('{:.2f}'.format(p.value.item(i)*price))
            if not i == 6:
                f.write(' & ')
            else: 
                f.write(' \\\\ \\hline \\hline \n')
        f.write('Agent &  8  &  9  &  10 &  11 &  12 &  13  & 14  \\\\ \\hline\n')
        f.write('Payment/revenue [\\$] &')
        for i in range(7,len(p.value)):
            f.write('{:.2f}'.format(p.value.item(i)*price))
            if not i == len(p.value)-1:
                f.write(' & ')
            else: 
                f.write(' \n')
        f.write('\\end{tabular}\n')
        f.write('\\label{tab:'+label+'}\n')
        f.write('\\end{table}\n')
    print('Done.')