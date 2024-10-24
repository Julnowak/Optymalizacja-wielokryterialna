function compared = compare_points(a, b)

% Sprawdzenie czy punkty maj� tyle samo wsp��dnych
if length(a) ~= length(b)
    disp('mistake')
end

% Inicjalizacja licznik�w
a_better = 0;
a_worse = 0;

% Policzenie ilo�ci lepszych i gorszych warto�ci wsp�rz�dnych punkt�w
for i=1:length(a)
    if a(i) < b(i)
        a_better = a_better + 1;
    end
    if a(i) > b(i)
        a_worse = a_worse + 1;
    end
end

if a_better ~= 0 && a_worse == 0
    % Punkt a jest lepszy
    compared = -1;

elseif a_worse ~= 0 && a_better == 0
    % Punkt b jest lepszy
    compared = 1;
    
else
    % Punkty s� niepor�wnywalne
    compared = 0;
end
