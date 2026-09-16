%------------------------------------------------------------------------------
% File     : ARI765-2 : TPTP v9.3.1. Released v9.3.0.
% Domain   : Arithmetic
% Problem  : Find X such that log_2(2^X) = 4.
% Version  : Especial
% English  : 

% Refs     : [AG00]  Arts & Giesl (2000), Termination of Term Rewriting usi
%          : [AG01]  Arts & Giesl (1991), A Collection of Examples for Term
%          : [Sai24] Saito (2024), Email to Geoff Sutcliffe
% Source   : [Sai24]
% Names    : Example 3.8 [AG01]
%          : log_exist.p [Sai24]

% Status   : Unsatisfiable
% Rating   : 0.67 v9.3.0
% Syntax   : Number of clauses     :   16 (  16 unt;   0 nHn;   4 RR)
%            Number of literals    :   16 (  16 equ;   1 neg)
%            Maximal clause size   :    1 (   1 avg)
%            Maximal term depth    :    7 (   2 avg)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   11 (  11 usr;   3 con; 0-3 aty)
%            Number of variables   :   18 (   7 sgn)
% SPC      : CNF_UNS_RFO_PEQ_UEQ

% Comments : The rules are of TRS_Standard/AG01/#3.8b.ari from TPDB.
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
    minus(s(X),Y) = if_minus(le(s(X),Y),s(X),Y) ).

cnf(rule6,axiom,
    if_minus(true,s(X),Y) = zero ).

cnf(rule7,axiom,
    if_minus(false,s(X),Y) = s(minus(X,Y)) ).

cnf(rule8,axiom,
    quot(zero,s(Y)) = zero ).

cnf(rule9,axiom,
    quot(s(X),s(Y)) = s(quot(minus(X,Y),s(Y))) ).

cnf(rule10,axiom,
    log(s(zero)) = zero ).

cnf(rule11,axiom,
    log(s(s(X))) = s(log(s(quot(X,s(s(zero)))))) ).

cnf(double1,axiom,
    d(zero) = zero ).

cnf(double2,axiom,
    d(s(X)) = s(s(d(X))) ).

cnf(exp1,axiom,
    e(zero) = s(zero) ).

cnf(exp2,axiom,
    e(s(X)) = d(e(X)) ).

cnf(goal,negated_conjecture,
    log(e(X)) != s(s(s(s(zero)))) ).

%------------------------------------------------------------------------------
