function z = updatez(x,y,rho)
% Function for updating z in pool-based ADMM

H = rho*[1,-1;-1,1];
h = [70;-40] + y*[1;-1] + rho*[ones(size(x))'*x; -ones(size(x))'*x];