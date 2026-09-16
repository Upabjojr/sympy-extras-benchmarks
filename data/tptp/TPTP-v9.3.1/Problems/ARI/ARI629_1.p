%------------------------------------------------------------------------------
% File     : ARI629_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 1
% Version  : Especial.
% English  :

% Refs     : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 1 [Lew14]

% Status   : Theorem
% Rating   : 0.50 v9.1.0, 0.40 v9.0.0, 0.50 v8.2.0, 0.33 v7.5.0, 0.40 v7.4.0, 0.33 v7.3.0, 0.25 v7.1.0, 0.33 v7.0.0, 0.67 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    4 (   2 unt;   2 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   10 (   2 atm;   5 fun;   3 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    5 (   2 usr;   3 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $real ).

tff(y_type,type,
    y: $real ).

tff(hypothesis,hypothesis,
    $greater(x,1.0) ).

tff(conclusion,conjecture,
    $greatereq($product($sum(1.0,$product(y,y)),x),$sum(1.0,$product(y,y))) ).

%------------------------------------------------------------------------------
