%------------------------------------------------------------------------------
% File     : ARI640_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 18
% Version  : Especial.
% English  :

% Refs     : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 18 [Lew14]

% Status   : ContradictoryAxioms
% Rating   : 0.50 v9.1.0, 0.40 v9.0.0, 0.50 v8.2.0, 0.33 v7.5.0, 0.40 v7.4.0, 0.33 v7.3.0, 0.25 v7.1.0, 0.33 v7.0.0, 0.67 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    7 (   5 unt;   2 typ;   0 def)
%            Number of atoms       :    5 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    9 (   4 atm;   2 fun;   3 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   1 prp; 0-2 aty)
%            Number of functors    :    6 (   2 usr;   4 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_CAX_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $real ).

tff(y_type,type,
    y: $real ).

tff(hypothesis,hypothesis,
    $greater(x,0.0) ).

tff(hypothesis_01,hypothesis,
    $greater(y,0.0) ).

tff(hypothesis_02,hypothesis,
    $less(y,1.0) ).

tff(hypothesis_03,hypothesis,
    $greater($product(x,y),$sum(x,y)) ).

tff(conclusion,conjecture,
    $false ).

%------------------------------------------------------------------------------
