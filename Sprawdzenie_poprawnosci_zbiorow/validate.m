function [D, Q, A1, A2] = validate(A1, A2)

% Inicjalizacja wektorów
A = [A1; A2];
D = [];
Q = [];
to_del_A1 = [];
to_del_A2 = [];
to_add_A1 = [];
to_add_A2 = [];

% Odczytanie iloœci punktów i ich wspó³rzêdnych
[liczba_punktow, liczba_wspolzednych] = size(A);
[liczba_punktow_A1, liczba_wspolzednych_A1] = size(A1);
dominuje(liczba_punktow) = 0;
zdominowany(liczba_punktow) = 0;

% Policzenie iloœci punktów zdominowanych przez ka¿dy pojedynczy punkt
% oraz iloœci punktów zdominowanych przez ka¿dy pojedynczy punkt
for i=1:liczba_punktow
    for j=i+1:liczba_punktow
        lepszy = compare_points(A(i,:), A(j,:));
        if lepszy < 0
            dominuje(i) = dominuje(i) + 1;
            zdominowany(j) = zdominowany(j) + 1;
        elseif lepszy > 0
            dominuje(j) = dominuje(j) + 1;
            zdominowany(i) = zdominowany(i) + 1;
        end
    end
end

% Przygotowanie do przeniesienia punktów pomiêdzy zbiorami 
% i usuwaniêcia punktów ze zbiorów
% oraz wyznaczenie punktów docelowych i status quo pomiêdzy 2 zbiorami
for i=1:liczba_punktow
    if dominuje(i) ~= 0 && zdominowany(i) == 0
        D = [D; A(i,:)];
        if i > liczba_punktow_A1
            to_add_A1 = [to_add_A1; A(i, :)];
            to_del_A2 = [to_del_A2, i - liczba_punktow_A1];
        end
    elseif dominuje(i) == 0 && zdominowany(i) ~= 0
        Q = [Q; A(i,:)];
        if i <= liczba_punktow_A1
            to_add_A2 = [to_add_A2; A(i, :)];
            to_del_A1 = [to_del_A1, i];
        end
    elseif dominuje(i) == 0 && zdominowany(i) == 0
        if i > liczba_punktow_A1
            to_del_A2 = [to_del_A2, i - liczba_punktow_A1];
        else
            to_del_A1 = [to_del_A1, i];
        end
    end
end

% Dodawanie punktów do zbiorów
A1 = [A1; to_add_A1];
A2 = [A2; to_add_A2];

% Usuwanie punktów ze zbiorów
if ~isempty(to_del_A1)
    for i = length(to_del_A1):-1:1
        A1(to_del_A1(i),:) = [];
    end
end

if ~isempty(to_del_A2)
    for i = length(to_del_A2):-1:1
        A2(to_del_A2(i),:) = [];
    end
end