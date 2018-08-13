function y = updatey(x,z,y,rho)
% Function for updating y in pool-based ADMM

y = y + rho*(ones(size(x))'*x + [1;-1]'*z);