function compared = compare_points(a, b)

% Sprawdzenie czy punkty maj¹ tyle samo wspó³¿êdnych
if length(a) ~= length(b)
    disp('mistake')
end

% Inicjalizacja liczników
a_better = 0;
a_worse = 0;

% Policzenie iloœci lepszych i gorszych wartoœci wspó³rzêdnych punktów
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
    % Punkty s¹ nieporównywalne
    compared = 0;
end
