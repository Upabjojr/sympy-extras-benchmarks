%------------------------------------------------------------------------------
% File     : ARI120_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Product of X and X is 4
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v9.1.0, 0.25 v8.2.0, 0.50 v7.5.0, 0.60 v7.4.0, 0.50 v7.3.0, 0.33 v7.0.0, 0.43 v6.4.0, 0.67 v6.3.0, 0.57 v6.2.0, 0.75 v6.1.0, 0.67 v6.0.0, 0.71 v5.5.0, 0.67 v5.4.0, 0.75 v5.3.0, 0.80 v5.2.0, 0.83 v5.1.0, 1.00 v5.0.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    4 (   2 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    4 (   1   ~;   0   |;   2   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    7 (   7 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    5 (   0 atm;   1 fun;   2 num;   2 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   1 usr;   0 prp; 1-2 aty)
%            Number of functors    :    3 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    2 (   0   !;   2   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(p_type,type,
    p: $int > $o ).

tff(product_X_X_4_predicate,conjecture,
    ( p(2)
   => ? [X: $int,Y: $int] :
        ( p(X)
        & ( X != Y )
        & ( $product(Y,Y) = 4 ) ) ) ).

%------------------------------------------------------------------------------
