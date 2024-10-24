% Przyk�adowe zbiory
A1 = readmatrix('A0.csv', 'Range', 'B2:D4');
A2 = readmatrix('A1.csv', 'Range', 'B2:D4');
A3 = readmatrix('A2.csv', 'Range', 'B2:D5');
A4 = readmatrix('A3.csv', 'Range', 'B2:D4');

% Narysowanie pocz�tkowych zbior�w
figure(1)
hold on
grid on
view(3)
plot3(A1(:, 1), A1(:, 2), A1(:, 3), 'x', 'color', 'b')
plot3(A2(:, 1), A2(:, 2), A2(:, 3), 'x', 'color', 'r')
plot3(A3(:, 1), A3(:, 2), A3(:, 3), 'x', 'color', 'k')
plot3(A4(:, 1), A4(:, 2), A4(:, 3), 'x', 'color', 'm')
xlabel('1 wsp�rz�dna')
ylabel('2 wsp�rz�dna')
zlabel('3 wsp�rz�dna')

[A1, A2, A3, A4] = validate_4(A1, A2, A3, A4);

% Narysowanie ko�cowych zbior�w
plot3(A1(:, 1), A1(:, 2), A1(:, 3), 'o', 'color', 'b')
plot3(A2(:, 1), A2(:, 2), A2(:, 3), 'o', 'color', 'r')
plot3(A3(:, 1), A3(:, 2), A3(:, 3), 'o', 'color', 'k')
plot3(A4(:, 1), A4(:, 2), A4(:, 3), 'o', 'color', 'm')

legend('Pocz�tkowe punkty zbioru A1', 'Pocz�tkowe punkty zbioru A2', 'Pocz�tkowe punkty zbioru A3', 'Pocz�tkowe punkty zbioru A4', 'Ko�cowe punkty zbioru A1', 'Ko�cowe punkty zbioru A2', 'Ko�cowe punkty zbioru A3', 'Ko�cowe punkty zbioru A4')

