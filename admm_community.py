from cvxopt import matrix, spdiag, spmatrix, solvers, printing
from cvxopt.blas import nrm2
import sys



def admm_community(x,z,y,A,b,Pl,Pu,C,D,**kwargs):
    '''
    Solve community-based market using ADMM. 

    Input: 
        x:      initial guess for stacked p,q,alpha,beta
        z:      initial guess for import and export
        y:      initial guess for lagrange multipliers
        A:      diagonal matrix with coefficients for quadratic terms of costs
        b:      vector of coefficients for linear terms of costs
        Pl:     lower bound on power generation
        Pu:     upper bound on power generation
        C:      matrix to be multiplied with x in coupling constraint (Cx+Dz=0)
        D:      matrix to be multiplied with z in coupling constraint (Cx+Dz=0)
        gamma:  base price for energy export/import (default: 40)
        tau:    added cost for energy import (default: 30)
        rho:    penalty parameter/step size in y

    Output: x,z,y
    '''
    gamma = kwargs.get('gamma',40.0)
    tau = kwargs.get('tau',30.0)
    rho = kwargs.get('rho',1.0)
    maxiter = kwargs.get('maxiter',1000)
    epspri = kwargs.get('epspri',1e-4)
    epsdual = kwargs.get('epsdual',1e-4)
    verbose = kwargs.get('verbose',False)
    print("Starting ADMM for community...")
    print("gamma: ", gamma,", tau: ", tau,", rho: ", rho)
    """ Begin inner functions """
    def _update_x(x,z,y,A,b,Pl,Pu,C,D,rho):
        # set up matrices and vectors for QP
        n = int(x.size[0]/4)
        rhoOnes = matrix(rho,(n,n),tc = 'd')
        H = spdiag([A,rhoOnes,rhoOnes,rhoOnes]) 
        #print(H)
        h1 = b
        h2 = matrix(y[0],size=(n,1))
        h3 = matrix(y[1]-rho*z[0],size=(n,1))
        h4 = matrix(y[2]-rho*z[1],size=(n,1))
        h = matrix([h1,h2,h3,h4],size=(4*n,1))
        #print(h)
        Aineq_I = list(range(4*n))
        Aineq_J = list(range(n)) + list(range(n)) + list(range(2*n,4*n))
        Aineq_vals = [1.0]*n + [-1.0]*(3*n)
        Aineq = spmatrix(Aineq_vals,Aineq_I,Aineq_J,size=(4*n,4*n))
        #print(Aineq)
        bineq = matrix([Pu,-Pl,matrix(0.0,size=(2*n,1))],size=(4*n,1))
        #print("bineq: ",bineq)
        Aeq_I = list(range(n))*4
        Aeq_J = list(range(4*n))
        Aeq_vals = [1.0]*(3*n) + [-1.0]*n
        Aeq = spmatrix(Aeq_vals,Aeq_I,Aeq_J,size=(n,4*n))
        #print(Aeq)
        beq = matrix(0.0,size=(n,1))
        solvers.options['show_progress'] = False
        sol= solvers.qp(H, h, Aineq, bineq, Aeq, beq)
        x = sol['x']
        return x

    def _update_z(x,z,y,A,b,C,D,gamma,tau,rho):
        n = b.size[0]
        # set up matrices and vectors for QP
        H = matrix([rho,0,0,rho],size=(2,2),tc='d')
        #print("Hz: ",H)
        h1 = gamma + tau - y[1] - rho* (matrix(1.0,size=(1,n))*x[2*n:3*n]) # alpha from x
        h2 = -gamma - y[2] - rho* (matrix(1.0,size=(1,n))*x[3*n:4*n]) # beta from x
        h = matrix([h1,h2],size=(2,1))
        #print(h)
        Aineq_I = list(range(2))
        Aineq = spmatrix(-1.0,Aineq_I,Aineq_I,size=(2,2))
        #print(Aineq)
        bineq = matrix(0.0,size=(2,1))
        #print("bineq: ",bineq)
        solvers.options['show_progress'] = False
        sol= solvers.qp(H, h, Aineq, bineq)
        z = sol['x']

        return z

    def _update_y(x,z,y,C,D,rho):
        y += rho*(C*x + D*z)
        return y
    """ End of inner functions """
    for k in range(maxiter):
        sys.stdout.write("\rIteration: %i" % k)
        sys.stdout.flush()
        zprev = z
        if verbose: 
            p = x[0:n]
            q =x[n:(2*n)]
            alpha = x[(2*n):(3*n)]
            beta = x[(3*n):(4*n)]
            print("p: ",p.T)
            print("q: ",q.T)
            print("sum(q): ",sum(q))
            print("alpha: ",alpha.T)
            print("sum(alpha): ",sum(alpha))
            print("beta: ",beta.T)
            print("sum(beta): ",sum(beta))
            print("z: ",z.T)
            print("y: ",y.T)
        x = _update_x(x,z,y,A,b,Pl,Pu,C,D,rho)
        z = _update_z(x,z,y,A,b,C,D,gamma,tau,rho)
        y = _update_y(x,z,y,C,D,rho)


        r = C*x + D*z
        rnorm = nrm2(r)
        s = rho*C.T*D*(z - zprev)
        snorm = nrm2(s)
        if verbose: print("Iteration: ",k,"Primal residual norm: ", rnorm,"Dual residual norm: ", snorm)
        if rnorm < epspri and snorm < epsdual: break

    if k == maxiter-1: 
        sys.stdout.write("\nNOT CONVERGED.\nPrimal residual: %.2e\nDual residual:   %.2f\n" % (rnorm,snorm)) 
    sys.stdout.write("\n")
    return x,z,y


