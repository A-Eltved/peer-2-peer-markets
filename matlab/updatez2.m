function z = updatez2(x, y, rho,n)
% Function for updating z in community-based ADMM
alpha = x(n*2+1 : n*3);
beta = x(n*3+1:end);

H = rho*eye(2,2);
h = [70-y(2) - rho*sum(alpha); -40*y(3) - rho*sum(beta)] ;

options = optimoptions('quadprog','Display','off');
z = quadprog(H,h,-eye(2,2),zeros(2,1),[],[],zeros(2,1),inf(2,1),[],options);
end