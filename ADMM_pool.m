function [x,z] = ADMM_pool(x,z,y,A,b,Pl,Pu,rho) 

maxiter = 100;
tolpri = 1e-3;
toldual = 1e-3;

r = ones(size(x))'*x + [1;-1]'*z;
fprintf('Initial primal residual: %.2f\n',norm(r));

for k = 1:maxiter
    xprev = x;
    zprev = z; 
    yprev = y;
    
    x = updatex(z,y,A,b,Pl,Pu,rho);
    z = updatez(x,y,rho);
    y = updatey(x,z);
    
    r = ones(size(x))'*x + [1;-1]'*z;
    s = rho*ones(size(x)) * ([1;-1]'*(z - zprev));
    
    fprintf('Norm of residuals: %.2f, %.2f\n',norm(r), norm(s));
    if norm(r) < tolpri && norm(s) < toldual
        break;
    end
end