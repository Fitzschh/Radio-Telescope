% Fundamentals Laboratory #1

% Physical Parameters
m = 2;
v = 0:1:10;

% Kinetic Energy Formula
K = (1/2) * m * v.^2

% Plot the graph for the result
plot(v, K);
xlabel("Speed (m/s)");
ylabel("Kinetic Energy (J)");
title("Speed vs Kinetic Energy");
grid on;
