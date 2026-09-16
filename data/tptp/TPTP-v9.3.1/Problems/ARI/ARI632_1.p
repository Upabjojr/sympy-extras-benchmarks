%------------------------------------------------------------------------------
% File     : ARI632_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 6
% Version  : Especial.
% English  :

% Refs     : [ALR14] Avigad et al. (2014), A Heuristic Prover for Real Ineq
%          : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 6 [Lew14]

% Status   : Theorem
% Rating   : 0.25 v9.1.0, 0.20 v9.0.0, 0.25 v8.2.0, 0.17 v7.5.0, 0.20 v7.4.0, 0.17 v7.3.0, 0.38 v7.1.0, 0.17 v6.4.0, 0.00 v6.3.0
% Syntax   : Number of formulae    :    9 (   3 unt;   5 typ;   0 def)
%            Number of atoms       :    5 (   0 equ)
%            Maximal formula atoms :    2 (   1 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   2 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :    9 (   5 atm;   2 fun;   0 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   5 usr;   4 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $real ).

tff(y_type,type,
    y: $real ).

tff(u_type,type,
    u: $real ).

tff(v_type,type,
    v: $real ).

tff(f_type,type,
    f: $real > $real ).

tff(f_non_decreasing,axiom,
    ! [X: $real,Y: $real] :
      ( $greatereq(X,Y)
     => $greatereq(f(X),f(Y)) ) ).

tff(hypothesis,hypothesis,
    $less(u,v) ).

tff(hypothesis_01,hypothesis,
    $lesseq(x,y) ).

tff(conclusion,conjecture,
    $less($sum(u,f(x)),$sum(v,f(y))) ).

%------------------------------------------------------------------------------
