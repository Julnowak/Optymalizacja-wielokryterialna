% Przyk³adowe zbiory
A1 = [-8 -6; -7 -3; -6 -5; -4 -7; 2 -8];
A2 = [-4 1; -2 -2; -2 -5];
A3 = [2 -1; 1 4; 3 2; 5 5; -6 6; 8 4; -3 -2];
A4 = [3 7; 5 3; 7 6];

% Narysowanie pocz¹tkowych zbiorów
figure(1)
hold on
grid on
plot(A1(:, 1), A1(:, 2), 'x', 'color', 'b')
plot(A2(:, 1), A2(:, 2), 'x', 'color', 'r')
plot(A3(:, 1), A3(:, 2), 'x', 'color', 'k')
plot(A4(:, 1), A4(:, 2), 'x', 'color', 'm')
axis([-9 9 -9 8])
xlabel('1 wspó³rzêdna')
ylabel('2 wspó³rzêdna')

[A1, A2, A3, A4] = validate_4(A1, A2, A3, A4);

% Narysowanie koñcowych zbiorów
plot(A1(:, 1), A1(:, 2), 'o', 'color', 'b')
plot(A2(:, 1), A2(:, 2), 'o', 'color', 'r')
plot(A3(:, 1), A3(:, 2), 'o', 'color', 'k')
plot(A4(:, 1), A4(:, 2), 'o', 'color', 'm')
%legend('Pocz¹tkowe punkty zbioru A1', 'Pocz¹tkowe punkty zbioru A2', 'Pocz¹tkowe punkty zbioru A3', 'Pocz¹tkowe punkty zbioru A4', 'Punkty uznane za zbiór A1 przed ostateczn¹ klasyfikacj¹', 'Punkty uznane za zbiór A2 przed ostateczn¹ klasyfikacj¹', 'Punkty uznane za zbiór A3 przed ostateczn¹ klasyfikacj¹', 'Punkty uznane za zbiór A4 przed ostateczn¹ klasyfikacj¹')
%legend('Pocz¹tkowe punkty zbioru A1', 'Pocz¹tkowe punkty zbioru A2', 'Pocz¹tkowe punkty zbioru A3', 'Pocz¹tkowe punkty zbioru A4', 'Spe³niaj¹ce warunki punkty nowego zbioru A1', 'Spe³niaj¹ce warunki punkty nowego zbioru A2', 'Spe³niaj¹ce warunki punkty nowego zbioru A3', 'Spe³niaj¹ce warunki punkty nowego zbioru A4')
