function [x,z,y] = ADMM_pool(x,z,y,A,b,Pl,Pu,rho) 


maxiter = 1000;
tolpri = 1e-3;
toldual = 1e-3;

% r = ones(size(x))'*x + [1;-1]'*z;
% fprintf('Initial primal residual: %.2f\n',norm(r));

for k = 1:maxiter
    zprev = z; % used for dual residual
    
    x = updatex(z,y,A,b,Pl,Pu,rho);
    z = updatez(x,y,rho);
    y = updatey(x,z,y,rho);
    
    r = ones(size(x))'*x + [1;-1]'*z;
    s = rho*ones(size(x)) * ([1;-1]'*(z - zprev));
    
    fprintf('Iteration %i done. Norm of residuals: %.2e, %.2e\n',k,norm(r), norm(s));
    if norm(r) < tolpri && norm(s) < toldual
        break;
    end
end