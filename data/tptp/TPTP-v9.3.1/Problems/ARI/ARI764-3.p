%------------------------------------------------------------------------------
% File     : ARI764-3 : TPTP v9.3.1. Released v9.3.0.
% Domain   : Arithmetic
% Problem  : Find X such that X / 4 = 4.
% Version  : Especial
% English  : 

% Refs     : [Sai24] Saito (2024), Email to Geoff Sutcliffe
% Source   : [Sai24]
% Names    : division_exist.p [Sai24]

% Status   : Unsatisfiable
% Rating   : 0.94 v9.3.0
% Syntax   : Number of clauses     :   10 (  10 unt;   0 nHn;   1 RR)
%            Number of literals    :   10 (  10 equ;   1 neg)
%            Maximal clause size   :    1 (   1 avg)
%            Maximal term depth    :    6 (   2 avg)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   8 usr;   3 con; 0-3 aty)
%            Number of variables   :   15 (   7 sgn)
% SPC      : CNF_UNS_RFO_PEQ_UEQ

% Comments : The rules are of TRS_Standard/Rubio_04/division.ari in TPDB.
%------------------------------------------------------------------------------
cnf(rule1,axiom,
    le(zero,Y) = true ).

cnf(rule2,axiom,
    le(s(X),zero) = false ).

cnf(rule3,axiom,
    le(s(X),s(Y)) = le(X,Y) ).

cnf(rule4,axiom,
    minus(zero,Y) = zero ).

cnf(rule5,axiom,
    minus(s(X),Y) = ifMinus(le(s(X),Y),s(X),Y) ).

cnf(rule6,axiom,
    ifMinus(true,s(X),Y) = zero ).

cnf(rule7,axiom,
    ifMinus(false,s(X),Y) = s(minus(X,Y)) ).

cnf(rule8,axiom,
    quot(zero,s(Y)) = zero ).

cnf(rule9,axiom,
    quot(s(X),s(Y)) = s(quot(minus(X,Y),s(Y))) ).

cnf(goal,negated_conjecture,
    quot(X,s(s(s(s(zero))))) != s(s(s(s(zero)))) ).

%------------------------------------------------------------------------------
