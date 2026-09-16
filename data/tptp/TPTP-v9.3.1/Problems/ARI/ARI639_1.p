%------------------------------------------------------------------------------
% File     : ARI639_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 15
% Version  : Especial.
% English  :

% Refs     : [ALR14] Avigad et al. (2014), A Heuristic Prover for Real Ineq
%          : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 15 [Lew14]

% Status   : Theorem
% Rating   : 0.50 v9.1.0, 0.60 v9.0.0, 0.50 v7.5.0, 0.40 v7.4.0, 0.67 v7.3.0, 0.50 v7.1.0, 0.67 v7.0.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :   11 (   6 unt;   5 typ;   0 def)
%            Number of atoms       :    6 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    7 (   2 avg)
%            Number arithmetic     :   28 (   6 atm;  11 fun;  11 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   12 (   5 usr;   9 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(eps_type,type,
    eps: $real ).

tff(c_type,type,
    c: $real ).

tff(k_type,type,
    k: $real ).

tff(x_type,type,
    x: $real ).

tff(n_type,type,
    n: $real ).

tff(hypothesis,hypothesis,
    $greatereq(n,0.0) ).

tff(hypothesis_01,hypothesis,
    $less(n,$product($quotient(1.0,2.0),$product(k,x))) ).

tff(hypothesis_02,hypothesis,
    $greater(c,0.0) ).

tff(hypothesis_03,hypothesis,
    $greater(eps,0.0) ).

tff(hypothesis_04,hypothesis,
    $less(eps,1.0) ).

tff(conclusion,conjecture,
    $less($product($sum($product($quotient(1.0,3.0),$product($quotient(1.0,$sum(3.0,c)),eps)),1.0),n),$product(k,x)) ).

%------------------------------------------------------------------------------
