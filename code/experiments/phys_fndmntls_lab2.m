% Fundamentals Laboratory #2

%Physical Parameters
m = 2;
v_i = 2;
F_push = 8;
F_resist = -2;

%Displacement vector
x = 0:0.5:10;

%Net Force
F_net = F_push + F_resist;

%Initial kinetic energy
K_i = 0.5 * m * v_i^2;

% Net work performed at each displacement
W_net = F_net * x;

%Kinetic energy at each displacement
K = K_i + W_net;

% Speed at each displacement
v = sqrt(2 * K / m);

% Display final reuslts
printf("Final net work: %.2f J\n", W_net(end));
printf("Final kinetic energy: %.2f J\n", K(end));
printf("Final speed: %.2f m/s\n", v(end));

%Visualization
plot(x, W_net, "b-", x, K, "r-");

xlabel("Displacement (m)");
ylabel("Energy (J)");
title("Work-Energy Theorem");
legend("Net Work", "Kinetic Energy");

grid on;
drawnow;

savefig("work-energy_vs_displacement.ofig");
print("work-energy_vs_displacemnts.png", "-dpng", "-r300");


