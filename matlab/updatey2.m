function y = updatey2(x,z,y,rho,n)
% Function for updating y in community-based ADMM
y = y + rho*(C*x + D*z);
end