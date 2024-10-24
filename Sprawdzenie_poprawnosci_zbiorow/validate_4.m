function [v_A1, v_A2, v_A3, v_A4] = validate_4(A1, A2, A3, A4)

% Utworzenie cell waktor�w do iteracji
V = {A1, A2, A3, A4};
V_temp = {};

% Por�wnanie zbior�w ka�dego z ka�dym
for i = 1:length(V)
    for j = i+1:length(V)
        [V_temp{i}, V_temp{j}, V{i}, V{j}] = validate(V{i}, V{j});
    end
end

% Odkomentowa� �eby zobaczy� wynik po�redni
% v_A1 = V{1};
% v_A2 = V{2};
% v_A3 = V{3};
% v_A4 = V{4};

% Odkomentowa� �eby zobaczy� wynik ko�cowy
v_A1 = V_temp{1};
v_A2 = V_temp{2};
v_A3 = V_temp{3};
v_A4 = V_temp{4};
