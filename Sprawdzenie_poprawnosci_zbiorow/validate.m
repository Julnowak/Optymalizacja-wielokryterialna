function [D, Q, A1, A2] = validate(A1, A2)

% Inicjalizacja wektor�w
A = [A1; A2];
D = [];
Q = [];
to_del_A1 = [];
to_del_A2 = [];
to_add_A1 = [];
to_add_A2 = [];

% Odczytanie ilo�ci punkt�w i ich wsp�rz�dnych
[liczba_punktow, liczba_wspolzednych] = size(A);
[liczba_punktow_A1, liczba_wspolzednych_A1] = size(A1);
dominuje(liczba_punktow) = 0;
zdominowany(liczba_punktow) = 0;

% Policzenie ilo�ci punkt�w zdominowanych przez ka�dy pojedynczy punkt
% oraz ilo�ci punkt�w zdominowanych przez ka�dy pojedynczy punkt
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

% Przygotowanie do przeniesienia punkt�w pomi�dzy zbiorami 
% i usuwani�cia punkt�w ze zbior�w
% oraz wyznaczenie punkt�w docelowych i status quo pomi�dzy 2 zbiorami
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

% Dodawanie punkt�w do zbior�w
A1 = [A1; to_add_A1];
A2 = [A2; to_add_A2];

% Usuwanie punkt�w ze zbior�w
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