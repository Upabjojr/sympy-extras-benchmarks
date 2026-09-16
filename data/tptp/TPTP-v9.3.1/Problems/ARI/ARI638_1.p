%------------------------------------------------------------------------------
% File     : ARI638_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 14
% Version  : Especial.
% English  :

% Refs     : [ALR14] Avigad et al. (2014), A Heuristic Prover for Real Ineq
%          : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 14 [Lew14]

% Status   : Theorem
% Rating   : 0.40 v9.3.0, 0.50 v9.1.0, 0.75 v9.0.0, 0.62 v8.2.0, 0.75 v7.5.0, 0.90 v7.4.0, 0.88 v7.3.0, 0.83 v7.1.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    9 (   4 unt;   5 typ;   0 def)
%            Number of atoms       :    4 (   1 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   2 avg)
%            Maximal term depth    :    5 (   2 avg)
%            Number arithmetic     :   15 (   3 atm;   7 fun;   3 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    9 (   5 usr;   6 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $real ).

tff(b_type,type,
    b: $real ).

tff(c_type,type,
    c: $real ).

tff(d_type,type,
    d: $real ).

tff(f_type,type,
    f: $real > $real ).

tff(f_feature,axiom,
    ! [X: $real,Y: $real] : ( f($sum(X,Y)) = $product(f(X),f(Y)) ) ).

tff(hypothesis,hypothesis,
    $greater(f($sum(a,b)),2.0) ).

tff(hypothesis_01,hypothesis,
    $greater(f($sum(c,d)),2.0) ).

tff(conclusion,conjecture,
    $greater(f($sum(a,$sum(b,$sum(c,d)))),4.0) ).

%------------------------------------------------------------------------------
