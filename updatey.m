function y = updatey(x,z)
% Function for updating y in pool-based ADMM

y = y + ones(size(x))'*x + [1;-1]*z;