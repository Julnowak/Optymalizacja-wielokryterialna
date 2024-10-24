function [v_A1, v_A2, v_A3, v_A4] = validate_4(A1, A2, A3, A4)

% Utworzenie cell waktorów do iteracji
V = {A1, A2, A3, A4};
V_temp = {};

% Porównanie zbiorów ka¿dego z ka¿dym
for i = 1:length(V)
    for j = i+1:length(V)
        [V_temp{i}, V_temp{j}, V{i}, V{j}] = validate(V{i}, V{j});
    end
end

% Odkomentowaæ ¿eby zobaczyæ wynik poœredni
% v_A1 = V{1};
% v_A2 = V{2};
% v_A3 = V{3};
% v_A4 = V{4};

% Odkomentowaæ ¿eby zobaczyæ wynik koñcowy
v_A1 = V_temp{1};
v_A2 = V_temp{2};
v_A3 = V_temp{3};
v_A4 = V_temp{4};
