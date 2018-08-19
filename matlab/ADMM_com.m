function [x,z,y] = ADMM_com(x,z,y,A,b,Pl,Pu,rho,n)

maxiter = 1000;
tolpri = 1e-3;
toldual = 1e-3;

% r = ones(size(x))'*x + [1;-1]'*z;
% fprintf('Initial primal residual: %.2f\n',norm(r));

% Matrices for y-update and for calulating residuals (r and s):
C = [zeros(1, n), ones(1, n),  zeros(1, n), zeros(1, n) ;
     zeros(1, n), zeros(1, n), ones(1, n),  zeros(1, n) ;
     zeros(1, n), zeros(1, n), zeros(1, n), ones(1,n)    ];
 
D = [0, 0; -1, 0; 0, -1];

for k = 1:maxiter
    fprintf('Starting iteration %i\n', k);
    
    zprev = z; % used for dual residual
    yprev = y;
    
    x = updatex2(z,y,A,b,Pl,Pu,rho);
    z = updatez2(x,y,rho,n);
    %y = updatey(x,z,y,rho,n, C, D);
    y = yprev + rho*(C*x + D*z);
    
    r = C*x + D*z;
    s = rho*C'*D*(z - zprev);
    
    fprintf('Iteration %i done. Norm of residuals: %.2e, %.2e\n',k,norm(r), norm(s));
    if norm(r) < tolpri && norm(s) < toldual
        break;
    end
end