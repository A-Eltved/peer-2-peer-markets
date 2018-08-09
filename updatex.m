function x = updatex(z,y,A,b,Pl,Pu,rho)
% Function for updating x pool-based ADMM

H = A + rho*ones(size(A));
h = b + (y + rho*(z(1) - z(2)))*ones(size(b));

x = quadprog(H,h,[],[],[],[],Pl,Pu);