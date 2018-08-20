function x = updatex2(z,y,A,b,Pl,Pu,rho)
% Function for updating x community-based ADMM

H = [A,              zeros(size(A)),    zeros(size(A)),    zeros(size(A)) ;
     zeros(size(A)), rho*ones(size(A)), zeros(size(A)),    zeros(size(A)) ;
     zeros(size(A)), zeros(size(A)),    rho*ones(size(A)), zeros(size(A)) ;
     zeros(size(A)), zeros(size(A)),    zeros(size(A)),    rho*ones(size(A))] ;
 
h = [b; y(1)*ones(length(b),1); (y(2) - rho*z(1))*ones(length(b),1); (y(3) - rho*z(2))*ones(length(b),1) ];

Aeq = [eye(size(A)), eye(size(A)), eye(size(A)), -eye(size(A))];
beq = zeros(length(b), 1) ;

Aineq = [eye(size(A)),   zeros(size(A)), zeros(size(A)), zeros(size(A));
         -eye(size(A)),  zeros(size(A)), zeros(size(A)), zeros(size(A));
         zeros(size(A)), zeros(size(A)), -eye(size(A)),  zeros(size(A)); 
         zeros(size(A)), zeros(size(A)), zeros(size(A)), -eye(size(A)) ]; 
     
bineq = [Pu ; -Pl; zeros(length(b), 1); zeros(length(b), 1)];

options = optimoptions('quadprog','Display','off');

x = quadprog(H,h,Aineq,bineq,Aeq,beq,[],[],[],options);
end