% Przyk�adowe zbiory
A1 = [-8 -6; -7 -3; -6 -5; -4 -7; 2 -8];
A2 = [-4 1; -2 -2; -2 -5];
A3 = [2 -1; 1 4; 3 2; 5 5; -6 6; 8 4; -3 -2];
A4 = [3 7; 5 3; 7 6];

% Narysowanie pocz�tkowych zbior�w
figure(1)
hold on
grid on
plot(A1(:, 1), A1(:, 2), 'x', 'color', 'b')
plot(A2(:, 1), A2(:, 2), 'x', 'color', 'r')
plot(A3(:, 1), A3(:, 2), 'x', 'color', 'k')
plot(A4(:, 1), A4(:, 2), 'x', 'color', 'm')
axis([-9 9 -9 8])
xlabel('1 wsp�rz�dna')
ylabel('2 wsp�rz�dna')

[A1, A2, A3, A4] = validate_4(A1, A2, A3, A4);

% Narysowanie ko�cowych zbior�w
plot(A1(:, 1), A1(:, 2), 'o', 'color', 'b')
plot(A2(:, 1), A2(:, 2), 'o', 'color', 'r')
plot(A3(:, 1), A3(:, 2), 'o', 'color', 'k')
plot(A4(:, 1), A4(:, 2), 'o', 'color', 'm')
%legend('Pocz�tkowe punkty zbioru A1', 'Pocz�tkowe punkty zbioru A2', 'Pocz�tkowe punkty zbioru A3', 'Pocz�tkowe punkty zbioru A4', 'Punkty uznane za zbi�r A1 przed ostateczn� klasyfikacj�', 'Punkty uznane za zbi�r A2 przed ostateczn� klasyfikacj�', 'Punkty uznane za zbi�r A3 przed ostateczn� klasyfikacj�', 'Punkty uznane za zbi�r A4 przed ostateczn� klasyfikacj�')
%legend('Pocz�tkowe punkty zbioru A1', 'Pocz�tkowe punkty zbioru A2', 'Pocz�tkowe punkty zbioru A3', 'Pocz�tkowe punkty zbioru A4', 'Spe�niaj�ce warunki punkty nowego zbioru A1', 'Spe�niaj�ce warunki punkty nowego zbioru A2', 'Spe�niaj�ce warunki punkty nowego zbioru A3', 'Spe�niaj�ce warunki punkty nowego zbioru A4')