########### Start of main ###############

def solve_admm_community(Pren7 = 18.5):
    """
    Solves the community based market with ADMM. 

    Input:
        Pren7:  renewable energy production of agent 7

    Output
        p:      schedule
        y[0]:   market price
    """
    # printing options
    printing.options['dformat'] = '%.1f'
    printing.options['width'] = -1

    #
    n = 14
    Pmin = matrix([-21.7,-94.2,-47.8,-7.6,-11.2,-29.5,-9.,-3.5,-6.1,-13.5,-14.9,0.,0.,0.],(14,1))
    Pmax = matrix([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,20.,50.,10.],(14,1))
    Pren = matrix([0.,0.,0.,14.9,9.,10.,Pren7,2.,7.,5.,5.,0.,0.,0.],(14,1))
    
    Pl = Pmin + Pren
    Pu = Pmax + Pren


    a = [4.,1.,2.,10.,8.,4.,9.,15.,18.,7.,6.,7.,2.,8.];
    b = matrix([130.,120.,135.,125.,140.,145.,150.,135.,140.,125.,120.,25.,10.,20.],size=(n,1))
    A = spdiag(a);


    # Initial guesses for ADMM
    x = matrix([Pl,matrix(0.0,(n*3,1))],size=(4*n,1))
    z = matrix(0.0,(2,1))
    y = matrix(0.0,(3,1))

    # ADMM matrices
    l = [0]*n + [1]*n + [2]*n
    Cvals = [1.0]*n + [1.0]*(2*n)
    C = spmatrix(Cvals,l,range(n,4*n),size=(3,4*n)) 
    D = spmatrix(-1.0,[1,2],[0,1],size=(3,2))
    #print(D)

    #print(x.size)
    #x = _update_x(x,z,y,A,b,Pl,Pu,C,D,rho)
    #print("x: ",x)
    #z = _update_z(x,z,y,A,b,C,D,gamma,tau,rho)
    #print("z: ",z)
    #y = _update_y(x,z,y,C,D,rho)
    #print("y: ",y)

    x,z,y = admm_community(x,z,y,A,b,Pl,Pu,C,D,rho=50.0,maxiter=10000)
    p = x[0:n]
    q =x[n:(2*n)]
    alpha = x[(2*n):(3*n)]
    beta = x[(3*n):(4*n)]
    print("p: ",p.T)
    print("q: ",q.T)
    #print("sum(q): ",sum(q))
    print("alpha: ",alpha.T)
    #print("sum(alpha): ",sum(alpha))
    print("beta: ",beta.T)
    #print("sum(beta): ",sum(beta))
    print("import: ", z[0], ", Export: ",z[1])
    print("market price: ", y[0])
    return p,y[0]
