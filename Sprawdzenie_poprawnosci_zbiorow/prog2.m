% Przyk³adowe zbiory
A1 = readmatrix('A0.csv', 'Range', 'B2:D4');
A2 = readmatrix('A1.csv', 'Range', 'B2:D4');
A3 = readmatrix('A2.csv', 'Range', 'B2:D5');
A4 = readmatrix('A3.csv', 'Range', 'B2:D4');

% Narysowanie pocz¹tkowych zbiorów
figure(1)
hold on
grid on
view(3)
plot3(A1(:, 1), A1(:, 2), A1(:, 3), 'x', 'color', 'b')
plot3(A2(:, 1), A2(:, 2), A2(:, 3), 'x', 'color', 'r')
plot3(A3(:, 1), A3(:, 2), A3(:, 3), 'x', 'color', 'k')
plot3(A4(:, 1), A4(:, 2), A4(:, 3), 'x', 'color', 'm')
xlabel('1 wspó³rzêdna')
ylabel('2 wspó³rzêdna')
zlabel('3 wspó³rzêdna')

[A1, A2, A3, A4] = validate_4(A1, A2, A3, A4);

% Narysowanie koñcowych zbiorów
plot3(A1(:, 1), A1(:, 2), A1(:, 3), 'o', 'color', 'b')
plot3(A2(:, 1), A2(:, 2), A2(:, 3), 'o', 'color', 'r')
plot3(A3(:, 1), A3(:, 2), A3(:, 3), 'o', 'color', 'k')
plot3(A4(:, 1), A4(:, 2), A4(:, 3), 'o', 'color', 'm')

legend('Pocz¹tkowe punkty zbioru A1', 'Pocz¹tkowe punkty zbioru A2', 'Pocz¹tkowe punkty zbioru A3', 'Pocz¹tkowe punkty zbioru A4', 'Koñcowe punkty zbioru A1', 'Koñcowe punkty zbioru A2', 'Koñcowe punkty zbioru A3', 'Koñcowe punkty zbioru A4')

